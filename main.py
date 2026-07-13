#!/usr/bin/env python3
"""
EdiquixEdinh- CLI
Interface de linha de comando para Termux
"""

import sys
import os
from modules.sni_scanner import SNIScanner
from modules.payload_generator import PayloadGenerator
from modules.ssh_validator import SSHValidator
from modules.tunnel_config import TunnelConfig


def print_banner():
    """Exibe banner da aplicação"""
    banner = """
╔═══════════════════════════════════════╗
║   EdiquixEdinh- v1.0                  ║
║   Network Security Toolkit            ║
║   For Educational & Authorized Use    ║
╚═══════════════════════════════════════╝
    """
    print(banner)


def print_menu():
    """Exibe menu principal"""
    print("\n" + "="*40)
    print("MENU PRINCIPAL")
    print("="*40)
    print("1. 📡 SNI Scanner")
    print("2. 💣 Payload Generator")
    print("3. 🔐 SSH Validator")
    print("4. 🌐 Tunnel Configuration")
    print("5. ❌ Sair")
    print("="*40)


def sni_scanner_menu():
    """Menu do SNI Scanner"""
    print("\n" + "="*40)
    print("SNI SCANNER")
    print("="*40)
    
    host = input("Host/IP: ").strip()
    port = int(input("Porta (ex: 443): ").strip())
    sni_input = input("SNIs (separadas por vírgula): ").strip()
    sni_list = [s.strip() for s in sni_input.split(',')]
    
    print("\n[*] Escaneando...")
    scanner = SNIScanner()
    result = scanner.scan_sni(host, port, sni_list)
    
    print("\n[+] RESULTADOS:")
    for sni_result in result["sni_results"]:
        print(f"\n  SNI: {sni_result['sni']}")
        print(f"  Válido: {sni_result['valid']}")
        if sni_result['valid']:
            print(f"  SSL Version: {sni_result['ssl_version']}")
            print(f"  Cipher: {sni_result['cipher']}")
        else:
            print(f"  Erro: {sni_result['error']}")


def payload_generator_menu():
    """Menu do Gerador de Payloads"""
    print("\n" + "="*40)
    print("PAYLOAD GENERATOR")
    print("="*40)
    print("1. Reverse Shell")
    print("2. SQL Injection")
    print("3. XSS Payload")
    print("4. Password List")
    print("="*40)
    
    choice = input("Escolha: ").strip()
    
    generator = PayloadGenerator()
    
    if choice == "1":
        lhost = input("LHOST: ").strip()
        lport = input("LPORT: ").strip()
        shell_type = input("Tipo (bash/python/nc/perl) [bash]: ").strip() or "bash"
        
        payload = generator.generate_reverse_shell(lhost, int(lport), shell_type)
        print(f"\n[+] Payload Gerado:\n{payload}")
        
        encoding = input("\nCodificar? (base64/hex/url/none) [none]: ").strip()
        if encoding != "none" and encoding:
            encoded = generator.generate_encoded_payload(payload, encoding)
            print(f"\n[+] Payload Codificado ({encoding}):\n{encoded}")
    
    elif choice == "2":
        technique = input("Técnica (union/error/time-based/boolean) [union]: ").strip() or "union"
        payload = generator.generate_sql_injection(technique=technique)
        print(f"\n[+] SQL Injection Payload:\n{payload}")
    
    elif choice == "3":
        xss_type = input("Tipo XSS (basic/event/img/svg) [basic]: ").strip() or "basic"
        payload = generator.generate_xss_payload(xss_type)
        print(f"\n[+] XSS Payload:\n{payload}")
    
    elif choice == "4":
        size = int(input("Quantidade de senhas [100]: ").strip() or "100")
        length = int(input("Tamanho [8]: ").strip() or "8")
        
        passwords = generator.generate_password_list(size, length)
        print(f"\n[+] Primeiras 10 senhas geradas:")
        for pwd in passwords[:10]:
            print(f"  {pwd}")
        
        save = input("\nSalvar em arquivo? (s/n) [n]: ").strip().lower()
        if save == "s":
            with open("passwords.txt", "w") as f:
                for pwd in passwords:
                    f.write(pwd + "\n")
            print("[+] Salvo em passwords.txt")


def ssh_validator_menu():
    """Menu do SSH Validator"""
    print("\n" + "="*40)
    print("SSH VALIDATOR")
    print("="*40)
    print("1. Validar Credenciais")
    print("2. Brute Force")
    print("3. Check SSH Port")
    print("4. Get SSH Banner")
    print("="*40)
    
    choice = input("Escolha: ").strip()
    
    validator = SSHValidator()
    
    if choice == "1":
        host = input("SSH Host: ").strip()
        port = int(input("SSH Port [22]: ").strip() or "22")
        username = input("Username: ").strip()
        password = input("Password: ").strip()
        
        print("\n[*] Validando credenciais...")
        result = validator.validate_ssh_credentials(host, port, username, password)
        
        print(f"\n[+] Resultado:")
        print(f"  Host: {result['host']}:{result['port']}")
        print(f"  Usuário: {result['username']}")
        print(f"  Válido: {result['valid']}")
        if result['error']:
            print(f"  Erro: {result['error']}")
    
    elif choice == "2":
        host = input("SSH Host: ").strip()
        port = int(input("SSH Port [22]: ").strip() or "22")
        username = input("Username: ").strip()
        wordlist = input("Caminho do wordlist: ").strip()
        
        if not os.path.exists(wordlist):
            print(f"[-] Arquivo não encontrado: {wordlist}")
            return
        
        with open(wordlist, "r") as f:
            passwords = [pwd.strip() for pwd in f.readlines()]
        
        print(f"\n[*] Testando {len(passwords)} senhas...")
        result = validator.brute_force_ssh(host, port, username, passwords)
        
        print(f"\n[+] Resultado:")
        print(f"  Host: {result['host']}:{result['port']}")
        print(f"  Usuário: {result['username']}")
        print(f"  Encontrado: {result['found']}")
        if result['found']:
            print(f"  Senha Válida: {result['valid_password']}")
        print(f"  Tentativas: {result['attempts']}")
    
    elif choice == "3":
        host = input("SSH Host: ").strip()
        port = int(input("SSH Port [22]: ").strip() or "22")
        
        print("\n[*] Verificando porta...")
        is_open = validator.check_ssh_port_open(host, port)
        print(f"\n[+] Porta {port}: {'ABERTA' if is_open else 'FECHADA'}")
    
    elif choice == "4":
        host = input("SSH Host: ").strip()
        port = int(input("SSH Port [22]: ").strip() or "22")
        
        print("\n[*] Obtendo banner...")
        banner = validator.get_ssh_banner(host, port)
        print(f"\n[+] Banner:\n{banner}")


def tunnel_config_menu():
    """Menu de Configuração de Túneis"""
    print("\n" + "="*40)
    print("TUNNEL CONFIGURATION")
    print("="*40)
    print("1. Criar Túnel Local (-L)")
    print("2. Criar Túnel Remoto (-R)")
    print("3. Criar Túnel SOCKS5")
    print("4. Listar Túneis")
    print("="*40)
    
    choice = input("Escolha: ").strip()
    
    tunnel_config = TunnelConfig()
    
    if choice == "1":
        name = input("Nome do túnel: ").strip()
        ssh_host = input("SSH Host: ").strip()
        ssh_port = int(input("SSH Port [22]: ").strip() or "22")
        ssh_user = input("SSH User: ").strip()
        ssh_pass = input("SSH Password: ").strip()
        local_port = int(input("Porta Local: ").strip())
        remote_host = input("Host Remoto: ").strip()
        remote_port = int(input("Porta Remota: ").strip())
        
        result = tunnel_config.create_local_tunnel(
            name, ssh_host, ssh_port, ssh_user, ssh_pass,
            local_port, remote_host, remote_port
        )
        print(f"\n[+] Túnel criado:\n{tunnel_config.export_tunnel_config(name, 'txt')}")
    
    elif choice == "2":
        name = input("Nome do túnel: ").strip()
        ssh_host = input("SSH Host: ").strip()
        ssh_port = int(input("SSH Port [22]: ").strip() or "22")
        ssh_user = input("SSH User: ").strip()
        ssh_pass = input("SSH Password: ").strip()
        remote_port = int(input("Porta Remota: ").strip())
        local_host = input("Host Local: ").strip()
        local_port = int(input("Porta Local: ").strip())
        
        result = tunnel_config.create_remote_tunnel(
            name, ssh_host, ssh_port, ssh_user, ssh_pass,
            remote_port, local_host, local_port
        )
        print(f"\n[+] Túnel criado:\n{tunnel_config.export_tunnel_config(name, 'txt')}")
    
    elif choice == "3":
        name = input("Nome do túnel: ").strip()
        ssh_host = input("SSH Host: ").strip()
        ssh_port = int(input("SSH Port [22]: ").strip() or "22")
        ssh_user = input("SSH User: ").strip()
        ssh_pass = input("SSH Password: ").strip()
        socks_port = int(input("Porta SOCKS: ").strip())
        
        result = tunnel_config.create_socks_tunnel(
            name, ssh_host, ssh_port, ssh_user, ssh_pass, socks_port
        )
        print(f"\n[+] Túnel SOCKS criado:\n{tunnel_config.export_tunnel_config(name, 'txt')}")
    
    elif choice == "4":
        tunnels = tunnel_config.list_tunnels()
        if tunnels:
            print("\n[+] Túneis Configurados:")
            for tunnel in tunnels:
                print(f"  - {tunnel['name']} ({tunnel['type']}) - {tunnel['status']}")
        else:
            print("\n[-] Nenhum túnel configurado")


def main():
    """Função principal"""
    print_banner()
    
    while True:
        print_menu()
        choice = input("Escolha uma opção: ").strip()
        
        try:
            if choice == "1":
                sni_scanner_menu()
            elif choice == "2":
                payload_generator_menu()
            elif choice == "3":
                ssh_validator_menu()
            elif choice == "4":
                tunnel_config_menu()
            elif choice == "5":
                print("\n[*] Saindo... Até logo! 👋")
                sys.exit(0)
            else:
                print("\n[-] Opção inválida!")
        except Exception as e:
            print(f"\n[-] Erro: {str(e)}")
            input("\nPressione Enter para continuar...")


if __name__ == "__main__":
    main()
