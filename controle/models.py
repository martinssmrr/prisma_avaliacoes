from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import User

class Cliente(models.Model):
    """Modelo para clientes da empresa"""
    
    # Campos obrigatórios
    nome = models.CharField(
        max_length=150,
        verbose_name="Nome Completo"
    )
    
    telefone = models.CharField(
        max_length=20,
        validators=[
            RegexValidator(
                regex=r'^\(\d{2}\)\s\d{4,5}-\d{4}$|^\d{10,11}$',
                message='Formato inválido. Use (xx) xxxxx-xxxx ou apenas números'
            )
        ],
        verbose_name="Telefone"
    )
    
    # Campos opcionais
    email = models.EmailField(
        blank=True,
        null=True,
        verbose_name="Email"
    )
    
    cidade = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Cidade"
    )
    
    ESTADOS_CHOICES = [
        ('AC', 'Acre'), ('AL', 'Alagoas'), ('AP', 'Amapá'), 
        ('AM', 'Amazonas'), ('BA', 'Bahia'), ('CE', 'Ceará'),
        ('DF', 'Distrito Federal'), ('ES', 'Espírito Santo'),
        ('GO', 'Goiás'), ('MA', 'Maranhão'), ('MT', 'Mato Grosso'),
        ('MS', 'Mato Grosso do Sul'), ('MG', 'Minas Gerais'),
        ('PA', 'Pará'), ('PB', 'Paraíba'), ('PR', 'Paraná'),
        ('PE', 'Pernambuco'), ('PI', 'Piauí'), ('RJ', 'Rio de Janeiro'),
        ('RN', 'Rio Grande do Norte'), ('RS', 'Rio Grande do Sul'),
        ('RO', 'Rondônia'), ('RR', 'Roraima'), ('SC', 'Santa Catarina'),
        ('SP', 'São Paulo'), ('SE', 'Sergipe'), ('TO', 'Tocantins')
    ]
    
    estado = models.CharField(
        max_length=2,
        choices=ESTADOS_CHOICES,
        blank=True,
        null=True,
        verbose_name="Estado"
    )
    
    # Metadados
    data_cadastro = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Data de Cadastro"
    )
    
    data_atualizacao = models.DateTimeField(
        auto_now=True,
        verbose_name="Última Atualização"
    )
    
    # Relacionamento com usuário Django para área do cliente
    usuario = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Usuário do Cliente",
        help_text="Usuário para acesso à área do cliente"
    )
    
    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        ordering = ['-data_cadastro']
    
    def __str__(self):
        return f"{self.nome} - {self.telefone}"


class Venda(models.Model):
    """Modelo para vendas com controle de etapas"""
    
    # Relacionamento
    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.CASCADE,
        related_name='vendas',
        verbose_name="Cliente"
    )
    
    # Etapas do processo
    orcamento = models.BooleanField(
        default=False,
        verbose_name="Orçamento"
    )
    
    venda = models.BooleanField(
        default=False,
        verbose_name="Venda Fechada"
    )
    
    documentacao = models.BooleanField(
        default=False,
        verbose_name="Documentação"
    )
    
    sinal_1 = models.BooleanField(
        default=False,
        verbose_name="1º Sinal (50%)"
    )
    
    confeccao = models.BooleanField(
        default=False,
        verbose_name="Confecção"
    )
    
    sinal_2 = models.BooleanField(
        default=False,
        verbose_name="2º Sinal"
    )
    
    envio = models.BooleanField(
        default=False,
        verbose_name="Envio"
    )
    
    # Campos adicionais
    valor_total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Valor Total (R$)"
    )
    
    observacoes = models.TextField(
        blank=True,
        null=True,
        verbose_name="Observações"
    )
    
    # Documento final para área do cliente
    documento_final = models.FileField(
        upload_to='documentos_finais/',
        blank=True,
        null=True,
        verbose_name="Documento Final",
        help_text="PDF/Laudo que será disponibilizado ao cliente após pagamento do 2º sinal"
    )
    
    # Controle de pagamentos
    segundo_sinal_pago = models.BooleanField(
        default=False,
        verbose_name="2º Sinal Pago",
        help_text="Marcar como pago quando cliente efetuar o pagamento do segundo sinal"
    )
    
    # Metadados
    data_criacao = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Data de Criação"
    )
    
    data_atualizacao = models.DateTimeField(
        auto_now=True,
        verbose_name="Última Atualização"
    )
    
    class Meta:
        verbose_name = "Venda"
        verbose_name_plural = "Vendas"
        ordering = ['-data_criacao']
    
    @property
    def status_geral(self):
        """Retorna o status geral da venda baseado nas etapas"""
        etapas = [
            self.orcamento,
            self.venda,
            self.documentacao,
            self.sinal_1,
            self.confeccao,
            self.sinal_2,
            self.envio
        ]
        
        if all(etapas):
            return "Concluída"
        elif not any(etapas):
            return "Iniciada"
        else:
            return "Em Andamento"
    
    @property
    def progresso_percentual(self):
        """Retorna o percentual de progresso da venda"""
        etapas = [
            self.orcamento,
            self.venda,
            self.documentacao,
            self.sinal_1,
            self.confeccao,
            self.sinal_2,
            self.envio
        ]
        
        concluidas = sum(etapas)
        total = len(etapas)
        
        return round((concluidas / total) * 100, 1)
    
    @property
    def proxima_etapa(self):
        """Retorna a próxima etapa a ser concluída"""
        etapas_nomes = [
            ('orcamento', 'Orçamento'),
            ('venda', 'Venda Fechada'),
            ('documentacao', 'Documentação'),
            ('sinal_1', '1º Sinal'),
            ('confeccao', 'Confecção'),
            ('sinal_2', '2º Sinal'),
            ('envio', 'Envio')
        ]
        
        for campo, nome in etapas_nomes:
            if not getattr(self, campo):
                return nome
        
        return "Todas as etapas concluídas"
    
    @property
    def pode_pagar_segundo_sinal(self):
        """Verifica se o cliente pode pagar o segundo sinal"""
        return self.confeccao and not self.segundo_sinal_pago
    
    @property
    def pode_baixar_documento(self):
        """Verifica se o cliente pode baixar o documento final"""
        return self.confeccao and self.segundo_sinal_pago and self.documento_final
    
    def __str__(self):
        return f"Venda #{self.id} - {self.cliente.nome} ({self.status_geral})"
