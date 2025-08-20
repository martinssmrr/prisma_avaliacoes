/**
 * Prisma Avaliações Imobiliárias - JavaScript Principal
 * Funcionalidades interativas da landing page
 */

document.addEventListener('DOMContentLoaded', function() {
    
    // ========================================================================
    // Configurações e variáveis globais
    // ========================================================================
    
    const navbar = document.querySelector('.navbar');
    const scrollToTopBtn = createScrollToTopButton();
    
    // ========================================================================
    // Funcionalidades do Navbar
    // ========================================================================
    
    function handleNavbarScroll() {
        if (window.scrollY > 100) {
            navbar.classList.add('scrolled');
            scrollToTopBtn.classList.add('visible');
        } else {
            navbar.classList.remove('scrolled');
            scrollToTopBtn.classList.remove('visible');
        }
    }
    
    // ========================================================================
    // Criação do botão "Voltar ao topo"
    // ========================================================================
    
    function createScrollToTopButton() {
        const button = document.createElement('button');
        button.className = 'scroll-to-top';
        button.innerHTML = '<i class="fas fa-chevron-up"></i>';
        button.setAttribute('aria-label', 'Voltar ao topo');
        
        button.addEventListener('click', function() {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });
        
        document.body.appendChild(button);
        return button;
    }
    
    // ========================================================================
    // Scroll suave para links internos
    // ========================================================================
    
    function setupSmoothScrolling() {
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function(e) {
                e.preventDefault();
                
                const targetId = this.getAttribute('href').substring(1);
                const targetElement = document.getElementById(targetId);
                
                if (targetElement) {
                    const navbarHeight = navbar.offsetHeight;
                    const targetPosition = targetElement.offsetTop - navbarHeight - 20;
                    
                    window.scrollTo({
                        top: targetPosition,
                        behavior: 'smooth'
                    });
                }
            });
        });
    }
    
    // ========================================================================
    // Animações de entrada
    // ========================================================================
    
    function setupAnimations() {
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };
        
        const observer = new IntersectionObserver(function(entries) {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('animate-in');
                    observer.unobserve(entry.target); // Para de observar após animar
                }
            });
        }, observerOptions);
        
        // Observa elementos para animação
        document.querySelectorAll('.card, .contact-item, .stat-item').forEach(el => {
            observer.observe(el);
        });
    }
    
    // ========================================================================
    // Validação e envio do formulário
    // ========================================================================
    
    function setupContactForm() {
        const form = document.getElementById('contactForm');
        if (!form) return;
        
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Validação dos campos
            if (!validateForm()) {
                return;
            }
            
            // Mostra estado de carregamento
            showFormLoading(true);
            
            // Coleta dados do formulário
            const formData = collectFormData();
            
            // Simula um pequeno delay para UX
            setTimeout(() => {
                sendToWhatsApp(formData);
                showFormLoading(false);
            }, 1000);
        });
    }
    
    function validateForm() {
        const requiredFields = ['nome', 'telefone', 'email', 'tipo_imovel', 'mensagem'];
        let isValid = true;
        
        requiredFields.forEach(fieldName => {
            const field = document.getElementById(fieldName);
            const value = field.value.trim();
            
            // Remove classes de erro anteriores
            field.classList.remove('is-invalid');
            
            if (!value) {
                field.classList.add('is-invalid');
                isValid = false;
            }
        });
        
        // Validação específica do email
        const emailField = document.getElementById('email');
        const emailValue = emailField.value.trim();
        if (emailValue && !isValidEmail(emailValue)) {
            emailField.classList.add('is-invalid');
            isValid = false;
        }
        
        if (!isValid) {
            showAlert('Por favor, preencha todos os campos obrigatórios corretamente.', 'warning');
        }
        
        return isValid;
    }
    
    function isValidEmail(email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    }
    
    function collectFormData() {
        return {
            nome: document.getElementById('nome').value.trim(),
            telefone: document.getElementById('telefone').value.trim(),
            email: document.getElementById('email').value.trim(),
            tipoImovel: document.getElementById('tipo_imovel').value,
            mensagem: document.getElementById('mensagem').value.trim()
        };
    }
    
    function sendToWhatsApp(data) {
        const message = `
*Solicitação de Avaliação Imobiliária*

*Dados do Cliente:*
• Nome: ${data.nome}
• Telefone: ${data.telefone}
• E-mail: ${data.email}
• Tipo de Imóvel: ${data.tipoImovel}

*Mensagem:*
${data.mensagem}

_Enviado através do site da Prisma Avaliações Imobiliárias_
        `.trim();
        
        const encodedMessage = encodeURIComponent(message);
        const whatsappURL = `https://wa.me/5577999515837?text=${encodedMessage}`;
        
        // Abre o WhatsApp
        window.open(whatsappURL, '_blank');
        
        // Mostra mensagem de sucesso
        showAlert('Redirecionando para o WhatsApp...', 'success');
        
        // Limpa o formulário após envio
        setTimeout(() => {
            document.getElementById('contactForm').reset();
        }, 1500);
    }
    
    function showFormLoading(loading) {
        const form = document.getElementById('contactForm');
        const submitBtn = form.querySelector('button[type="submit"]');
        
        if (loading) {
            form.classList.add('form-loading');
            submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Enviando...';
        } else {
            form.classList.remove('form-loading');
            submitBtn.innerHTML = '<i class="fab fa-whatsapp me-2"></i>Enviar via WhatsApp';
        }
    }
    
    // ========================================================================
    // Sistema de alertas
    // ========================================================================
    
    function showAlert(message, type = 'info') {
        // Remove alertas existentes
        const existingAlert = document.querySelector('.custom-alert');
        if (existingAlert) {
            existingAlert.remove();
        }
        
        // Cria novo alerta
        const alert = document.createElement('div');
        alert.className = `alert alert-${type} custom-alert position-fixed`;
        alert.style.cssText = `
            top: 100px;
            right: 20px;
            z-index: 9999;
            min-width: 300px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        `;
        alert.innerHTML = `
            <div class="d-flex align-items-center">
                <i class="fas fa-${type === 'success' ? 'check-circle' : type === 'warning' ? 'exclamation-triangle' : 'info-circle'} me-2"></i>
                <span>${message}</span>
                <button type="button" class="btn-close ms-auto" onclick="this.parentElement.parentElement.remove()"></button>
            </div>
        `;
        
        document.body.appendChild(alert);
        
        // Remove automaticamente após 5 segundos
        setTimeout(() => {
            if (alert.parentElement) {
                alert.remove();
            }
        }, 5000);
    }
    
    // ========================================================================
    // Funcionalidades adicionais
    // ========================================================================
    
    function setupPhoneMask() {
        const phoneField = document.getElementById('telefone');
        if (phoneField) {
            phoneField.addEventListener('input', function(e) {
                let value = e.target.value.replace(/\D/g, '');
                
                if (value.length >= 11) {
                    value = value.replace(/(\d{2})(\d{5})(\d{4})/, '($1) $2-$3');
                } else if (value.length >= 6) {
                    value = value.replace(/(\d{2})(\d{4})(\d{0,4})/, '($1) $2-$3');
                } else if (value.length >= 2) {
                    value = value.replace(/(\d{2})(\d{0,5})/, '($1) $2');
                }
                
                e.target.value = value;
            });
        }
    }
    
    function setupTooltips() {
        // Inicializa tooltips do Bootstrap se disponível
        if (typeof bootstrap !== 'undefined') {
            const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
            tooltipTriggerList.map(function(tooltipTriggerEl) {
                return new bootstrap.Tooltip(tooltipTriggerEl);
            });
        }
    }
    
    // ========================================================================
    // Performance e otimizações
    // ========================================================================
    
    function debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }
    
    function throttle(func, limit) {
        let inThrottle;
        return function() {
            const args = arguments;
            const context = this;
            if (!inThrottle) {
                func.apply(context, args);
                inThrottle = true;
                setTimeout(() => inThrottle = false, limit);
            }
        };
    }
    
    // ========================================================================
    // Inicialização
    // ========================================================================
    
    function initialize() {
        setupSmoothScrolling();
        setupAnimations();
        setupContactForm();
        setupPhoneMask();
        setupTooltips();
        
        // Event listeners otimizados
        window.addEventListener('scroll', throttle(handleNavbarScroll, 100));
        
        // Event listener para fechar navbar mobile ao clicar em link
        document.querySelectorAll('.navbar-nav .nav-link').forEach(link => {
            link.addEventListener('click', () => {
                const navbarCollapse = document.querySelector('.navbar-collapse');
                if (navbarCollapse.classList.contains('show')) {
                    const navbarToggler = document.querySelector('.navbar-toggler');
                    navbarToggler.click();
                }
            });
        });
        
        // Chama função inicial do scroll
        handleNavbarScroll();
        
        console.log('Prisma Avaliações - JavaScript carregado com sucesso!');
    }
    
    // Inicializa quando o DOM estiver pronto
    initialize();
});

// ========================================================================
// Funcionalidades globais (disponíveis fora do DOMContentLoaded)
// ========================================================================

// Função para abrir WhatsApp diretamente
function openWhatsApp(message = '') {
    const defaultMessage = 'Olá! Gostaria de saber mais sobre os serviços de avaliação imobiliária.';
    const finalMessage = message || defaultMessage;
    const encodedMessage = encodeURIComponent(finalMessage);
    const whatsappURL = `https://wa.me/5577999515837?text=${encodedMessage}`;
    window.open(whatsappURL, '_blank');
}

// Função para compartilhar a página
function sharePage() {
    if (navigator.share) {
        navigator.share({
            title: 'Prisma Avaliações Imobiliárias',
            text: 'Avaliações imobiliárias com precisão e confiança',
            url: window.location.href
        });
    } else {
        // Fallback para navegadores que não suportam Web Share API
        const url = window.location.href;
        navigator.clipboard.writeText(url).then(() => {
            alert('Link copiado para a área de transferência!');
        });
    }
}
