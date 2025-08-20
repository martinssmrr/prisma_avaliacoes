# Guia de Personalização Visual - Prisma Avaliações

## 🎨 Opções de Design para a Seção Hero

### 1. Gradiente (Design Original)
```html
<section id="inicio" class="hero-section bg-gradient-primary text-white py-5">
```

### 2. Imagem de Fundo Expandida (Atual)
```html
<section id="inicio" class="hero-section hero-with-image text-white py-5" style="background-image: url('/media/home2.jpg');">
```

### 3. Imagem na Coluna (Design Intermediário)
```html
<div class="hero-image-container rounded-3 overflow-hidden shadow-lg">
    <img src="/media/home2.jpg" alt="Avaliações Profissionais">
</div>
```

## 🖼️ Como Trocar Imagens

1. **Adicionar nova imagem**: Coloque o arquivo na pasta `media/`
2. **Atualizar template**: Edite `templates/Prisma_avaliacoes/home.html`
3. **Alterar caminho**: Mude `url('/media/NOVA-IMAGEM.jpg')`

## 🎨 Personalizar Cores

### Arquivo: `static/css/style.css`
```css
:root {
    --primary-color: #1e40af;     /* Azul principal */
    --secondary-color: #0f172a;   /* Azul escuro */
    --accent-color: #3b82f6;      /* Azul claro */
}
```

## 📱 Responsividade

- **Mobile**: `background-attachment: scroll` (melhor performance)
- **Desktop**: `background-attachment: fixed` (efeito parallax)

## 🎯 Overlay de Texto

### Opacidade do Overlay
```css
.hero-overlay {
    background: linear-gradient(
        135deg, 
        rgba(30, 64, 175, 0.85) 0%,  /* Ajustar opacidade aqui */
        rgba(59, 130, 246, 0.75) 50%,
        rgba(15, 23, 42, 0.85) 100%
    );
}
```

### Card de Destaque
```css
.hero-content-overlay {
    background: rgba(255, 255, 255, 0.10);  /* Ajustar transparência */
    backdrop-filter: blur(10px);             /* Efeito de desfoque */
}
```

## 🚀 Dicas de Performance

1. **Otimizar imagens**: Use formatos WebP quando possível
2. **Tamanho ideal**: 1920x1080 ou similar para full HD
3. **Compressão**: Mantenha abaixo de 500KB para carregamento rápido
4. **Mobile**: Use `background-attachment: scroll` em telas pequenas
