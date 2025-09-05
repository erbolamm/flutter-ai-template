#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Servidor MCP ligero en Python.
Limita las acciones a las declaradas en capabilities.yaml y allowlist.yaml.
Arranque: python tools/mcp/server.py [puerto]
"""

import asyncio
import json
import os
import socket
import subprocess
import sys
import time
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path
from threading import Thread
from urllib.parse import urlparse, parse_qs
import yaml


# Configuración global
ROOT_DIR = Path.cwd()
CAPABILITIES_FILE = ROOT_DIR / 'tools' / 'mcp' / 'capabilities.yaml'
ALLOWLIST_FILE = ROOT_DIR / 'tools' / 'mcp' / 'allowlist.yaml'

class MCPCapability:
    def __init__(self, name, type_, command=None, path=None, glob=None, allow_patterns=None, description=None):
        self.name = name
        self.type = type_
        self.command = command
        self.path = path
        self.glob = glob
        self.allow_patterns = allow_patterns or []
        self.description = description


class MCPServer:
    def __init__(self):
        self.capabilities = {}
        self.allow_paths = []
        self.allow_regex = []
        self.auth_token = os.environ.get('MCP_TOKEN', '').strip()
        self.shell_timeout = max(5, min(600, int(os.environ.get('MCP_SHELL_TIMEOUT', '60'))))
        self.start_time = datetime.now()
        
    def load_config(self):
        """Cargar configuración desde archivos YAML"""
        self.capabilities = {}
        
        # Cargar capabilities
        if CAPABILITIES_FILE.exists():
            with open(CAPABILITIES_FILE, 'r', encoding='utf-8') as f:
                yaml_content = yaml.safe_load(f)
                capabilities_list = yaml_content.get('capabilities', [])
                
                for item in capabilities_list:
                    name = item.get('name')
                    if not name:
                        continue
                        
                    capability = MCPCapability(
                        name=name,
                        type_=item.get('type', 'shell'),
                        command=item.get('command'),
                        path=item.get('path'),
                        glob=item.get('glob'),
                        allow_patterns=item.get('allow_patterns', []),
                        description=item.get('description')
                    )
                    self.capabilities[name] = capability
        
        # Cargar allowlist
        self.allow_paths = []
        self.allow_regex = []
        if ALLOWLIST_FILE.exists():
            with open(ALLOWLIST_FILE, 'r', encoding='utf-8') as f:
                yaml_content = yaml.safe_load(f)
                self.allow_paths = yaml_content.get('paths', [])
                self.allow_regex = yaml_content.get('regex_patterns', [])

    def is_path_allowed(self, path):
        """Verificar si una ruta está permitida"""
        norm_path = str(Path(path).resolve())
        
        # Verificar rutas permitidas
        for allowed_path in self.allow_paths:
            if norm_path.startswith(str(Path(allowed_path).resolve())):
                return True
                
        # Verificar patrones regex
        import re
        for pattern in self.allow_regex:
            if re.match(pattern, norm_path):
                return True
                
        return False

    def execute_capability(self, capability, params):
        """Ejecutar una capacidad específica"""
        if capability.type == 'health':
            return {
                'status': 'ok',
                'timestamp': datetime.now().isoformat(),
                'uptimeMs': int((datetime.now() - self.start_time).total_seconds() * 1000)
            }
            
        elif capability.type == 'list_capabilities':
            return {'capabilities': list(self.capabilities.keys())}
            
        elif capability.type == 'shell':
            return self.run_shell_command(capability.command)
            
        elif capability.type == 'analyze_dependencies':
            return self.analyze_dependencies()
            
        elif capability.type == 'list_files':
            return self.list_files(capability.path, capability.glob)
            
        elif capability.type == 'read_file':
            file_path = params.get('path')
            if not file_path:
                return {'error': 'Falta parámetro path'}
            
            if not self.is_path_allowed(file_path):
                return {'error': 'Acceso denegado'}
                
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                return {'path': file_path, 'content': content}
            except FileNotFoundError:
                return {'error': 'Archivo no encontrado'}
            except Exception as e:
                return {'error': str(e)}
        else:
            raise ValueError(f'Tipo no soportado: {capability.type}')

    def run_shell_command(self, command):
        """Ejecutar comando shell con timeout"""
        start_time = time.time()
        
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=self.shell_timeout
            )
            
            duration_ms = int((time.time() - start_time) * 1000)
            
            # Truncar salida si es muy larga
            def truncate_output(text, max_bytes=200*1024):
                if len(text.encode('utf-8')) <= max_bytes:
                    return text
                truncated = text[:max_bytes//2]
                return f'{truncated}\n...[TRUNCATED] ({len(text.encode("utf-8"))} bytes)'
            
            return {
                'exitCode': result.returncode,
                'timedOut': False,
                'durationMs': duration_ms,
                'stdout': truncate_output(result.stdout),
                'stderr': truncate_output(result.stderr)
            }
            
        except subprocess.TimeoutExpired:
            duration_ms = int((time.time() - start_time) * 1000)
            return {
                'exitCode': -1,
                'timedOut': True,
                'durationMs': duration_ms,
                'stdout': '',
                'stderr': f'Comando excedió timeout de {self.shell_timeout}s'
            }
        except Exception as e:
            duration_ms = int((time.time() - start_time) * 1000)
            return {
                'exitCode': -1,
                'timedOut': False,
                'durationMs': duration_ms,
                'stdout': '',
                'stderr': str(e)
            }

    def analyze_dependencies(self):
        """Analizar dependencias del pubspec.yaml"""
        pubspec_file = ROOT_DIR / 'pubspec.yaml'
        if not pubspec_file.exists():
            return {'error': 'pubspec.yaml no encontrado'}
        
        try:
            with open(pubspec_file, 'r', encoding='utf-8') as f:
                yaml_content = yaml.safe_load(f)
            
            env = yaml_content.get('environment', {})
            deps = yaml_content.get('dependencies', {})
            dev_deps = yaml_content.get('dev_dependencies', {})
            
            dependencies = []
            for name, version in deps.items():
                dependencies.append({
                    'name': str(name),
                    'version': str(version),
                    'scope': 'direct'
                })
            
            dev_dependencies = []
            for name, version in dev_deps.items():
                dev_dependencies.append({
                    'name': str(name),
                    'version': str(version),
                    'scope': 'dev'
                })
            
            return {
                'sdk': str(env.get('sdk', '')),
                'flutter': str(env.get('flutter', '')),
                'dependencies': dependencies,
                'dev_dependencies': dev_dependencies,
                'summary': {
                    'count_dependencies': len(dependencies),
                    'count_dev_dependencies': len(dev_dependencies)
                }
            }
            
        except Exception as e:
            return {'error': str(e)}

    def list_files(self, directory, glob_pattern=None):
        """Listar archivos en un directorio"""
        if not directory:
            return {'files': []}
            
        try:
            dir_path = Path(directory)
            if not dir_path.exists():
                return {'files': []}
            
            files = []
            pattern = glob_pattern or '*'
            
            for file_path in dir_path.rglob(pattern):
                if file_path.is_file():
                    relative_path = str(file_path.relative_to(ROOT_DIR))
                    files.append(relative_path)
            
            files.sort()
            return {'files': files}
            
        except Exception as e:
            return {'error': str(e)}


class MCPRequestHandler(BaseHTTPRequestHandler):
    def __init__(self, request, client_address, server, mcp_server):
        self.mcp_server = mcp_server
        super().__init__(request, client_address, server)
    
    def log_message(self, format, *args):
        # Logging silencioso para evitar spam
        pass
    
    def do_GET(self):
        try:
            parsed_url = urlparse(self.path)
            path = parsed_url.path
            
            # Verificar autenticación (excepto para /health)
            if path != '/health' and self.mcp_server.auth_token:
                auth_header = self.headers.get('x-mcp-token', '')
                if auth_header != self.mcp_server.auth_token:
                    self.send_error_response(401, 'No autorizado')
                    return
            
            if path == '/health':
                response = {'status': 'ok'}
                self.send_json_response(response)
                
            elif path == '/capabilities':
                capabilities_list = []
                for cap in self.mcp_server.capabilities.values():
                    cap_info = {
                        'name': cap.name,
                        'type': cap.type
                    }
                    if cap.description:
                        cap_info['description'] = cap.description
                    capabilities_list.append(cap_info)
                
                response = {'capabilities': capabilities_list}
                self.send_json_response(response)
                
            else:
                self.send_error_response(404, 'Ruta no encontrada')
                
        except Exception as e:
            print(f'[MCP][ERROR] GET {self.path}: {e}')
            self.send_error_response(500, 'Error interno')
    
    def do_POST(self):
        try:
            parsed_url = urlparse(self.path)
            path = parsed_url.path
            
            # Verificar autenticación
            if self.mcp_server.auth_token:
                auth_header = self.headers.get('x-mcp-token', '')
                if auth_header != self.mcp_server.auth_token:
                    self.send_error_response(401, 'No autorizado')
                    return
            
            if path == '/run':
                content_length = int(self.headers.get('Content-Length', 0))
                post_data = self.rfile.read(content_length).decode('utf-8')
                
                try:
                    data = json.loads(post_data) if post_data else {}
                except json.JSONDecodeError:
                    self.send_error_response(400, 'JSON inválido')
                    return
                
                capability_name = data.get('capability')
                if not capability_name:
                    self.send_error_response(400, 'Falta "capability"')
                    return
                
                capability = self.mcp_server.capabilities.get(capability_name)
                if not capability:
                    self.send_error_response(404, f'Capacidad no encontrada: {capability_name}')
                    return
                
                params = data.get('params', {})
                result = self.mcp_server.execute_capability(capability, params)
                
                response = {
                    'ok': True,
                    'capability': capability_name,
                    'result': result
                }
                self.send_json_response(response)
                
            else:
                self.send_error_response(404, 'Ruta no encontrada')
                
        except Exception as e:
            print(f'[MCP][ERROR] POST {self.path}: {e}')
            self.send_error_response(500, 'Error interno')
    
    def send_json_response(self, data, status_code=200):
        response_json = json.dumps(data, ensure_ascii=False, indent=2)
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(response_json.encode('utf-8'))))
        self.end_headers()
        self.wfile.write(response_json.encode('utf-8'))
    
    def send_error_response(self, status_code, message):
        error_data = {
            'ok': False,
            'error': message,
            'code': status_code
        }
        self.send_json_response(error_data, status_code)


def find_available_port(requested_port, max_attempts=5):
    """Buscar puerto disponible automáticamente"""
    port = requested_port
    
    for attempt in range(max_attempts):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('127.0.0.1', port))
                return port
        except OSError:
            port += 1
    
    raise Exception(f'No se pudo encontrar un puerto disponible después de {max_attempts} intentos')


def main():
    # Determinar puerto
    requested_port = 3000
    if len(sys.argv) > 1:
        try:
            requested_port = int(sys.argv[1])
        except ValueError:
            pass
    
    if not requested_port:
        requested_port = int(os.environ.get('MCP_PORT', '3000'))
    
    # Buscar puerto disponible
    try:
        port = find_available_port(requested_port)
    except Exception as e:
        print(f'[MCP][ERROR] {e}')
        sys.exit(1)
    
    if port != requested_port:
        print(f'[MCP] Puerto {requested_port} ocupado, usando puerto {port}')
    
    # Crear servidor MCP
    mcp_server = MCPServer()
    mcp_server.load_config()
    
    # Crear handler personalizado
    def handler_factory(*args):
        return MCPRequestHandler(*args, mcp_server)
    
    # Iniciar servidor HTTP
    try:
        httpd = HTTPServer(('127.0.0.1', port), handler_factory)
        
        auth_info = 'none' if not mcp_server.auth_token else 'token'
        print(f'[MCP] Escuchando en http://localhost:{port} (timeout={mcp_server.shell_timeout}s auth={auth_info})')
        
        httpd.serve_forever()
        
    except KeyboardInterrupt:
        print('\n[MCP] Cerrando servidor...')
        httpd.shutdown()
    except Exception as e:
        print(f'[MCP][ERROR] {e}')
        sys.exit(1)


if __name__ == '__main__':
    main()
