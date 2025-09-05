# 🧩 Servidor MCP Local - Python

Este directorio contiene el servidor MCP (Model Context Protocol) local para el proyecto, implementado en Python para máxima universalidad y portabilidad.

## 🎯 Propósito

Proveer un endpoint HTTP local que expone "capacidades" (funciones) consumibles por agentes AI para:
- Introspección del proyecto Flutter/Dart
- Automatización de tareas rutinarias
- Acceso estructurado a información contextual

## 📁 Estructura de Archivos

```
tools/mcp/
├── server.py          # Servidor HTTP principal
├── requirements.txt   # Dependencias Python
├── capabilities.yaml  # Configuración de capacidades disponibles
├── allowlist.yaml     # Permisos de acceso a archivos/comandos
└── README.md         # Este archivo
```

## 🚀 Inicio Rápido

### Instalación de Dependencias
```bash
pip install -r tools/mcp/requirements.txt
```

### Inicio del Servidor
```bash
# Desde la raíz del proyecto
./start_mcp.sh

# O directamente con Python
python3 tools/mcp/server.py

# Puerto personalizado
python3 tools/mcp/server.py 3100
```

### Verificación
```bash
curl http://localhost:3000/health
curl http://localhost:3000/capabilities
```

## 🌐 Endpoints Disponibles

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET    | `/health` | Estado del servidor |
| GET    | `/capabilities` | Lista de capacidades disponibles |
| POST   | `/run` | Ejecutar una capacidad con parámetros |

### Ejemplo de Uso
```bash
# Ejecutar análisis de dependencias
curl -X POST http://localhost:3000/run \
  -H 'Content-Type: application/json' \
  -d '{"capability":"analyze_dependencies"}'

# Leer un archivo
curl -X POST http://localhost:3000/run \
  -H 'Content-Type: application/json' \
  -d '{"capability":"read_file","params":{"path":"pubspec.yaml"}}'
```

## ⚙️ Configuración

### Capacidades (`capabilities.yaml`)
Define las funciones disponibles en el servidor. Cada capacidad tiene:
- `name`: Identificador único
- `type`: Tipo de operación (health, shell, read_file, etc.)
- `description`: Descripción legible
- Parámetros específicos según el tipo

### Lista de Permisos (`allowlist.yaml`)
Define qué archivos y rutas pueden ser accedidos por seguridad:
- `paths`: Directorios permitidos
- `regex_patterns`: Patrones de archivos permitidos

## 🔧 Capacidades Predefinidas

- **health**: Estado del servidor
- **list_capabilities**: Lista todas las capacidades
- **analyze_dependencies**: Analiza `pubspec.yaml`
- **list_dart_files**: Lista archivos `.dart` del proyecto
- **read_file**: Lee contenido de archivos permitidos
- **flutter_analyze**: Ejecuta análisis estático
- **flutter_test**: Ejecuta tests del proyecto

## 🛡️ Seguridad

- **Solo localhost**: El servidor solo escucha en `127.0.0.1`
- **Allowlist**: Solo archivos/comandos explícitamente permitidos
- **Sin autenticación**: Adecuado para desarrollo local único
- **Timeouts**: Los comandos shell tienen timeout configurable

## 🔧 Personalización

### Añadir Nueva Capacidad
1. Editar `capabilities.yaml`:
```yaml
- name: mi_capacidad
  type: shell
  command: "echo 'Hola mundo'"
  description: Mi capacidad personalizada
```

2. Reiniciar el servidor

### Ampliar Permisos
1. Editar `allowlist.yaml`:
```yaml
paths:
  - "nueva_carpeta"
regex_patterns:
  - "^nueva_carpeta/.*\\.txt$"
```

## 🐍 Requisitos Python

- **Python 3.7+**
- **PyYAML >= 6.0** (para parsing de configuración)

## 🔄 Selección Automática de Puerto

El servidor intentará usar el puerto especificado (por defecto 3000). Si está ocupado, probará automáticamente los siguientes puertos hasta encontrar uno libre:
- 3000 → 3001 → 3002 → 3003 → 3004

Máximo 5 intentos antes de fallar.

## 📝 Variables de Entorno

| Variable | Descripción | Valor por Defecto |
|----------|-------------|-------------------|
| `MCP_PORT` | Puerto del servidor | 3000 |
| `MCP_TOKEN` | Token de autenticación | (vacío) |
| `MCP_SHELL_TIMEOUT` | Timeout comandos shell (segundos) | 60 |

## 🚨 Troubleshooting

| Problema | Solución |
|----------|----------|
| Puerto ocupado | Usar puerto alternativo: `python3 server.py 3100` |
| PyYAML no encontrado | `pip install pyyaml` |
| Acceso denegado a archivo | Revisar `allowlist.yaml` |
| Comando timeout | Aumentar `MCP_SHELL_TIMEOUT` |

## 📊 Logs

El servidor imprime logs básicos a stdout:
- Inicio y puerto usado
- Errores de ejecución
- Información de capacidades cargadas

Para logs persistentes:
```bash
python3 tools/mcp/server.py | tee mcp.log
```

## 🔄 Migración desde Dart

Este servidor reemplaza la implementación anterior en Dart con las siguientes ventajas:
- ✅ No requiere Flutter/Dart SDK
- ✅ Dependencias mínimas (solo PyYAML)
- ✅ Más universal y portable
- ✅ Sintaxis más familiar para scripts

Los endpoints y funcionalidades son idénticos para mantener compatibilidad.

---

Para más información sobre el protocolo MCP y uso avanzado, consulta `.github/instructions/mcp.instructions.md`.
