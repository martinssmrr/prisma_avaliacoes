"""
Models para o app de artigos/blog da Prisma Avaliações Imobiliárias
"""

from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils import timezone


class Artigo(models.Model):
    """
    Model para artigos do blog
    """
    
    # Campos principais
    titulo = models.CharField(
        max_length=200,
        verbose_name="Título",
        help_text="Título do artigo (máximo 200 caracteres)"
    )
    
    slug = models.SlugField(
        max_length=200,
        unique=True,
        blank=True,
        verbose_name="URL amigável",
        help_text="URL do artigo (gerada automaticamente a partir do título)"
    )
    
    autor = models.CharField(
        max_length=100,
        verbose_name="Autor",
        help_text="Nome do autor do artigo"
    )
    
    resumo = models.TextField(
        max_length=300,
        verbose_name="Resumo",
        help_text="Resumo do artigo para exibição na listagem (máximo 300 caracteres)"
    )
    
    conteudo = models.TextField(
        verbose_name="Conteúdo",
        help_text="Conteúdo completo do artigo"
    )
    
    imagem_destacada = models.ImageField(
        upload_to='artigos/imagens/',
        blank=True,
        null=True,
        verbose_name="Imagem destacada",
        help_text="Imagem principal do artigo (opcional)"
    )
    
    # Campos de controle
    publicado = models.BooleanField(
        default=False,
        verbose_name="Publicado",
        help_text="Marque para publicar o artigo"
    )
    
    data_criacao = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Data de criação"
    )
    
    data_publicacao = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name="Data de publicação",
        help_text="Data em que o artigo foi publicado"
    )
    
    data_atualizacao = models.DateTimeField(
        auto_now=True,
        verbose_name="Última atualização"
    )
    
    # Meta informações para SEO
    meta_description = models.CharField(
        max_length=160,
        blank=True,
        verbose_name="Meta descrição",
        help_text="Descrição para SEO (máximo 160 caracteres)"
    )
    
    meta_keywords = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Palavras-chave",
        help_text="Palavras-chave separadas por vírgula para SEO"
    )
    
    tags = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Tags",
        help_text="Tags separadas por vírgula (ex: avaliação, imóveis, mercado)"
    )
    
    canonical_url = models.URLField(
        blank=True,
        verbose_name="URL canônica",
        help_text="URL canônica se diferente da padrão (opcional)"
    )
    
    class Meta:
        verbose_name = "Artigo"
        verbose_name_plural = "Artigos"
        ordering = ['-data_publicacao', '-data_criacao']
        
    def __str__(self):
        return self.titulo
    
    def save(self, *args, **kwargs):
        """
        Sobrescreve o save para gerar o slug automaticamente
        e definir a data de publicação
        """
        if not self.slug:
            self.slug = slugify(self.titulo)
            
        # Se o artigo está sendo publicado pela primeira vez
        if self.publicado and not self.data_publicacao:
            self.data_publicacao = timezone.now()
            
        # Se o artigo foi despublicado, remove a data de publicação
        if not self.publicado:
            self.data_publicacao = None
            
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        """
        Retorna a URL absoluta do artigo
        """
        return reverse('artigos:detalhe', kwargs={'slug': self.slug})
    
    def get_resumo_truncado(self, palavras=30):
        """
        Retorna o resumo truncado em um número específico de palavras
        """
        palavras_resumo = self.resumo.split()
        if len(palavras_resumo) > palavras:
            return ' '.join(palavras_resumo[:palavras]) + '...'
        return self.resumo
    
    def get_tags_list(self):
        """
        Retorna as tags como uma lista
        """
        if self.tags:
            return [tag.strip() for tag in self.tags.split(',')]
        return []
    
    def get_tempo_leitura(self):
        """
        Estima o tempo de leitura baseado no conteúdo
        Média de 200 palavras por minuto
        """
        palavras = len(self.conteudo.split())
        minutos = max(1, round(palavras / 200))
        return f"{minutos} min de leitura"


class Categoria(models.Model):
    """
    Model para categorias dos artigos (para futuras expansões)
    """
    
    nome = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Nome"
    )
    
    slug = models.SlugField(
        max_length=100,
        unique=True,
        blank=True,
        verbose_name="URL amigável"
    )
    
    descricao = models.TextField(
        blank=True,
        verbose_name="Descrição"
    )
    
    ativa = models.BooleanField(
        default=True,
        verbose_name="Ativa"
    )
    
    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"
        ordering = ['nome']
        
    def __str__(self):
        return self.nome
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nome)
        super().save(*args, **kwargs)
