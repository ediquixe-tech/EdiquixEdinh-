# Guia de Instalação - EdiquixEdinh-

## Instalação no Termux (Android)

### 1. Instalar Termux
- Baixe do F-Droid: https://f-droid.org/repo/com.termux_118.apk

### 2. Atualizar Termux
```bash
apt update && apt upgrade -y
```

### 3. Instalar Dependências
```bash
apt install python3 pip git libssl-dev libffi-dev -y
```

### 4. Clonar Repositório
```bash
git clone https://github.com/ediquixe-tech/EdiquixEdinh-.git
cd EdiquixEdinh-
```

### 5. Instalar Requirements
```bash
pip install -r requirements.txt
```

### 6. Executar Aplicação
```bash
python main.py
```

---

## Compilar como APK (Opcional)

### Requisitos:
- Linux/macOS com 20GB de espaço
- Python 3.8+
- Java JDK

### Passos:
```bash
pip install buildozer cython
cd EdiquixEdinh-
buildozer android debug
```

O APK será gerado em `bin/ediquixedinh-1.0-debug.apk`

---

## Uso das Ferramentas

### 🔍 SNI Scanner
- **Função**: Escaneia SNIs válidas com IP e porta
- **Input**: IP, Porta, Lista de SNIs
- **Output**: Certificados, Ciphers, SSL Version

### 💣 Payload Generator
- **Função**: Gera payloads para diversos ataques
- **Tipos**: Reverse Shell, SQL Injection, XSS, Password Lists

### 🔐 SSH Validator
- **Função**: Valida credenciais SSH
- **Recursos**: Brute Force, Banner Grabbing, Key Validation

### 🌐 Tunnel Configuration
- **Função**: Configura túneis SSH
- **Tipos**: Local (-L), Remote (-R), SOCKS5

---

## Troubleshooting

### Erro: ModuleNotFoundError
```bash
pip install --upgrade -r requirements.txt
```

### Erro de Conexão SSH
- Verifique IP/Porta do servidor
- Confirme credenciais
- Teste com: `ssh -vvv user@host`

### Interface Kivy não carrega
```bash
pip install kivy --upgrade
```

---

## Segurança

⚠️ **IMPORTANTE**: Use esta ferramenta apenas em ambientes autorizados!

- Obtenha permissão antes de qualquer teste
- Mantenha credenciais seguras
- Use VPN quando apropriado
- Respeite as leis locais

---

## Licença

MIT License - Veja LICENSE.md

---

**Desenvolvido por**: ediquixe-tech
**Versão**: 1.0
**Android Mínimo**: 14
