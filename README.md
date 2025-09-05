# 🚀 Plantilla Universal Flutter + IA

> **Plantilla profesional para proyectos Flutter con configuración avanzada para agentes IA (GitHub Copilot, Claude, etc.)**

[![Flutter](https://img.shields.io/badge/Flutter-Framework-blue?logo=flutter)](https://flutter.dev/)
[![Python](https://img.shields.io/badge/Python-MCP%20Server-green?logo=python)](https://python.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## ✨ Características

- 🧠 **Configuración IA completa** - Instrucciones modulares para agentes IA
- 🏗️ **Arquitectura Clean** - Estructura S.O.L.I.D. preconfigurada  
- 🐍 **Servidor MCP** - Capacidades avanzadas para IA (Python, universal)
- 📚 **Documentación local** - Dependencias documentadas offline
- 🔧 **Scripts automatizados** - Gestión simplificada del servidor MCP
- 🎯 **Cero conflictos** - Se integra sin problemas en proyectos existentes

## 🚀 Instalación Rápida

### 1. Clonar e integrar
```bash
# Clonar la plantilla
git clone https://github.com/erbolamm/flutter-ai-template.git
cd flutter-ai-template

# Copiar a tu proyecto Flutter existente
cp -r .github /ruta/tu/proyecto/flutter/
cp -r tools /ruta/tu/proyecto/flutter/
cp PROMPT_INICIAL.txt /ruta/tu/proyecto/flutter/
```

### 2. Configurar IA
```bash
# En tu proyecto, copia el contenido de PROMPT_INICIAL.txt
cat PROMPT_INICIAL.txt
# Pégalo en tu chat con GitHub Copilot/Claude
# Personaliza el objetivo del proyecto
# Borra el archivo PROMPT_INICIAL.txt
rm PROMPT_INICIAL.txt
```

### 3. Servidor MCP (Opcional)
```bash
# Para capacidades avanzadas de IA
./tools/scripts/start_mcp.sh

# Verificar funcionamiento
curl http://localhost:3000/health
```

## 📁 Estructura

```
tu-proyecto-flutter/
├── .github/
│   ├── copilot-instructions.md      # Índice de instrucciones IA
│   └── instructions/
│       ├── contexto.instructions.md  # Reglas de código y arquitectura
│       ├── iteraccion.instructions.md # Estilo de conversación IA
│       └── mcp.instructions.md        # Configuración servidor MCP
├── tools/
│   ├── mcp/                          # Servidor MCP (Python)
│   ├── scripts/                      # Scripts de automatización
│   ├── docs/                         # Documentación de dependencias
│   ├── pubspec.example.yaml          # Dependencias recomendadas
│   └── README.md                     # Documentación técnica
└── PROMPT_INICIAL.txt                # Configuración inicial IA (borrar después)
```

## 🎯 Casos de Uso

### Para Desarrolladores
- ✅ Acelerar desarrollo con IA configurada
- ✅ Arquitectura limpia desde el inicio
- ✅ Documentación offline de dependencias
- ✅ Scripts de automatización listos

### Para Equipos
- ✅ Estándares de código unificados
- ✅ Configuración IA consistente
- ✅ Onboarding rápido de nuevos miembros
- ✅ Documentación técnica centralizada

### Para Proyectos Existentes
- ✅ Integración sin conflictos
- ✅ Mejora gradual de arquitectura
- ✅ Potenciación de herramientas IA
- ✅ Migración progresiva a Clean Architecture

## 🛠️ Dependencias Incluidas

### Core (Obligatorias)
- `logger` - Logging profesional (NO usar `print()`)
- `get_it` - Inyección de dependencias
- `provider` - Manejo de estado

### Opcionales (Según proyecto)
- `firebase_*` - Backend completo
- `permission_handler` - Permisos del sistema
- `google_mobile_ads` - Monetización

> 📖 **Documentación offline**: Cada dependencia tiene su documentación en `tools/docs/`

## 🧠 Configuración IA

### Principios Aplicados
- ✅ **S.O.L.I.D.** - Arquitectura limpia y mantenible
- ✅ **DRY** - No repetir código
- ✅ **YAGNI** - Solo lo que necesitas
- ✅ **Clean Code** - Código autodocumentado

### Reglas Automáticas
- 🚫 **Nunca** usar `print()` → usar `logger`
- 🔤 **Idioma**: Todo en español
- 📝 **Estilo**: `effective_dart` siempre
- 🏗️ **Arquitectura**: Clean Architecture por defecto

## 📚 Documentación

### Usuarios
- [`tools/COPY_INSTRUCTIONS.md`](tools/COPY_INSTRUCTIONS.md) - Guía de instalación
- [`PROMPT_INICIAL.txt`](PROMPT_INICIAL.txt) - Configuración IA inicial

### Desarrolladores
- [`tools/README.md`](tools/README.md) - Documentación técnica completa
- [`tools/mcp/README.md`](tools/mcp/README.md) - Servidor MCP
- [`tools/docs/`](tools/docs/) - Documentación de dependencias

## 🤝 Contribuir

1. **Fork** el repositorio
2. **Crea** una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. **Commit** tus cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. **Push** a la rama (`git push origin feature/nueva-funcionalidad`)
5. **Crea** un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.

## 🙏 Agradecimientos

- **Flutter Team** - Por el increíble framework
- **GitHub Copilot** - Por la inspiración en configuración IA
- **Comunidad Flutter** - Por las mejores prácticas compartidas

---

⭐ **¿Te gusta esta plantilla? ¡Dale una estrella!**

📧 **¿Problemas o sugerencias?** [Abre un issue](https://github.com/erbolamm/flutter-ai-template/issues)
