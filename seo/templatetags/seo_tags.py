"""
Template tags para SEO
"""
from django import template
from django.utils.safestring import mark_safe
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
import json

from ..models import SEOMeta, SEOConfig

register = template.Library()


@register.inclusion_tag('seo/meta_tags.html', takes_context=True)
def render_seo(context, obj=None):
    """
    Template tag principal para renderizar todas as meta tags SEO
    
    Uso: {% render_seo object %}
    """
    request = context['request']
    try:
        seo_config = SEOConfig.get_config()
    except:
        # Fallback se não houver configuração
        seo_config = None
    
    # Dados padrão
    seo_data = {
        'title': seo_config.site_name if seo_config else 'Prisma Avaliações Imobiliárias',
        'description': seo_config.site_description if seo_config else 'Avaliações imobiliárias profissionais',
        'keywords': seo_config.default_keywords if seo_config else 'avaliação imobiliária',
        'canonical_url': request.build_absolute_uri(),
        'robots': 'index, follow',
        'og_title': seo_config.site_name if seo_config else 'Prisma Avaliações Imobiliárias',
        'og_description': seo_config.site_description if seo_config else 'Avaliações imobiliárias profissionais',
        'og_type': 'website',
        'og_image': None,
        'twitter_card': 'summary_large_image',
        'twitter_title': seo_config.site_name if seo_config else 'Prisma Avaliações Imobiliárias',
        'twitter_description': seo_config.site_description if seo_config else 'Avaliações imobiliárias profissionais',
        'twitter_image': None,
        'schema_markup': '',
    }
    
    # Adicionar imagem padrão se existir
    if seo_config and seo_config.default_og_image:
        seo_data['og_image'] = request.build_absolute_uri(seo_config.default_og_image.url)
        seo_data['twitter_image'] = seo_data['og_image']
    
    # Se objeto fornecido, buscar SEO específico
    if obj:
        try:
            content_type = ContentType.objects.get_for_model(obj)
            seo_meta = SEOMeta.objects.get(
                content_type=content_type,
                object_id=obj.pk
            )
            
            # Sobrescrever com dados específicos
            seo_data.update({
                'title': seo_meta.get_title(),
                'description': seo_meta.get_description(),
                'keywords': seo_meta.keywords or seo_data['keywords'],
                'canonical_url': seo_meta.canonical_url or request.build_absolute_uri(),
                'robots': seo_meta.get_robots_content(),
                'og_title': seo_meta.get_og_title(),
                'og_description': seo_meta.get_og_description(),
                'og_type': seo_meta.og_type,
                'twitter_card': seo_meta.twitter_card,
                'twitter_title': seo_meta.get_twitter_title(),
                'twitter_description': seo_meta.get_twitter_description(),
                'schema_markup': seo_meta.get_schema_markup_safe(),
            })
            
            # Imagens específicas
            if seo_meta.og_image:
                seo_data['og_image'] = request.build_absolute_uri(seo_meta.og_image.url)
            
            if seo_meta.twitter_image:
                seo_data['twitter_image'] = request.build_absolute_uri(seo_meta.twitter_image.url)
            elif seo_meta.og_image:
                seo_data['twitter_image'] = seo_data['og_image']
            
        except SEOMeta.DoesNotExist:
            # Se não existe SEO específico, tentar extrair do objeto
            if hasattr(obj, 'get_absolute_url'):
                seo_data['canonical_url'] = request.build_absolute_uri(obj.get_absolute_url())
            
            # Tentar usar campos do objeto para title e description
            if hasattr(obj, 'titulo'):
                seo_data['title'] = f"{obj.titulo} | {seo_config.site_name}"
                seo_data['og_title'] = obj.titulo
                seo_data['twitter_title'] = obj.titulo
            elif hasattr(obj, 'title'):
                seo_data['title'] = f"{obj.title} | {seo_config.site_name}"
                seo_data['og_title'] = obj.title
                seo_data['twitter_title'] = obj.title
            
            if hasattr(obj, 'resumo'):
                seo_data['description'] = obj.resumo[:160]
                seo_data['og_description'] = obj.resumo[:160]
                seo_data['twitter_description'] = obj.resumo[:160]
            elif hasattr(obj, 'description'):
                seo_data['description'] = obj.description[:160]
                seo_data['og_description'] = obj.description[:160]
                seo_data['twitter_description'] = obj.description[:160]
            
            # Tentar usar imagem do objeto
            if hasattr(obj, 'imagem_destaque') and obj.imagem_destaque:
                seo_data['og_image'] = request.build_absolute_uri(obj.imagem_destaque.url)
                seo_data['twitter_image'] = seo_data['og_image']
            elif hasattr(obj, 'image') and obj.image:
                seo_data['og_image'] = request.build_absolute_uri(obj.image.url)
                seo_data['twitter_image'] = seo_data['og_image']
    
    return {
        'seo': seo_data,
        'config': seo_config,
        'request': request,
    }


@register.simple_tag
def google_analytics():
    """
    Adiciona código do Google Analytics
    
    Uso: {% google_analytics %}
    """
    config = SEOConfig.get_config()
    if not config.google_analytics_id:
        return ''
    
    if config.google_analytics_id.startswith('G-'):
        # Google Analytics 4
        return mark_safe(f'''
        <!-- Google Analytics 4 -->
        <script async src="https://www.googletagmanager.com/gtag/js?id={config.google_analytics_id}"></script>
        <script>
            window.dataLayer = window.dataLayer || [];
            function gtag(){{dataLayer.push(arguments);}}
            gtag('js', new Date());
            gtag('config', '{config.google_analytics_id}');
        </script>
        ''')
    else:
        # Universal Analytics (legado)
        return mark_safe(f'''
        <!-- Google Analytics Universal -->
        <script async src="https://www.google-analytics.com/analytics.js"></script>
        <script>
            (function(i,s,o,g,r,a,m){{i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){{
            (i[r].q=i[r].q||[]).push(arguments)}},i[r].l=1*new Date();a=s.createElement(o),
            m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
            }})(window,document,'script','https://www.google-analytics.com/analytics.js','ga');
            ga('create', '{config.google_analytics_id}', 'auto');
            ga('send', 'pageview');
        </script>
        ''')


@register.simple_tag
def google_tag_manager_head():
    """
    Google Tag Manager - código para <head>
    
    Uso: {% google_tag_manager_head %}
    """
    config = SEOConfig.get_config()
    if not config.google_tag_manager_id:
        return ''
    
    return mark_safe(f'''
    <!-- Google Tag Manager -->
    <script>(function(w,d,s,l,i){{w[l]=w[l]||[];w[l].push({{'gtm.start':
    new Date().getTime(),event:'gtm.js'}});var f=d.getElementsByTagName(s)[0],
    j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
    'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
    }})(window,document,'script','dataLayer','{config.google_tag_manager_id}');</script>
    <!-- End Google Tag Manager -->
    ''')


@register.simple_tag
def google_tag_manager_body():
    """
    Google Tag Manager - código para <body>
    
    Uso: {% google_tag_manager_body %}
    """
    config = SEOConfig.get_config()
    if not config.google_tag_manager_id:
        return ''
    
    return mark_safe(f'''
    <!-- Google Tag Manager (noscript) -->
    <noscript><iframe src="https://www.googletagmanager.com/ns.html?id={config.google_tag_manager_id}"
    height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
    <!-- End Google Tag Manager (noscript) -->
    ''')


@register.simple_tag
def facebook_pixel():
    """
    Adiciona código do Facebook Pixel
    
    Uso: {% facebook_pixel %}
    """
    config = SEOConfig.get_config()
    if not config.facebook_pixel_id:
        return ''
    
    return mark_safe(f'''
    <!-- Facebook Pixel -->
    <script>
    !function(f,b,e,v,n,t,s)
    {{if(f.fbq)return;n=f.fbq=function(){{n.callMethod?
    n.callMethod.apply(n,arguments):n.queue.push(arguments)}};
    if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
    n.queue=[];t=b.createElement(e);t.async=!0;
    t.src=v;s=b.getElementsByTagName(e)[0];
    s.parentNode.insertBefore(t,s)}}(window,document,'script',
    'https://connect.facebook.net/en_US/fbevents.js');
    fbq('init', '{config.facebook_pixel_id}');
    fbq('track', 'PageView');
    </script>
    <noscript>
    <img height="1" width="1" 
    src="https://www.facebook.com/tr?id={config.facebook_pixel_id}&ev=PageView&noscript=1"/>
    </noscript>
    <!-- End Facebook Pixel -->
    ''')


@register.simple_tag
def organization_schema():
    """
    Adiciona schema.org da organização
    
    Uso: {% organization_schema %}
    """
    config = SEOConfig.get_config()
    return config.get_organization_schema()


@register.simple_tag
def breadcrumb_schema(breadcrumbs):
    """
    Adiciona schema.org de breadcrumb
    
    Uso: {% breadcrumb_schema breadcrumb_list %}
    
    breadcrumb_list deve ser uma lista de dicionários:
    [
        {'name': 'Home', 'url': '/'},
        {'name': 'Artigos', 'url': '/artigos/'},
        {'name': 'Título do Artigo', 'url': '/artigos/titulo-artigo/'},
    ]
    """
    if not breadcrumbs:
        return ''
    
    items = []
    for position, breadcrumb in enumerate(breadcrumbs, 1):
        items.append({
            "@type": "ListItem",
            "position": position,
            "name": breadcrumb['name'],
            "item": breadcrumb['url']
        })
    
    schema = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": items
    }
    
    return mark_safe(f'<script type="application/ld+json">{json.dumps(schema, ensure_ascii=False)}</script>')


@register.filter
def seo_exists(obj):
    """
    Verifica se objeto tem SEO configurado
    
    Uso: {% if object|seo_exists %}
    """
    if not obj:
        return False
    
    try:
        content_type = ContentType.objects.get_for_model(obj)
        return SEOMeta.objects.filter(
            content_type=content_type,
            object_id=obj.pk
        ).exists()
    except:
        return False


@register.simple_tag(takes_context=True)
def current_url(context):
    """
    Retorna a URL atual completa
    
    Uso: {% current_url %}
    """
    request = context['request']
    return request.build_absolute_uri()


@register.simple_tag
def site_verification_tags():
    """
    Adiciona tags de verificação de sites
    
    Uso: {% site_verification_tags %}
    """
    config = SEOConfig.get_config()
    tags = []
    
    if config.google_search_console_id:
        tags.append(f'<meta name="google-site-verification" content="{config.google_search_console_id}">')
    
    if config.bing_webmaster_id:
        tags.append(f'<meta name="msvalidate.01" content="{config.bing_webmaster_id}">')
    
    return mark_safe('\n'.join(tags))


# Template tags adicionais que podem ser chamados
@register.simple_tag
def seo_meta_tags():
    """Template tag simplificado para meta tags básicas"""
    try:
        config = SEOConfig.get_config()
        return mark_safe(f'''
        <meta name="description" content="{config.site_description}">
        <meta name="keywords" content="{config.default_keywords}">
        <meta name="author" content="{config.organization_name}">
        ''')
    except:
        return mark_safe('')


@register.simple_tag
def schema_org_data():
    """Template tag para dados estruturados Schema.org"""
    try:
        config = SEOConfig.get_config()
        schema = config.get_organization_schema()
        return mark_safe(f'<script type="application/ld+json">{schema}</script>')
    except:
        return mark_safe('')


@register.simple_tag
def google_analytics():
    """Template tag para Google Analytics"""
    try:
        config = SEOConfig.get_config()
        if config.google_analytics_id:
            return mark_safe(f'''
            <script async src="https://www.googletagmanager.com/gtag/js?id={config.google_analytics_id}"></script>
            <script>
              window.dataLayer = window.dataLayer || [];
              function gtag(){{dataLayer.push(arguments);}}
              gtag('js', new Date());
              gtag('config', '{config.google_analytics_id}');
            </script>
            ''')
    except:
        pass
    return mark_safe('')


@register.simple_tag
def google_tag_manager():
    """Template tag para Google Tag Manager"""
    try:
        config = SEOConfig.get_config()
        if config.google_tag_manager_id:
            return mark_safe(f'''
            <script>(function(w,d,s,l,i){{w[l]=w[l]||[];w[l].push({{'gtm.start':
            new Date().getTime(),event:'gtm.js'}});var f=d.getElementsByTagName(s)[0],
            j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
            'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
            }})(window,document,'script','dataLayer','{config.google_tag_manager_id}');</script>
            ''')
    except:
        pass
    return mark_safe('')


@register.simple_tag
def google_tag_manager_body():
    """Template tag para Google Tag Manager (body)"""
    try:
        config = SEOConfig.get_config()
        if config.google_tag_manager_id:
            return mark_safe(f'''
            <noscript><iframe src="https://www.googletagmanager.com/ns.html?id={config.google_tag_manager_id}"
            height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
            ''')
    except:
        pass
    return mark_safe('')


@register.inclusion_tag('seo/seo_head.html', takes_context=True)
def render_seo_meta(context, obj=None, include_json_ld=True):
    """
    Renderiza todas as meta tags SEO usando o template seo_head.html
    
    Uso: {% render_seo_meta object %}
    """
    request = context['request']
    
    # Obter configuração global
    try:
        seo_config = SEOConfig.get_config()
    except:
        seo_config = None
    
    # Obter SEO Meta específico para o objeto
    seo_meta = None
    if obj:
        try:
            content_type = ContentType.objects.get_for_model(obj)
            seo_meta = SEOMeta.objects.filter(
                content_type=content_type,
                object_id=obj.pk
            ).first()
        except:
            pass
    
    return {
        'request': request,
        'seo_meta': seo_meta,
        'seo_config': seo_config,
        'include_json_ld': include_json_ld,
    }


@register.simple_tag
def get_seo_config():
    """
    Retorna a configuração global de SEO
    
    Uso: {% get_seo_config as config %}
    """
    try:
        return SEOConfig.get_config()
    except:
        return None


@register.inclusion_tag('seo/json_ld.html', takes_context=True)
def render_json_ld(context, obj=None):
    """
    Renderiza dados estruturados JSON-LD
    
    Uso: {% render_json_ld object %}
    """
    request = context['request']
    
    # Obter configuração global
    try:
        seo_config = SEOConfig.get_config()
    except:
        seo_config = None
    
    # Obter SEO Meta específico para o objeto
    seo_meta = None
    if obj:
        try:
            content_type = ContentType.objects.get_for_model(obj)
            seo_meta = SEOMeta.objects.filter(
                content_type=content_type,
                object_id=obj.pk
            ).first()
        except:
            pass
    
    return {
        'request': request,
        'seo_meta': seo_meta,
        'seo_config': seo_config,
        'obj': obj,
    }
