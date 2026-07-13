"""
SSH Validator Module
Valida e testa credenciais SSH
"""

import paramiko
import socket
from typing import Dict, List
import threading


class SSHValidator:
    def __init__(self):
        self.timeout = 10
    
    def validate_ssh_credentials(self, host: str, port: int, 
                                username: str, password: str) -> Dict:
        """
        Valida credenciais SSH
        
        Args:
            host: IP ou hostname SSH
            port: Porta SSH
            username: Usuário
            password: Senha
            
        Returns:
            Dicionário com resultado
        """
        try:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            
            client.connect(
                host,
                port=port,
                username=username,
                password=password,
                timeout=self.timeout,
                look_for_keys=False,
                allow_agent=False
            )
            
            client.close()
            
            return {
                "host": host,
                "port": port,
                "username": username,
                "valid": True,
                "error": None
            }
            
        except paramiko.AuthenticationException:
            return {
                "host": host,
                "port": port,
                "username": username,
                "valid": False,
                "error": "Authentication failed"
            }
        
        except Exception as e:
            return {
                "host": host,
                "port": port,
                "username": username,
                "valid": False,
                "error": str(e)
            }
    
    def brute_force_ssh(self, host: str, port: int, 
                       username: str, passwords: List[str]) -> Dict:
        """
        Tenta brute force em SSH
        
        Args:
            host: IP ou hostname SSH
            port: Porta SSH
            username: Usuário
            passwords: Lista de senhas para testar
            
        Returns:
            Dicionário com resultado
        """
        result = {
            "host": host,
            "port": port,
            "username": username,
            "found": False,
            "valid_password": None,
            "attempts": 0
        }
        
        for password in passwords:
            result["attempts"] += 1
            
            try:
                client = paramiko.SSHClient()
                client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                
                client.connect(
                    host,
                    port=port,
                    username=username,
                    password=password,
                    timeout=self.timeout,
                    look_for_keys=False,
                    allow_agent=False
                )
                
                result["found"] = True
                result["valid_password"] = password
                client.close()
                break
                
            except paramiko.AuthenticationException:
                continue
            
            except Exception:
                continue
        
        return result
    
    def check_ssh_port_open(self, host: str, port: int) -> bool:
        """
        Verifica se porta SSH está aberta
        
        Args:
            host: IP ou hostname
            port: Porta
            
        Returns:
            True se aberta, False caso contrário
        """
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            result = sock.connect_ex((host, port))
            sock.close()
            return result == 0
        except:
            return False
    
    def get_ssh_banner(self, host: str, port: int) -> str:
        """
        Obtém banner SSH do servidor
        
        Args:
            host: IP ou hostname
            port: Porta SSH
            
        Returns:
            String com banner
        """
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            sock.connect((host, port))
            
            banner = sock.recv(1024).decode('utf-8', errors='ignore').strip()
            sock.close()
            
            return banner
        
        except Exception as e:
            return f"Error: {str(e)}"
    
    def scan_ssh_servers(self, network: str, port: int = 22, threads: int = 5) -> List[Dict]:
        """
        Escaneia rede para servidores SSH
        
        Args:
            network: CIDR da rede (ex: 192.168.1.0/24)
            port: Porta SSH
            threads: Número de threads
            
        Returns:
            Lista com servidores SSH encontrados
        """
        import ipaddress
        
        results = []
        net = ipaddress.ip_network(network, strict=False)
        
        def check_host(ip):
            if self.check_ssh_port_open(str(ip), port):
                banner = self.get_ssh_banner(str(ip), port)
                results.append({
                    "ip": str(ip),
                    "port": port,
                    "open": True,
                    "banner": banner
                })
        
        thread_list = []
        for ip in net.hosts():
            while len(threading.enumerate()) > threads + 1:
                pass
            
            t = threading.Thread(target=check_host, args=(ip,))
            t.daemon = True
            t.start()
            thread_list.append(t)
        
        for t in thread_list:
            t.join(timeout=30)
        
        return results
