from django.contrib import admin
from django.db.models import Count, Q
from django.utils.html import format_html
from django.urls import path, reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from .models import Cliente, Venda
import re


class StatusVendaFilter(admin.SimpleListFilter):
    """Filtro personalizado para status da venda"""
    title = 'Status da Venda'
    parameter_name = 'status'
    
    def lookups(self, request, model_admin):
        return (
            ('iniciada', 'Iniciada'),
            ('andamento', 'Em Andamento'),
            ('concluida', 'Concluída'),
        )
    
    def queryset(self, request, queryset):
        if self.value() == 'iniciada':
            return queryset.filter(
                orcamento=False, venda=False, documentacao=False,
                sinal_1=False, confeccao=False, sinal_2=False, envio=False
            )
        elif self.value() == 'andamento':
            return queryset.filter(
                Q(orcamento=True) | Q(venda=True) | Q(documentacao=True) | 
                Q(sinal_1=True) | Q(confeccao=True) | Q(sinal_2=True)
            ).exclude(envio=True)
        elif self.value() == 'concluida':
            return queryset.filter(envio=True)
        return queryset


class VendaInline(admin.TabularInline):
    """Inline para vendas no admin de clientes"""
    model = Venda
    extra = 0
    readonly_fields = ('status_geral', 'progresso_percentual', 'data_criacao')
    fields = ('status_geral', 'progresso_percentual', 'valor_total', 'data_criacao')
    
    def status_geral(self, obj):
        if obj.id:
            status = obj.status_geral
            cores = {
                'Iniciada': '#F59E0B',  # Amarelo
                'Em Andamento': '#3B82F6',  # Azul
                'Concluída': '#10B981'  # Verde
            }
            cor = cores.get(status, '#6B7280')
            return format_html(
                '<span style="background-color: {}; color: white; padding: 4px 8px; border-radius: 4px; font-size: 12px;">{}</span>',
                cor, status
            )
        return "-"
    status_geral.short_description = "Status"


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'telefone', 'email', 'cidade', 'estado', 'usuario_status', 'total_vendas', 'data_cadastro')
    list_filter = ('estado', 'data_cadastro')
    search_fields = ('nome', 'telefone', 'email', 'cidade')
    ordering = ('-data_cadastro',)
    readonly_fields = ('data_cadastro', 'data_atualizacao')
    inlines = [VendaInline]
    actions = ['criar_usuario_cliente']
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('nome', 'telefone')
        }),
        ('Informações Opcionais', {
            'fields': ('email', 'cidade', 'estado'),
            'classes': ('collapse',)
        }),
        ('Área do Cliente', {
            'fields': ('usuario',),
            'classes': ('collapse',),
            'description': 'Usuário para acesso à área do cliente'
        }),
        ('Metadados', {
            'fields': ('data_cadastro', 'data_atualizacao'),
            'classes': ('collapse',)
        })
    )
    
    def usuario_status(self, obj):
        if obj.usuario:
            return format_html(
                '<span style="background-color: #10B981; color: white; padding: 2px 6px; border-radius: 3px;">✓ Ativo</span>'
            )
        else:
            return format_html(
                '<span style="background-color: #EF4444; color: white; padding: 2px 6px; border-radius: 3px;">✗ Não criado</span>'
            )
    usuario_status.short_description = "Acesso"
    
    def total_vendas(self, obj):
        count = obj.vendas.count()
        if count > 0:
            return format_html(
                '<span style="background-color: #1E3A8A; color: white; padding: 2px 6px; border-radius: 3px;">{}</span>',
                count
            )
        return "0"
    total_vendas.short_description = "Vendas"
    
    def criar_usuario_cliente(self, request, queryset):
        """Criar usuários para clientes selecionados"""
        created_count = 0
        
        for cliente in queryset:
            if not cliente.usuario:
                # Extrair apenas números do telefone
                telefone_numeros = re.sub(r'\D', '', cliente.telefone)
                
                if len(telefone_numeros) >= 4:
                    # Criar username único baseado no telefone
                    username = telefone_numeros
                    counter = 1
                    while User.objects.filter(username=username).exists():
                        username = f"{telefone_numeros}_{counter}"
                        counter += 1
                    
                    # Senha padrão: últimos 4 dígitos do telefone
                    senha_padrao = telefone_numeros[-4:]
                    
                    # Criar usuário
                    user = User.objects.create_user(
                        username=username,
                        email=cliente.email or '',
                        password=senha_padrao,
                        first_name=cliente.nome.split()[0] if cliente.nome else '',
                        last_name=' '.join(cliente.nome.split()[1:]) if len(cliente.nome.split()) > 1 else ''
                    )
                    
                    # Associar ao cliente
                    cliente.usuario = user
                    cliente.save()
                    
                    created_count += 1
        
        if created_count > 0:
            self.message_user(
                request,
                f'{created_count} usuário(s) criado(s) com sucesso! Senhas padrão: últimos 4 dígitos do telefone.',
                messages.SUCCESS
            )
        else:
            self.message_user(
                request,
                'Nenhum usuário foi criado. Clientes já possuem usuários ou telefones inválidos.',
                messages.WARNING
            )
    
    criar_usuario_cliente.short_description = "Criar usuário para área do cliente"


@admin.register(Venda)
class VendaAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'cliente', 'status_badge', 'progresso_bar', 
        'valor_total', 'proxima_etapa_display', 'data_criacao', 'acoes'
    )
    list_filter = ('data_criacao', StatusVendaFilter)
    search_fields = ('cliente__nome', 'cliente__telefone', 'id')
    ordering = ('-data_criacao',)
    readonly_fields = ('data_criacao', 'data_atualizacao', 'status_geral', 'progresso_percentual')
    
    fieldsets = (
        ('Cliente', {
            'fields': ('cliente',)
        }),
        ('Etapas do Processo', {
            'fields': (
                ('orcamento', 'venda'),
                ('documentacao', 'sinal_1'),
                ('confeccao', 'sinal_2'),
                ('envio',)
            ),
            'classes': ('wide',)
        }),
        ('Informações Financeiras', {
            'fields': ('valor_total',),
        }),
        ('Área do Cliente', {
            'fields': ('documento_final', 'segundo_sinal_pago'),
            'classes': ('wide',),
            'description': 'Documentos e pagamentos para área do cliente'
        }),
        ('Observações', {
            'fields': ('observacoes',),
            'classes': ('collapse',)
        }),
        ('Status e Progresso', {
            'fields': ('status_geral', 'progresso_percentual'),
            'classes': ('collapse',)
        }),
        ('Metadados', {
            'fields': ('data_criacao', 'data_atualizacao'),
            'classes': ('collapse',)
        })
    )
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('dashboard/', self.admin_site.admin_view(self.dashboard_view), name='controle_dashboard'),
            path('<int:venda_id>/avancar/', self.admin_site.admin_view(self.avancar_etapa), name='controle_venda_avancar'),
        ]
        return custom_urls + urls
    
    def dashboard_view(self, request):
        """View personalizada para dashboard"""
        from django.utils import timezone
        from django.db.models import Sum
        
        # Data atual
        hoje = timezone.now()
        mes_atual = hoje.month
        ano_atual = hoje.year
        
        # Nomes dos meses em português
        meses_pt = {
            1: 'Janeiro', 2: 'Fevereiro', 3: 'Março', 4: 'Abril',
            5: 'Maio', 6: 'Junho', 7: 'Julho', 8: 'Agosto',
            9: 'Setembro', 10: 'Outubro', 11: 'Novembro', 12: 'Dezembro'
        }
        
        # Estatísticas gerais
        total_clientes = Cliente.objects.count()
        total_vendas = Venda.objects.count()
        vendas_em_andamento = Venda.objects.filter(
            Q(orcamento=True) | Q(venda=True) | Q(documentacao=True) | 
            Q(sinal_1=True) | Q(confeccao=True) | Q(sinal_2=True)
        ).exclude(envio=True).count()
        vendas_concluidas = Venda.objects.filter(envio=True).count()
        
        # Estatísticas do mês atual - APENAS VENDAS FECHADAS
        vendas_mes_fechadas = Venda.objects.filter(
            data_criacao__month=mes_atual,
            data_criacao__year=ano_atual,
            venda=True  # Apenas vendas fechadas são contabilizadas
        )
        total_vendas_mes = vendas_mes_fechadas.count()
        valor_total_mes = vendas_mes_fechadas.aggregate(
            total=Sum('valor_total')
        )['total'] or 0
        
        # Vendas recentes
        vendas_recentes = Venda.objects.select_related('cliente').order_by('-data_criacao')[:10]
        
        context = {
            'title': 'Dashboard de Vendas',
            'total_clientes': total_clientes,
            'total_vendas': total_vendas,
            'vendas_em_andamento': vendas_em_andamento,
            'vendas_concluidas': vendas_concluidas,
            'vendas_recentes': vendas_recentes,
            'total_vendas_mes': total_vendas_mes,
            'valor_total_mes': valor_total_mes,
            'mes_nome': meses_pt[mes_atual],
            'ano_atual': ano_atual,
        }
        
        return render(request, 'admin/controle/dashboard.html', context)
    
    def avancar_etapa(self, request, venda_id):
        """Avança para a próxima etapa da venda"""
        venda = get_object_or_404(Venda, id=venda_id)
        
        # Determinar próxima etapa
        etapas = ['orcamento', 'venda', 'documentacao', 'sinal_1', 'confeccao', 'sinal_2', 'envio']
        
        for etapa in etapas:
            if not getattr(venda, etapa):
                setattr(venda, etapa, True)
                venda.save()
                messages.success(request, f'Etapa "{venda._meta.get_field(etapa).verbose_name}" marcada como concluída!')
                break
        else:
            messages.info(request, 'Todas as etapas já foram concluídas!')
        
        return HttpResponseRedirect(reverse('admin:controle_venda_changelist'))
    
    def status_badge(self, obj):
        status = obj.status_geral
        cores = {
            'Iniciada': '#F59E0B',  # Amarelo
            'Em Andamento': '#3B82F6',  # Azul
            'Concluída': '#10B981'  # Verde
        }
        cor = cores.get(status, '#6B7280')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 4px 8px; border-radius: 4px; font-size: 12px; font-weight: bold;">{}</span>',
            cor, status
        )
    status_badge.short_description = "Status"
    
    def progresso_bar(self, obj):
        percentual = obj.progresso_percentual
        cor = '#10B981' if percentual == 100 else '#3B82F6' if percentual > 50 else '#F59E0B'
        
        return format_html(
            '''
            <div style="width: 100px; background-color: #E5E7EB; border-radius: 4px; overflow: hidden;">
                <div style="width: {}%; height: 20px; background-color: {}; display: flex; align-items: center; justify-content: center; color: white; font-size: 11px; font-weight: bold;">
                    {}%
                </div>
            </div>
            ''',
            percentual, cor, percentual
        )
    progresso_bar.short_description = "Progresso"
    
    def proxima_etapa_display(self, obj):
        proxima = obj.proxima_etapa
        if proxima == "Todas as etapas concluídas":
            return format_html('<span style="color: #10B981; font-weight: bold;">✓ Concluída</span>')
        else:
            return format_html('<span style="color: #F97316; font-weight: bold;">⏱ {}</span>', proxima)
    proxima_etapa_display.short_description = "Próxima Etapa"
    
    def acoes(self, obj):
        if obj.proxima_etapa != "Todas as etapas concluídas":
            url = reverse('admin:controle_venda_avancar', args=[obj.id])
            return format_html(
                '<a href="{}" style="background-color: #F97316; color: white; padding: 4px 8px; text-decoration: none; border-radius: 4px; font-size: 12px;">Avançar</a>',
                url
            )
        return "✓ Finalizada"
    acoes.short_description = "Ações"


# Personalização do admin site
admin.site.site_header = "Prisma Avaliações - Dashboard"
admin.site.site_title = "Dashboard Prisma"
admin.site.index_title = "Painel de Controle"
