# 📁 TRANSFERIR ARQUIVOS PARA VPS - WINDOWS

## 🚀 **OPÇÃO 1: WinSCP (Recomendado para Windows)**

### Baixar e Instalar WinSCP:
1. Acesse: https://winscp.net/eng/download.php
2. Baixe e instale o WinSCP
3. Configure a conexão:
   - **Protocolo**: SFTP
   - **Host**: 72.60.144.18
   - **Usuário**: root
   - **Senha**: [sua senha do VPS]

### Transferir Arquivos:
1. Conecte no VPS
2. Navegue até `/var/www/`
3. Arraste a pasta `Prisma Avaliações Imobiliarias` para o VPS
4. Renomeie para `Prisma_Avaliacoes` (sem espaços)

---

## 🚀 **OPÇÃO 2: PowerShell com pscp (PuTTY)**

### Instalar PuTTY:
```powershell
winget install PuTTY.PuTTY
```

### Transferir arquivos:
```powershell
cd "C:\Users\teste\OneDrive\Desktop"
pscp -r "Prisma Avaliações Imobiliarias" root@72.60.144.18:/var/www/Prisma_Avaliacoes
```

---

## 🚀 **OPÇÃO 3: Compactar e usar wget/curl**

### 1. Compactar projeto:
```powershell
Compress-Archive -Path "C:\Users\teste\OneDrive\Desktop\Prisma Avaliações Imobiliarias" -DestinationPath "C:\Users\teste\OneDrive\Desktop\prisma_projeto.zip"
```

### 2. Hospedar temporariamente (Google Drive, Dropbox, etc.)

### 3. No VPS baixar:
```bash
cd /var/www/
wget "LINK_DO_ARQUIVO_ZIP"
unzip prisma_projeto.zip
mv "Prisma Avaliações Imobiliarias" Prisma_Avaliacoes
```

---

## 🚀 **OPÇÃO 4: Git (Se já estiver no GitHub)**

### No VPS:
```bash
cd /var/www/
git clone https://github.com/SEU_USUARIO/prisma_avaliacoes.git Prisma_Avaliacoes
```

---

## 🚀 **OPÇÃO 5: PowerShell nativo (Windows 10+)**

### Ativar OpenSSH:
```powershell
# Executar como Administrador
Add-WindowsCapability -Online -Name OpenSSH.Client~~~~0.0.1.0
```

### Depois usar scp:
```powershell
scp -r "Prisma Avaliações Imobiliarias" root@72.60.144.18:/var/www/Prisma_Avaliacoes
```
