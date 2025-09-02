from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, Http404
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.cache import never_cache
from controle.models import Cliente, Venda
import os


@csrf_protect
@never_cache
def login_cliente(request):
    """View de login para clientes"""
    if request.method == 'POST':
        telefone_raw = request.POST.get('telefone')
        senha = request.POST.get('senha')
        
        # Limpar formatação do telefone (remover parênteses, espaços, hífens)
        telefone = ''.join(filter(str.isdigit, telefone_raw)) if telefone_raw else ''
        
        try:
            # Buscar cliente pelo telefone limpo
            cliente = Cliente.objects.get(telefone=telefone)
            
            if cliente.usuario:
                # Tentar autenticar com o usuário existente
                user = authenticate(request, username=cliente.usuario.username, password=senha)
                if user:
                    login(request, user)
                    messages.success(request, f'Bem-vindo, {cliente.nome}!')
                    return redirect('area_cliente:dashboard')
                else:
                    messages.error(request, 'Senha incorreta.')
            else:
                messages.error(request, 'Acesso não configurado. Entre em contato com o suporte.')
                
        except Cliente.DoesNotExist:
            messages.error(request, 'Cliente não encontrado. Verifique o telefone digitado.')
    
    return render(request, 'area_cliente/login.html')


def logout_cliente(request):
    """Logout do cliente"""
    logout(request)
    messages.success(request, 'Logout realizado com sucesso!')
    return redirect('area_cliente:login')


@login_required(login_url='area_cliente:login')
def dashboard(request):
    """Dashboard principal da área do cliente"""
    try:
        cliente = request.user.cliente
        vendas = cliente.vendas.all().order_by('-data_criacao')
        
        context = {
            'cliente': cliente,
            'vendas': vendas,
            'total_vendas': vendas.count(),
            'vendas_concluidas': vendas.filter(envio=True).count(),
            'vendas_andamento': vendas.exclude(envio=True).count(),
        }
        
        return render(request, 'area_cliente/dashboard.html', context)
        
    except Cliente.DoesNotExist:
        messages.error(request, 'Cliente não encontrado.')
        return redirect('area_cliente:login')


@login_required(login_url='area_cliente:login')
def minhas_compras(request):
    """Lista de compras/vendas do cliente"""
    try:
        cliente = request.user.cliente
        vendas = cliente.vendas.all().order_by('-data_criacao')
        
        context = {
            'cliente': cliente,
            'vendas': vendas,
        }
        
        return render(request, 'area_cliente/minhas_compras.html', context)
        
    except Cliente.DoesNotExist:
        messages.error(request, 'Cliente não encontrado.')
        return redirect('area_cliente:login')


@login_required(login_url='area_cliente:login')
def pagar_segundo_sinal(request, venda_id):
    """Simulação de pagamento do segundo sinal"""
    try:
        cliente = request.user.cliente
        venda = get_object_or_404(Venda, id=venda_id, cliente=cliente)
        
        if not venda.pode_pagar_segundo_sinal:
            messages.error(request, 'Pagamento do segundo sinal não disponível para esta venda.')
            return redirect('area_cliente:minhas_compras')
        
        if request.method == 'POST':
            # Simular pagamento (em produção, integrar com gateway real)
            venda.segundo_sinal_pago = True
            venda.save()
            
            messages.success(request, 'Pagamento do segundo sinal confirmado! Documento disponível para download.')
            return redirect('area_cliente:minhas_compras')
        
        context = {
            'cliente': cliente,
            'venda': venda,
        }
        
        return render(request, 'area_cliente/pagamento.html', context)
        
    except Cliente.DoesNotExist:
        messages.error(request, 'Cliente não encontrado.')
        return redirect('area_cliente:login')


@login_required(login_url='area_cliente:login')
def baixar_documento(request, venda_id):
    """Download do documento final"""
    try:
        cliente = request.user.cliente
        venda = get_object_or_404(Venda, id=venda_id, cliente=cliente)
        
        if not venda.pode_baixar_documento:
            messages.error(request, 'Documento não disponível para download.')
            return redirect('area_cliente:minhas_compras')
        
        # Verificar se arquivo existe
        if not venda.documento_final or not os.path.exists(venda.documento_final.path):
            messages.error(request, 'Documento não encontrado.')
            return redirect('area_cliente:minhas_compras')
        
        # Preparar download
        with open(venda.documento_final.path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/pdf")
            response['Content-Disposition'] = f'attachment; filename="Laudo_Venda_{venda.id}.pdf"'
            return response
            
    except Cliente.DoesNotExist:
        messages.error(request, 'Cliente não encontrado.')
        return redirect('area_cliente:login')


@login_required(login_url='area_cliente:login')
def trocar_senha(request):
    """Formulário para trocar senha"""
    try:
        cliente = request.user.cliente
        
        if request.method == 'POST':
            form = PasswordChangeForm(request.user, request.POST)
            if form.is_valid():
                user = form.save()
                update_session_auth_hash(request, user)  # Mantém o usuário logado
                messages.success(request, 'Senha alterada com sucesso!')
                return redirect('area_cliente:dashboard')
        else:
            form = PasswordChangeForm(request.user)
        
        context = {
            'cliente': cliente,
            'form': form,
        }
        
        return render(request, 'area_cliente/trocar_senha.html', context)
        
    except Cliente.DoesNotExist:
        messages.error(request, 'Cliente não encontrado.')
        return redirect('area_cliente:login')


@login_required(login_url='area_cliente:login')
def suporte(request):
    """Formulário de contato com suporte"""
    try:
        cliente = request.user.cliente
        
        if request.method == 'POST':
            assunto = request.POST.get('assunto')
            mensagem = request.POST.get('mensagem')
            
            if assunto and mensagem:
                # Preparar email
                corpo_email = f"""
                Solicitação de Suporte - Área do Cliente
                
                Cliente: {cliente.nome}
                Telefone: {cliente.telefone}
                Email: {cliente.email or 'Não informado'}
                
                Assunto: {assunto}
                
                Mensagem:
                {mensagem}
                
                ---
                Enviado através da Área do Cliente
                """
                
                try:
                    # Enviar email (configurar SMTP no settings.py)
                    send_mail(
                        subject=f'Suporte - {assunto}',
                        message=corpo_email,
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=['suporte@prismaav.com.br'],  # Alterar para email real
                        fail_silently=False,
                    )
                    
                    messages.success(request, 'Mensagem enviada com sucesso! Entraremos em contato em breve.')
                    return redirect('area_cliente:suporte')
                    
                except Exception as e:
                    messages.error(request, 'Erro ao enviar mensagem. Tente novamente mais tarde.')
            else:
                messages.error(request, 'Preencha todos os campos obrigatórios.')
        
        context = {
            'cliente': cliente,
        }
        
        return render(request, 'area_cliente/suporte.html', context)
        
    except Cliente.DoesNotExist:
        messages.error(request, 'Cliente não encontrado.')
        return redirect('area_cliente:login')
