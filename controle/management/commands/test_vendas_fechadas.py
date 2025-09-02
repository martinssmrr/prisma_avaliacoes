from django.core.management.base import BaseCommand
from django.utils import timezone
from django.db.models import Sum
from controle.models import Venda

class Command(BaseCommand):
    help = 'Testa o cálculo de vendas fechadas vs todas as vendas'

    def handle(self, *args, **options):
        # Data atual
        hoje = timezone.now()
        mes_atual = hoje.month
        ano_atual = hoje.year
        
        # Todas as vendas do mês
        todas_vendas_mes = Venda.objects.filter(
            data_criacao__month=mes_atual,
            data_criacao__year=ano_atual
        )
        
        # Apenas vendas fechadas do mês
        vendas_fechadas_mes = Venda.objects.filter(
            data_criacao__month=mes_atual,
            data_criacao__year=ano_atual,
            venda=True  # Apenas vendas fechadas
        )
        
        # Cálculos
        total_todas_vendas = todas_vendas_mes.count()
        valor_todas_vendas = todas_vendas_mes.aggregate(total=Sum('valor_total'))['total'] or 0
        
        total_vendas_fechadas = vendas_fechadas_mes.count()
        valor_vendas_fechadas = vendas_fechadas_mes.aggregate(total=Sum('valor_total'))['total'] or 0
        
        self.stdout.write(self.style.SUCCESS(f'\n=== RELATÓRIO DE VENDAS - {mes_atual}/{ano_atual} ==='))
        
        self.stdout.write(f'\nTODAS AS VENDAS DO MÊS:')
        self.stdout.write(f'- Quantidade: {total_todas_vendas}')
        self.stdout.write(f'- Valor Total: R$ {valor_todas_vendas:,.2f}')
        
        self.stdout.write(f'\nVENDAS FECHADAS DO MÊS:')
        self.stdout.write(f'- Quantidade: {total_vendas_fechadas}')
        self.stdout.write(f'- Valor Total: R$ {valor_vendas_fechadas:,.2f}')
        
        diferenca_quantidade = total_todas_vendas - total_vendas_fechadas
        diferenca_valor = valor_todas_vendas - valor_vendas_fechadas
        
        self.stdout.write(f'\nDIFERENÇA (Em Processo):')
        self.stdout.write(f'- Quantidade: {diferenca_quantidade}')
        self.stdout.write(f'- Valor: R$ {diferenca_valor:,.2f}')
        
        self.stdout.write(self.style.WARNING(f'\n✅ DASHBOARD AGORA MOSTRA APENAS: {total_vendas_fechadas} vendas fechadas = R$ {valor_vendas_fechadas:,.2f}'))
        self.stdout.write(self.style.WARNING(f'🔄 NÃO CONTABILIZA: {diferenca_quantidade} vendas em processo = R$ {diferenca_valor:,.2f}'))
        
        # Lista as vendas em processo (não fechadas)
        if diferenca_quantidade > 0:
            self.stdout.write(f'\n--- VENDAS EM PROCESSO (não contabilizadas) ---')
            vendas_processo = todas_vendas_mes.filter(venda=False)
            for venda in vendas_processo:
                status = []
                if venda.orcamento:
                    status.append("Orçamento")
                if venda.documentacao:
                    status.append("Documentação")
                if venda.sinal_1:
                    status.append("Sinal 1")
                if venda.confeccao:
                    status.append("Confecção")
                if venda.sinal_2:
                    status.append("Sinal 2")
                if venda.envio:
                    status.append("Envio")
                
                status_text = " | ".join(status) if status else "Iniciada"
                self.stdout.write(f'• {venda.cliente.nome} - R$ {venda.valor_total:,.2f} - Status: {status_text}')
