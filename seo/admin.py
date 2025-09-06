"""
Admin para SEO
"""
from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from django.utils.safestring import mark_safe
from django.urls import reverse
from django.utils.html import format_html
from .models import SEOMeta, SEOConfig


class SEOMetaInline(GenericTabularInline):
    """
    Inline para adicionar SEO Meta em qualquer modelo
    """
    model = SEOMeta
    extra = 0
    max_num = 1
    
    fieldsets = (
        ('Meta Tags Básicas', {
            'fields': ('title', 'description', 'keywords'),
            'classes': ('wide',)
        }),
        ('Configurações', {
            'fields': ('canonical_url', 'noindex', 'nofollow'),
            'classes': ('collapse', 'wide')
        }),
        ('Open Graph', {
            'fields': ('og_title', 'og_description', 'og_image', 'og_type'),
            'classes': ('collapse', 'wide')
        }),
        ('Twitter Cards', {
            'fields': ('twitter_card', 'twitter_title', 'twitter_description', 'twitter_image'),
            'classes': ('collapse', 'wide')
        }),
        ('Schema.org (JSON-LD)', {
            'fields': ('schema_markup',),
            'classes': ('collapse', 'wide')
        }),
    )
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('content_type')


@admin.register(SEOMeta)
class SEOMetaAdmin(admin.ModelAdmin):
    """
    Admin para gerenciar SEO Meta diretamente
    """
    list_display = ['title', 'content_type', 'content_object_link', 'noindex', 'nofollow', 'updated_at']
    list_filter = ['content_type', 'noindex', 'nofollow', 'og_type', 'twitter_card', 'created_at']
    search_fields = ['title', 'description', 'keywords']
    readonly_fields = ['content_object_link', 'preview_meta_tags', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Objeto Vinculado', {
            'fields': ('content_type', 'object_id', 'content_object_link')
        }),
        ('Meta Tags Básicas', {
            'fields': ('title', 'description', 'keywords'),
            'classes': ('wide',)
        }),
        ('Configurações', {
            'fields': ('canonical_url', 'noindex', 'nofollow'),
            'classes': ('collapse', 'wide')
        }),
        ('Open Graph', {
            'fields': ('og_title', 'og_description', 'og_image', 'og_type'),
            'classes': ('collapse', 'wide')
        }),
        ('Twitter Cards', {
            'fields': ('twitter_card', 'twitter_title', 'twitter_description', 'twitter_image'),
            'classes': ('collapse', 'wide')
        }),
        ('Schema.org (JSON-LD)', {
            'fields': ('schema_markup',),
            'classes': ('collapse', 'wide')
        }),
        ('Preview', {
            'fields': ('preview_meta_tags',),
            'classes': ('collapse', 'wide')
        }),
        ('Controle', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def content_object_link(self, obj):
        """Link para o objeto vinculado"""
        if obj.content_object:
            try:
                url = reverse(
                    f'admin:{obj.content_type.app_label}_{obj.content_type.model}_change',
                    args=[obj.object_id]
                )
                return format_html('<a href="{}" target="_blank">{}</a>', url, obj.content_object)
            except:
                return str(obj.content_object)
        return '-'
    content_object_link.short_description = 'Objeto'
    
    def preview_meta_tags(self, obj):
        """Preview das meta tags"""
        if not obj.pk:
            return '-'
        
        html = f'''
        <div style="background: #f8f9fa; padding: 15px; border-radius: 5px; font-family: monospace; font-size: 12px;">
            <strong>Preview das Meta Tags:</strong><br><br>
            
            &lt;title&gt;{obj.get_title()}&lt;/title&gt;<br>
            &lt;meta name="description" content="{obj.get_description()}"&gt;<br>
            
            {f'&lt;meta name="keywords" content="{obj.keywords}"&gt;<br>' if obj.keywords else ''}
            {f'&lt;link rel="canonical" href="{obj.canonical_url}"&gt;<br>' if obj.canonical_url else ''}
            &lt;meta name="robots" content="{obj.get_robots_content()}"&gt;<br><br>
            
            <strong>Open Graph:</strong><br>
            &lt;meta property="og:title" content="{obj.get_og_title()}"&gt;<br>
            &lt;meta property="og:description" content="{obj.get_og_description()}"&gt;<br>
            &lt;meta property="og:type" content="{obj.og_type}"&gt;<br>
            {f'&lt;meta property="og:image" content="{obj.og_image.url}"&gt;<br>' if obj.og_image else ''}<br>
            
            <strong>Twitter Cards:</strong><br>
            &lt;meta name="twitter:card" content="{obj.twitter_card}"&gt;<br>
            &lt;meta name="twitter:title" content="{obj.get_twitter_title()}"&gt;<br>
            &lt;meta name="twitter:description" content="{obj.get_twitter_description()}"&gt;<br>
            {f'&lt;meta name="twitter:image" content="{obj.twitter_image.url}"&gt;<br>' if obj.twitter_image else ''}
        </div>
        '''
        return mark_safe(html)
    preview_meta_tags.short_description = 'Preview'
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('content_type')


@admin.register(SEOConfig)
class SEOConfigAdmin(admin.ModelAdmin):
    """
    Admin para configurações globais de SEO
    """
    fieldsets = (
        ('Configurações Básicas do Site', {
            'fields': ('site_name', 'site_domain', 'site_description', 'default_keywords'),
            'classes': ('wide',)
        }),
        ('Imagens Padrão', {
            'fields': ('default_og_image',),
            'classes': ('collapse', 'wide')
        }),
        ('Analytics & Tracking', {
            'fields': (
                'google_analytics_id', 
                'google_tag_manager_id', 
                'google_search_console_id', 
                'bing_webmaster_id', 
                'facebook_pixel_id'
            ),
            'classes': ('collapse', 'wide')
        }),
        ('Dados da Organização (Schema.org)', {
            'fields': (
                'organization_name', 
                'organization_logo', 
                'organization_phone', 
                'organization_email', 
                'organization_address'
            ),
            'classes': ('collapse', 'wide')
        }),
        ('Configurações do Sitemap', {
            'fields': ('sitemap_changefreq', 'sitemap_priority'),
            'classes': ('collapse', 'wide')
        }),
        ('Controle', {
            'fields': ('updated_at',),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['updated_at']
    
    def has_add_permission(self, request):
        """Permitir apenas uma configuração"""
        return not SEOConfig.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        """Não permitir deletar a configuração"""
        return False
    
    def changelist_view(self, request, extra_context=None):
        """Redirecionar para edição se config existir"""
        if SEOConfig.objects.exists():
            config = SEOConfig.objects.first()
            from django.shortcuts import redirect
            return redirect('admin:seo_seoconfig_change', config.pk)
        return super().changelist_view(request, extra_context)


# Registrar o inline para uso em outros apps
# Exemplo de uso em outros admins:
# 
# from seo.admin import SEOMetaInline
# 
# class ArtigoAdmin(admin.ModelAdmin):
#     inlines = [SEOMetaInline]
