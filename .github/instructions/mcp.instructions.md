# 🧩 Guía MCP Local

Esta guía documenta cómo ejecutar, mantener y generalizar el servidor MCP (Model Context Protocol) local usado para ampliar las capacidades de agentes AI en este repositorio. Está diseñada para ser portable a otros proyectos con cambios mínimos.

---
## 🎯 Propósito
Proveer un endpoint local HTTP que expone "capacidades" (funciones) consumibles por agentes (ej. asistentes en el editor) para introspección del proyecto, automatización de tareas rutinarias y acceso estructurado a información contextual.

---
## 🗂️ Estructura Relacionada
```
start_mcp.sh            # Inicia el servidor (wrapper)
check_mcp.sh            # Verifica health + lista capacidades
mcp_aliases.sh          # Alias y funciones de conveniencia (añadir a shell)
tools/mcp/server.py     # Implementación del servidor en Python
tools/mcp/requirements.txt  # Dependencias Python
tools/mcp/capabilities.yaml # Configuración de capacidades
tools/mcp/allowlist.yaml    # Lista de permisos de acceso
tools/mcp/README.md     # Documentación específica del MCP
mcp_server.log          # Log manual de arranque (opcional)
.github/instructions/mcp.instructions.md  # Este archivo
```

---
## ✅ Requisitos Previos
- **Python 3.7+** instalado y funcionando (`python3 --version`).
- **PyYAML** instalado (`pip install pyyaml` o automático via `requirements.txt`).
- Puerto libre (por defecto 3000) o especificado al arrancar.
- Opcional: `jq` instalado para mejor lectura JSON (macOS: `brew install jq`).

---
## 🚀 Inicio Rápido
Arrancar con puerto por defecto:
```
./start_mcp.sh
```
Arrancar en puerto personalizado (ej. 3100):
```
./start_mcp.sh 3100
```
Verificar estado:
```
./check_mcp.sh            # Usa 3000 por defecto
./check_mcp.sh 3100       # Puerto alternativo
```

Llamadas manuales:
```
curl -s http://localhost:3000/health | jq .
curl -s http://localhost:3000/capabilities | jq .
```

Ejecutar una capacidad (POST genérico):
```
curl -s -X POST http://localhost:3000/run \
  -H 'Content-Type: application/json' \
  -d '{"capability":"health"}' | jq .
```

---
## 🌐 Endpoints Convencionales
| Método | Ruta            | Descripción                                 | Ejemplo |
|--------|-----------------|---------------------------------------------|---------|
| GET    | /health         | Estado básico del servidor                  | `curl /health` |
| GET    | /capabilities   | Lista metadatos de capacidades disponibles  | `curl /capabilities` |
| POST   | /run            | Ejecuta una capacidad con parámetros JSON   | `{"capability":"health"}` |

Respuesta `health` recomendada:
```json
{
  "status": "ok",
  "timestamp": "ISO-8601",
  "uptimeMs": 1234
}
```

---
## 🧪 Diseño de Capacidades
Cada "capacidad" debe exponer:
- `name`: identificador estable (snake_case).
- `description`: frase clara (español, verbo en infinitivo).
- `params` (opcional): esquema simple (clave -> tipo/nota).
- `run(Map<String,dynamic> params)`: implementación.

Ejemplo conceptual interno (Dart):
```dart
abstract class McpCapability {
  String get name;
  String get description;
  Future<Map<String, dynamic>> run(Map<String, dynamic> params);
}
```

Registrar capacidades en una lista inyectable para mantener SOLID (Open/Closed): extender añadiendo nueva clase sin tocar las existentes.

---
## 🛠️ Servidor Mínimo de Referencia (Python)
El servidor completo está en `tools/mcp/server.py`. Para referencia rápida, aquí un ejemplo mínimo:

```python
#!/usr/bin/env python3
import json
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime

class MCPHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/health':
            response = {
                'status': 'ok',
                'timestamp': datetime.now().isoformat()
            }
            self.send_json(response)
        elif self.path == '/capabilities':
            response = {
                'capabilities': [
                    {'name': 'health', 'description': 'Comprobar estado del servidor'}
                ]
            }
            self.send_json(response)
        else:
            self.send_json({'error': 'Ruta no encontrada'}, 404)
    
    def send_json(self, data, status=200):
        response = json.dumps(data, ensure_ascii=False)
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.end_headers()
        self.wfile.write(response.encode('utf-8'))

if __name__ == '__main__':
    port = int(os.environ.get('MCP_PORT', '3000'))
    server = HTTPServer(('127.0.0.1', port), MCPHandler)
    print(f'[MCP] Escuchando en http://localhost:{port}')
    server.serve_forever()
```

---
## 🧵 Flujo Operativo Habitual
1. Ejecutas `./start_mcp.sh` (instala dependencias si faltan).  
2. El script exporta `MCP_PORT` y lanza `dart run tools/mcp/server.dart`.  
3. Verificas con `./check_mcp.sh` o alias `mcp-check`.  
4. Un agente externo consulta `/capabilities` y decide llamar a `/run`.  
5. Se itera ampliando capacidades sin reinvención.

---
## 🔐 Seguridad (Uso Solo Local)
Escenario: único desarrollador y uso estrictamente local.
- Basta binding a loopback (`127.0.0.1`).
- No se configura token ni auth adicional.
- Si algún día se expone externamente: entonces añadir variable `MCP_TOKEN` y rechazar peticiones sin cabecera (`x-mcp-token`). Hasta entonces no es necesario.

---
## 🧩 Alias Recomendados
Importar en `~/.zshrc`:
```
source /Users/USUARIO/RUTA_PROYECTO/mcp_aliases.sh
```
Ajustar ruta al clonar en otro equipo. Parámetros variables: puerto y path.

---
## 🪵 Logs
Salida estándar suficiente. Si necesitas histórico puntual: `./start_mcp.sh | tee mcp_server.log`. No se mantiene rotación elaborada por ser entorno single‑dev.

---
## 🧯 Troubleshooting
| Síntoma | Causa probable | Acción |
|--------|-----------------|--------|
| `Servidor no responde` | Puerto ocupado | Cambiar puerto `./start_mcp.sh 3100` |
| `curl: (7) Failed to connect` | Servidor no arrancó | Revisar dependencias / stacktrace |
| Respuesta 404 en /run | Nombre capacidad mal escrito | Consultar `/capabilities` |
| JSON inválido | Body mal formateado | Validar con `jq .` antes de enviar |

---
## ♻️ Generalización a Otros Proyectos
1. Copiar carpeta `tools/mcp/` completa al nuevo proyecto.
2. Copiar scripts `start_mcp.sh`, `check_mcp.sh`, `mcp_aliases.sh` ajustando rutas.
3. Instalar dependencias Python: `pip install -r tools/mcp/requirements.txt`.
4. Adaptar `capabilities.yaml` y `allowlist.yaml` según las necesidades del proyecto.
5. Documentar en `.github/instructions/mcp.instructions.md`.
6. Actualizar índice maestro para enlazarla.  

---
## 🧠 Buenas Prácticas de Evolución
- Mantener capacidades pequeñas y con responsabilidad única (SRP de SOLID).  
- Evitar efectos secundarios no declarados.  
- Versionar cambios de contrato (añadir campo `version` en `/capabilities`).  
- No bloquear el loop principal con operaciones largas (usar async / aislar).  
- Añadir tests unitarios para cada capacidad crítica.

---
## 🚧 Próximos Pasos (Enfoque Single Dev)
Capacidades activas: `health`, `list_capabilities`, `analyze_dependencies`, `list_files`, `read_file`, `flutter_analyze`, `flutter_test`.
- [x] Migrar de Dart a Python para mayor universalidad.
- [x] Reorganizar estructura en `tools/mcp/`.
- [ ] (Opcional futuro) Script que combine analyze + tests en un reporte breve.
- [ ] (Opcional) Añadir campo `version` en /capabilities para saber si cambió el contrato.

---
## 📎 Referencia Rápida
| Acción | Comando |
|-------|---------|
| Iniciar | `./start_mcp.sh` |
| Iniciar puerto custom | `./start_mcp.sh 3100` |
| Verificar | `./check_mcp.sh` |
| Health | `curl -s :3000/health` |
| Capacidades | `curl -s :3000/capabilities` |
| Ejecutar capacidad | `curl -s -X POST :3000/run -d '{"capability":"health"}' -H 'Content-Type: application/json'` |
| Instalar deps Python | `pip install -r tools/mcp/requirements.txt` |

---
## 🔚 Notas
Este documento debe mantenerse corto y accionable. Si crece demasiado, dividir en: `mcp.capabilities.md` y `mcp.security.md`.

---
## 🤖 Protocolo para Agentes / Uso Inteligente del MCP
Esta sección define cuándo un agente debe pedir que el servidor MCP esté activo y cómo proceder.

### 1. Checklist Inicial Antes de Operaciones Costosas
El agente debe verificar o solicitar confirmación de MCP ANTES de:
- Búsquedas globales complejas ("encuentra duplicados", "lista todas las clases X").
- Análisis estructural (dependencias, grafo de imports, métricas).
- Extracción masiva de texto (resumir muchos archivos, inventario de módulos).
- Refactors que impliquen localizar múltiples referencias.

Para tareas triviales (pregunta conceptual, formateo de fragmento ya visible, explicación de código mostrado) se puede omitir MCP.

### 2. Secuencia de Verificación
1. ¿Está ya definido el puerto? Intentar `curl -s http://localhost:$PORT/health` (default 3000).  
2. Si falla, pedir al usuario: "¿Arranco MCP? Ejecuta: ./start_mcp.sh".  
3. Tras confirmación, reintentar health hasta 3 veces (backoff 1s,2s,3s).  
4. Obtener capacidades y cachear localmente la lista (tiempo recomendado: sesión actual).  

### 3. Matriz de Decisión
| Tipo de Solicitud | ¿Requiere MCP? | Motivo |
|-------------------|----------------|-------|
| Explicar fragmento visible | No | Contexto ya proporcionado |
| Buscar archivo/clase en todo el repo | Sí | Evita múltiples lecturas iterativas |
| Detectar código duplicado | Sí | Necesita escaneo global eficiente |
| Añadir icono / cambiar YAML puntual | No | Cambios locales directos |
| Listar dependencias y versiones | Sí (si hay capacidad) | Centraliza parsing pubspec |
| Generar reporte de arquitectura | Sí | Consolidación multi archivo |

### 4. Ejemplos de Prompt que el Agente Puede Usar
- "Confírmame si el MCP está activo (puerto 3000). Si no, indícame cómo iniciarlo y espera mi confirmación."  
- "Necesito escanear duplicados. ¿Puedes arrancar MCP y decirme cuando /health devuelva status ok?"  
- "Proporciona lista de capacidades MCP y su descripción, luego sugiere cuál usar para analizar dependencias."  

### 5. Respuesta Estándar Cuando MCP No Está Activo
```
No detecto respuesta en /health. Inicia el servidor con:
./start_mcp.sh
Avísame cuando veas 'Escuchando en http://localhost:3000' y continuaré.
```

### 6. Consideraciones de Token (Archivado)
No se usa token en modo local único. Solo reactivar esta sección si se planea exponer el puerto fuera de localhost.

### 7. Errores Comunes y Estrategia de Recuperación
| Error | Acción Agente |
|-------|---------------|
| 404 en /capabilities | Reintentar tras 1s; si persiste, sugerir reinicio servidor |
| Timeout /health | Preguntar si puerto personalizado; probar lista `[3000,3100,3200]` |
| 500 en /run | Mostrar payload y sugerir revisar logs locales |

### 8. Buen Comportamiento de Consumo
- Cachear capacidades para no spamear /capabilities en bucles.  
- Reutilizar puerto / token confirmados.  
- Limitar concurrencia: 1 request a la vez salvo endpoints idempotentes.

### 9. Plantilla Interna de Estado (Memoria Sesión)
```json
{
  "mcp": {
    "active": true,
    "port": 3000,
    "capabilitiesCacheTs": "2025-09-03T10:00:00Z",
  "capabilities": ["health","list_capabilities","analyze_dependencies"]
  }
}
```

### 10. Estrategia de Degradación
Si usuario no puede (o no quiere) iniciar MCP:
1. Avisar aumento de latencia por lecturas manuales.  
2. Limitar alcance (ej. sólo carpeta relevante).  
3. Dividir tarea grande en subconsultas que no saturen.
