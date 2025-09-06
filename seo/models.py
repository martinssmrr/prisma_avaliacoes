"""
Modelos para SEO otimização
Autor: GitHub Copilot
Data: 2025-09-04
"""
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.urls import reverse
from django.core.validators import MaxLengthValidator
from django.utils.safestring import mark_safe
import json


class SEOMeta(models.Model):
    """
    Modelo para armazenar metadados SEO para qualquer objeto do Django
    usando GenericForeignKey
    """
    
    # Relação genérica com qualquer modelo
    content_type = models.ForeignKey(
        ContentType, 
        on_delete=models.CASCADE,
        verbose_name='Tipo de Conteúdo'
    )
    object_id = models.PositiveIntegerField(verbose_name='ID do Objeto')
    content_object = GenericForeignKey('content_type', 'object_id')
    
    # Meta Tags Básicas
    title = models.CharField(
        'Título SEO',
        max_length=60,
        validators=[MaxLengthValidator(60)],
        help_text='Título otimizado para SEO (máximo 60 caracteres)'
    )
    
    description = models.TextField(
        'Descrição SEO',
        max_length=160,
        validators=[MaxLengthValidator(160)],
        help_text='Descrição para mecanismos de busca (máximo 160 caracteres)'
    )
    
    keywords = models.CharField(
        'Palavras-chave',
        max_length=255,
        blank=True,
        help_text='Palavras-chave separadas por vírgula'
    )
    
    canonical_url = models.URLField(
        'URL Canônica',
        blank=True,
        help_text='URL canônica da página (deixe vazio para usar a URL atual)'
    )
    
    # Robots Meta Tags
    noindex = models.BooleanField(
        'No Index',
        default=False,
        help_text='Impedir indexação nos mecanismos de busca'
    )
    
    nofollow = models.BooleanField(
        'No Follow',
        default=False,
        help_text='Impedir que robôs sigam os links desta página'
    )
    
    # Open Graph Tags
    og_title = models.CharField(
        'Título Open Graph',
        max_length=60,
        blank=True,
        help_text='Título para redes sociais (Facebook, LinkedIn)'
    )
    
    og_description = models.TextField(
        'Descrição Open Graph',
        max_length=160,
        blank=True,
        help_text='Descrição para redes sociais'
    )
    
    og_image = models.ImageField(
        'Imagem Open Graph',
        upload_to='seo/og_images/',
        blank=True,
        help_text='Imagem para compartilhamento (recomendado: 1200x630px)'
    )
    
    og_type = models.CharField(
        'Tipo Open Graph',
        max_length=20,
        default='website',
        choices=[
            ('website', 'Website'),
            ('article', 'Artigo'),
            ('blog', 'Blog'),
            ('product', 'Produto'),
            ('business', 'Negócio'),
        ],
        help_text='Tipo de conteúdo para Open Graph'
    )
    
    # Twitter Cards
    twitter_card = models.CharField(
        'Twitter Card',
        max_length=20,
        default='summary_large_image',
        choices=[
            ('summary', 'Summary'),
            ('summary_large_image', 'Summary Large Image'),
            ('app', 'App'),
            ('player', 'Player'),
        ],
        help_text='Tipo de Twitter Card'
    )
    
    twitter_title = models.CharField(
        'Título Twitter',
        max_length=60,
        blank=True,
        help_text='Título para Twitter'
    )
    
    twitter_description = models.TextField(
        'Descrição Twitter',
        max_length=160,
        blank=True,
        help_text='Descrição para Twitter'
    )
    
    twitter_image = models.ImageField(
        'Imagem Twitter',
        upload_to='seo/twitter_images/',
        blank=True,
        help_text='Imagem para Twitter Cards'
    )
    
    # JSON-LD Schema.org
    schema_markup = models.TextField(
        'Schema Markup (JSON-LD)',
        blank=True,
        help_text='Código JSON-LD para dados estruturados Schema.org'
    )
    
    # Controle
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)
    
    class Meta:
        verbose_name = 'SEO Meta'
        verbose_name_plural = 'SEO Metas'
        unique_together = ('content_type', 'object_id')
        ordering = ['-updated_at']
    
    def __str__(self):
        return f'SEO: {self.title}'
    
    def get_title(self):
        """Retorna o título SEO ou o título do objeto"""
        return self.title or str(self.content_object)
    
    def get_description(self):
        """Retorna a descrição SEO"""
        return self.description
    
    def get_og_title(self):
        """Retorna o título Open Graph ou o título SEO"""
        return self.og_title or self.get_title()
    
    def get_og_description(self):
        """Retorna a descrição Open Graph ou a descrição SEO"""
        return self.og_description or self.get_description()
    
    def get_twitter_title(self):
        """Retorna o título Twitter ou o título SEO"""
        return self.twitter_title or self.get_title()
    
    def get_twitter_description(self):
        """Retorna a descrição Twitter ou a descrição SEO"""
        return self.twitter_description or self.get_description()
    
    def get_robots_content(self):
        """Retorna o conteúdo da meta tag robots"""
        robots = []
        if self.noindex:
            robots.append('noindex')
        else:
            robots.append('index')
        
        if self.nofollow:
            robots.append('nofollow')
        else:
            robots.append('follow')
        
        return ', '.join(robots)
    
    def get_schema_markup_safe(self):
        """Retorna o schema markup como HTML seguro"""
        if not self.schema_markup:
            return ''
        
        try:
            # Valida se é JSON válido
            json.loads(self.schema_markup)
            return mark_safe(f'<script type="application/ld+json">{self.schema_markup}</script>')
        except json.JSONDecodeError:
            return ''
    
    def clean(self):
        """Validação customizada"""
        from django.core.exceptions import ValidationError
        
        # Validar JSON-LD se fornecido
        if self.schema_markup:
            try:
                json.loads(self.schema_markup)
            except json.JSONDecodeError:
                raise ValidationError({
                    'schema_markup': 'JSON inválido. Verifique a sintaxe.'
                })


class SEOConfig(models.Model):
    """
    Configurações globais de SEO para o site
    """
    
    # Configurações básicas do site
    site_name = models.CharField(
        'Nome do Site',
        max_length=100,
        default='Prisma Avaliações Imobiliárias'
    )
    
    site_domain = models.CharField(
        'Domínio do Site',
        max_length=100,
        default='prismaavaliacoes.com.br',
        help_text='Domínio sem http:// ou https://'
    )
    
    site_description = models.TextField(
        'Descrição do Site',
        max_length=160,
        default='Avaliações imobiliárias profissionais e consultoria especializada',
        help_text='Descrição padrão do site'
    )
    
    default_keywords = models.TextField(
        'Palavras-chave Padrão',
        default='avaliação imobiliária, laudo de avaliação, perícia imobiliária, consultoria imobiliária',
        help_text='Palavras-chave padrão do site (separadas por vírgula)'
    )
    
    # Open Graph padrão
    default_og_image = models.ImageField(
        'Imagem Padrão Open Graph',
        upload_to='seo/default/',
        blank=True,
        help_text='Imagem padrão para compartilhamento (1200x630px)'
    )
    
    # Analytics e Tracking
    google_analytics_id = models.CharField(
        'Google Analytics ID',
        max_length=20,
        blank=True,
        help_text='Ex: G-XXXXXXXXXX ou UA-XXXXXXXX-X'
    )
    
    google_tag_manager_id = models.CharField(
        'Google Tag Manager ID',
        max_length=20,
        blank=True,
        help_text='Ex: GTM-XXXXXXX'
    )
    
    google_search_console_id = models.CharField(
        'Google Search Console Verification',
        max_length=100,
        blank=True,
        help_text='Código de verificação do Google Search Console'
    )
    
    bing_webmaster_id = models.CharField(
        'Bing Webmaster Verification',
        max_length=100,
        blank=True,
        help_text='Código de verificação do Bing Webmaster'
    )
    
    facebook_pixel_id = models.CharField(
        'Facebook Pixel ID',
        max_length=20,
        blank=True,
        help_text='ID do Facebook Pixel'
    )
    
    # Schema.org Organization
    organization_name = models.CharField(
        'Nome da Organização',
        max_length=100,
        default='Prisma Avaliações Imobiliárias'
    )
    
    organization_logo = models.ImageField(
        'Logo da Organização',
        upload_to='seo/organization/',
        blank=True,
        help_text='Logo para Schema.org Organization'
    )
    
    organization_phone = models.CharField(
        'Telefone da Organização',
        max_length=20,
        blank=True
    )
    
    organization_email = models.EmailField(
        'Email da Organização',
        blank=True
    )
    
    organization_address = models.TextField(
        'Endereço da Organização',
        blank=True
    )
    
    # Configurações do Sitemap
    sitemap_changefreq = models.CharField(
        'Frequência de Mudança do Sitemap',
        max_length=10,
        default='weekly',
        choices=[
            ('always', 'Always'),
            ('hourly', 'Hourly'),
            ('daily', 'Daily'),
            ('weekly', 'Weekly'),
            ('monthly', 'Monthly'),
            ('yearly', 'Yearly'),
            ('never', 'Never'),
        ]
    )
    
    sitemap_priority = models.DecimalField(
        'Prioridade do Sitemap',
        max_digits=2,
        decimal_places=1,
        default=0.8,
        help_text='Prioridade padrão (0.0 a 1.0)'
    )
    
    # Controle
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)
    
    class Meta:
        verbose_name = 'Configuração SEO'
        verbose_name_plural = 'Configurações SEO'
    
    def __str__(self):
        return f'Configurações SEO - {self.site_name}'
    
    def save(self, *args, **kwargs):
        # Garantir que só existe uma configuração
        if not self.pk and SEOConfig.objects.exists():
            raise ValueError('Só pode existir uma configuração SEO')
        super().save(*args, **kwargs)
    
    @classmethod
    def get_config(cls):
        """Retorna a configuração SEO (cria se não existir)"""
        config, created = cls.objects.get_or_create(
            pk=1,
            defaults={
                'site_name': 'Prisma Avaliações Imobiliárias',
                'site_domain': 'prismaavaliacoes.com.br',
                'site_description': 'Avaliações imobiliárias profissionais e consultoria especializada',
                'default_keywords': 'avaliação imobiliária, laudo de avaliação, perícia imobiliária, consultoria imobiliária',
                'organization_name': 'Prisma Avaliações Imobiliárias',
            }
        )
        return config
    
    def get_full_domain(self, protocol='https'):
        """Retorna o domínio completo com protocolo"""
        return f'{protocol}://{self.site_domain}'
    
    def get_organization_schema(self):
        """Retorna o schema da organização em JSON-LD"""
        schema = {
            "@context": "https://schema.org",
            "@type": "RealEstateAgent",
            "name": self.organization_name,
            "url": self.get_full_domain(),
            "description": self.site_description,
        }
        
        if self.organization_logo:
            schema["logo"] = {
                "@type": "ImageObject",
                "url": f"{self.get_full_domain()}{self.organization_logo.url}"
            }
        
        if self.organization_phone:
            schema["telephone"] = self.organization_phone
        
        if self.organization_email:
            schema["email"] = self.organization_email
        
        if self.organization_address:
            schema["address"] = self.organization_address
        
        return mark_safe(f'<script type="application/ld+json">{json.dumps(schema, ensure_ascii=False, indent=2)}</script>')
