"""
Configuração do Django Admin para o app de artigos
"""

from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils import timezone
from .models import Artigo, Categoria


@admin.register(Artigo)
class ArtigoAdmin(admin.ModelAdmin):
    """
    Configuração do admin para model Artigo
    """
    
    # Campos exibidos na listagem
    list_display = [
        'titulo',
        'autor',
        'status_publicacao',
        'data_publicacao',
        'visualizar_site',
        'data_criacao'
    ]
    
    # Filtros laterais
    list_filter = [
        'publicado',
        'data_criacao',
        'data_publicacao',
        'autor'
    ]
    
    # Campos de busca
    search_fields = [
        'titulo',
        'resumo',
        'conteudo',
        'tags'
    ]
    
    # Campos ordenáveis
    ordering = ['-data_criacao']
    
    # Campos editáveis na listagem
    # list_editable = ['publicado']  # Removido pois publicado não está em list_display
    
    # Número de itens por página
    list_per_page = 20
    
    # Campos no formulário de criação/edição
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('titulo', 'slug', 'autor', 'resumo')
        }),
        ('Conteúdo', {
            'fields': ('conteudo', 'imagem_destacada')
        }),
        ('Publicação', {
            'fields': ('publicado', 'data_publicacao'),
            'description': 'Controle de publicação do artigo'
        }),
        ('SEO e Organização', {
            'fields': ('meta_description', 'tags'),
            'classes': ('collapse',),
            'description': 'Informações para otimização e organização'
        }),
    )
    
    # Campos somente leitura
    readonly_fields = ['data_criacao', 'data_atualizacao']
    
    # Preenchimento automático do slug
    prepopulated_fields = {'slug': ('titulo',)}
    
    # Ações personalizadas
    actions = ['publicar_artigos', 'despublicar_artigos']
    
    def status_publicacao(self, obj):
        """
        Exibe o status de publicação com cores
        """
        if obj.publicado:
            return format_html(
                '<span style="color: green; font-weight: bold;">✓ Publicado</span>'
            )
        else:
            return format_html(
                '<span style="color: red; font-weight: bold;">✗ Rascunho</span>'
            )
    status_publicacao.short_description = 'Status'
    
    def visualizar_site(self, obj):
        """
        Link para visualizar o artigo no site
        """
        if obj.publicado and obj.slug:
            url = reverse('artigos:detalhe', kwargs={'slug': obj.slug})
            return format_html(
                '<a href="{}" target="_blank" style="color: #007cba;">Ver no site</a>',
                url
            )
        return '-'
    visualizar_site.short_description = 'Visualizar'
    
    def publicar_artigos(self, request, queryset):
        """
        Ação para publicar artigos selecionados
        """
        count = 0
        for artigo in queryset:
            if not artigo.publicado:
                artigo.publicado = True
                artigo.data_publicacao = timezone.now()
                artigo.save()
                count += 1
        
        self.message_user(
            request,
            f'{count} artigo(s) publicado(s) com sucesso.'
        )
    publicar_artigos.short_description = 'Publicar artigos selecionados'
    
    def despublicar_artigos(self, request, queryset):
        """
        Ação para despublicar artigos selecionados
        """
        count = queryset.filter(publicado=True).update(
            publicado=False,
            data_publicacao=None
        )
        
        self.message_user(
            request,
            f'{count} artigo(s) despublicado(s) com sucesso.'
        )
    despublicar_artigos.short_description = 'Despublicar artigos selecionados'
    
    def get_form(self, request, obj=None, **kwargs):
        """
        Personaliza o formulário baseado no usuário
        """
        form = super().get_form(request, obj, **kwargs)
        
        # Define um autor padrão para novos artigos se desejar
        if not obj and 'autor' in form.base_fields:
            form.base_fields['autor'].initial = request.user.get_full_name() or request.user.username
            
        return form
    
    def save_model(self, request, obj, form, change):
        """
        Personaliza o salvamento do modelo
        """
        # Se não há autor definido, usa o nome do usuário atual
        if not obj.autor and not change:  # Novo artigo sem autor
            obj.autor = request.user.get_full_name() or request.user.username
            
        super().save_model(request, obj, form, change)


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    """
    Configuração do admin para model Categoria
    """
    
    list_display = ['nome', 'slug', 'ativa', 'numero_artigos']
    list_filter = ['ativa']
    search_fields = ['nome', 'descricao']
    ordering = ['nome']
    list_editable = ['ativa']
    prepopulated_fields = {'slug': ('nome',)}
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('nome', 'slug', 'descricao')
        }),
        ('Configurações', {
            'fields': ('ativa',)
        }),
    )
    
    def numero_artigos(self, obj):
        """
        Conta o número de artigos publicados na categoria
        """
        # Para futuras implementações quando adicionarmos ForeignKey
        return 0
    numero_artigos.short_description = 'Artigos'


# Personalização do admin site
admin.site.site_header = "Prisma Avaliações - Administração"
admin.site.site_title = "Prisma Admin"
admin.site.index_title = "Painel de Controle"
