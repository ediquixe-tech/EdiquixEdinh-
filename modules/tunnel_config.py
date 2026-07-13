"""
Tunnel Configuration Module
Configura e gerencia túneis SSH
"""

import paramiko
import threading
from typing import Dict, List, Optional
from datetime import datetime
import json


class TunnelConfig:
    def __init__(self):
        self.tunnels = {}
        self.active_tunnels = []
    
    def create_local_tunnel(self, tunnel_name: str, ssh_host: str, 
                           ssh_port: int, ssh_username: str, 
                           ssh_password: str, local_port: int, 
                           remote_host: str, remote_port: int) -> Dict:
        """
        Cria um túnel local (-L)
        Encaminha local:local_port -> ssh_host -> remote_host:remote_port
        
        Args:
            tunnel_name: Nome identificador do túnel
            ssh_host: IP do servidor SSH
            ssh_port: Porta SSH
            ssh_username: Usuário SSH
            ssh_password: Senha SSH
            local_port: Porta local para escuta
            remote_host: Host de destino
            remote_port: Porta de destino
            
        Returns:
            Dicionário com configuração do túnel
        """
        tunnel_config = {
            "name": tunnel_name,
            "type": "local",
            "ssh_host": ssh_host,
            "ssh_port": ssh_port,
            "ssh_username": ssh_username,
            "local_port": local_port,
            "remote_host": remote_host,
            "remote_port": remote_port,
            "created_at": datetime.now().isoformat(),
            "status": "configured",
            "client": None
        }
        
        self.tunnels[tunnel_name] = tunnel_config
        return tunnel_config
    
    def create_remote_tunnel(self, tunnel_name: str, ssh_host: str, 
                            ssh_port: int, ssh_username: str, 
                            ssh_password: str, remote_port: int, 
                            local_host: str, local_port: int) -> Dict:
        """
        Cria um túnel remoto (-R)
        Encaminha ssh_host:remote_port -> local_host:local_port
        
        Args:
            tunnel_name: Nome identificador do túnel
            ssh_host: IP do servidor SSH
            ssh_port: Porta SSH
            ssh_username: Usuário SSH
            ssh_password: Senha SSH
            remote_port: Porta remota para escuta
            local_host: Host local
            local_port: Porta local
            
        Returns:
            Dicionário com configuração do túnel
        """
        tunnel_config = {
            "name": tunnel_name,
            "type": "remote",
            "ssh_host": ssh_host,
            "ssh_port": ssh_port,
            "ssh_username": ssh_username,
            "remote_port": remote_port,
            "local_host": local_host,
            "local_port": local_port,
            "created_at": datetime.now().isoformat(),
            "status": "configured",
            "client": None
        }
        
        self.tunnels[tunnel_name] = tunnel_config
        return tunnel_config
    
    def create_socks_tunnel(self, tunnel_name: str, ssh_host: str, 
                           ssh_port: int, ssh_username: str, 
                           ssh_password: str, socks_port: int) -> Dict:
        """
        Cria um túnel SOCKS5
        
        Args:
            tunnel_name: Nome identificador do túnel
            ssh_host: IP do servidor SSH
            ssh_port: Porta SSH
            ssh_username: Usuário SSH
            ssh_password: Senha SSH
            socks_port: Porta SOCKS local
            
        Returns:
            Dicionário com configuração do túnel
        """
        tunnel_config = {
            "name": tunnel_name,
            "type": "socks",
            "ssh_host": ssh_host,
            "ssh_port": ssh_port,
            "ssh_username": ssh_username,
            "socks_port": socks_port,
            "created_at": datetime.now().isoformat(),
            "status": "configured",
            "client": None
        }
        
        self.tunnels[tunnel_name] = tunnel_config
        return tunnel_config
    
    def activate_tunnel(self, tunnel_name: str) -> Dict:
        """
        Ativa um túnel SSH configurado
        
        Args:
            tunnel_name: Nome do túnel para ativar
            
        Returns:
            Dicionário com status da ativação
        """
        if tunnel_name not in self.tunnels:
            return {"status": "error", "message": "Tunnel not found"}
        
        tunnel = self.tunnels[tunnel_name]
        
        try:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            
            # Conecta ao servidor SSH
            client.connect(
                tunnel["ssh_host"],
                port=tunnel["ssh_port"],
                username=tunnel["ssh_username"],
                password=tunnel["ssh_password"],
                timeout=10
            )
            
            tunnel["client"] = client
            tunnel["status"] = "active"
            self.active_tunnels.append(tunnel_name)
            
            return {
                "status": "success",
                "message": f"Tunnel {tunnel_name} activated",
                "tunnel": tunnel
            }
            
        except Exception as e:
            tunnel["status"] = "error"
            return {
                "status": "error",
                "message": str(e),
                "tunnel_name": tunnel_name
            }
    
    def deactivate_tunnel(self, tunnel_name: str) -> Dict:
        """
        Desativa um túnel SSH
        
        Args:
            tunnel_name: Nome do túnel para desativar
            
        Returns:
            Dicionário com status da desativação
        """
        if tunnel_name not in self.tunnels:
            return {"status": "error", "message": "Tunnel not found"}
        
        tunnel = self.tunnels[tunnel_name]
        
        try:
            if tunnel["client"]:
                tunnel["client"].close()
            
            tunnel["status"] = "inactive"
            tunnel["client"] = None
            
            if tunnel_name in self.active_tunnels:
                self.active_tunnels.remove(tunnel_name)
            
            return {
                "status": "success",
                "message": f"Tunnel {tunnel_name} deactivated"
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }
    
    def get_tunnel_status(self, tunnel_name: str) -> Dict:
        """
        Obtém status de um túnel
        
        Args:
            tunnel_name: Nome do túnel
            
        Returns:
            Dicionário com status do túnel
        """
        if tunnel_name not in self.tunnels:
            return {"status": "error", "message": "Tunnel not found"}
        
        tunnel = self.tunnels[tunnel_name]
        return {
            "name": tunnel["name"],
            "type": tunnel["type"],
            "status": tunnel["status"],
            "created_at": tunnel["created_at"]
        }
    
    def list_tunnels(self) -> List[Dict]:
        """
        Lista todos os túneis
        
        Returns:
            Lista com informações de todos os túneis
        """
        tunnels_info = []
        for name, tunnel in self.tunnels.items():
            tunnels_info.append({
                "name": name,
                "type": tunnel["type"],
                "status": tunnel["status"],
                "created_at": tunnel["created_at"]
            })
        return tunnels_info
    
    def export_tunnel_config(self, tunnel_name: str, format: str = "json") -> str:
        """
        Exporta configuração de um túnel
        
        Args:
            tunnel_name: Nome do túnel
            format: Formato de exportação (json, txt)
            
        Returns:
            String com configuração formatada
        """
        if tunnel_name not in self.tunnels:
            return "Tunnel not found"
        
        tunnel = self.tunnels[tunnel_name]
        
        # Remove cliente do export
        export_tunnel = {k: v for k, v in tunnel.items() if k != "client"}
        
        if format == "json":
            return json.dumps(export_tunnel, indent=2)
        else:
            output = f"\n{'='*50}\n"
            output += f"Tunnel: {export_tunnel['name']}\n"
            output += f"Type: {export_tunnel['type']}\n"
            output += f"Status: {export_tunnel['status']}\n"
            output += f"SSH Host: {export_tunnel['ssh_host']}:{export_tunnel['ssh_port']}\n"
            output += f"SSH User: {export_tunnel['ssh_username']}\n"
            if export_tunnel["type"] == "local":
                output += f"Local: 127.0.0.1:{export_tunnel['local_port']}\n"
                output += f"Remote: {export_tunnel['remote_host']}:{export_tunnel['remote_port']}\n"
            return output
