# 🤝 Guía de Contribución

¡Gracias por tu interés en contribuir a la Plantilla Universal Flutter + IA! 

## 📋 Cómo Contribuir

### 1. 🍴 Fork y Clone
```bash
# Fork en GitHub, luego:
git clone https://github.com/franciscomateomarquez/flutter-ai-template.git
cd flutter-ai-template
```

### 2. 🌿 Crear Branch
```bash
git checkout -b feature/nueva-funcionalidad
# o
git checkout -b fix/correccion-importante
# o
git checkout -b docs/mejora-documentacion
```

### 3. ✅ Hacer Cambios
- **Sigue las convenciones**: Código en español, effective_dart
- **Documenta**: Actualiza archivos .md relevantes
- **Testa**: Verifica que los scripts funcionen

### 4. 📝 Commit y Push
```bash
git add .
git commit -m "feat: agregar nueva funcionalidad X"
git push origin feature/nueva-funcionalidad
```

### 5. 🔄 Pull Request
- Describe claramente los cambios
- Referencia issues relacionados
- Espera review y feedback

## 🎯 Tipos de Contribución

### 📚 Documentación
- Mejorar README.md
- Agregar documentación de dependencias en `tools/docs/`
- Crear ejemplos de uso
- Traducir contenido

### 🔧 Funcionalidades
- Nuevas capacidades para el servidor MCP
- Scripts de automatización adicionales
- Mejoras en la arquitectura
- Integraciones con nuevos servicios

### 🐛 Correcciones
- Bugs en scripts
- Errores de documentación
- Problemas de compatibilidad
- Mejoras de rendimiento

### 🧪 Testing
- Tests para el servidor MCP
- Validación de scripts
- Tests de integración
- Documentación de casos de prueba

## 📏 Estándares de Código

### Dart/Flutter
```dart
// ✅ CORRECTO
final Logger logger = Logger();
logger.d('Mensaje descriptivo en español');

// ❌ INCORRECTO
print('mensaje');
```

### Python (Servidor MCP)
```python
# ✅ CORRECTO
import yaml
import json

class MCPServer:
    def __init__(self):
        self.logger = self._setup_logger()
    
    def _setup_logger(self):
        # Configuración de logging
        pass

# ❌ INCORRECTO: Sin documentación, nombres en inglés genéricos
def handle(req):
    print(req)
```

### Markdown
```markdown
<!-- ✅ CORRECTO -->
## 🎯 Título Descriptivo

Contenido bien estructurado con ejemplos de código:

```dart
// Código con comentarios explicativos
final ejemplo = 'código claro';
```

<!-- ❌ INCORRECTO: Sin estructura, sin ejemplos -->
titulo
texto plano sin formato
```

## 🏗️ Estructura de Commits

### Prefijos
- `feat:` - Nueva funcionalidad
- `fix:` - Corrección de bug
- `docs:` - Cambios en documentación
- `style:` - Formato, espacios (no afecta lógica)
- `refactor:` - Refactorización de código
- `test:` - Agregar o modificar tests
- `chore:` - Tareas de mantenimiento

### Ejemplos
```bash
feat: agregar documentación para firebase_auth
fix: corregir detección de puerto en servidor MCP  
docs: actualizar instrucciones de instalación
refactor: reorganizar estructura de service locator
test: agregar tests para endpoints MCP
chore: actualizar dependencias en requirements.txt
```

## 🧪 Testing Local

### Servidor MCP
```bash
# Iniciar servidor
./tools/scripts/start_mcp.sh

# Probar endpoints
curl http://localhost:3000/health
curl http://localhost:3000/capabilities

# Detener
Ctrl+C
```

### Scripts
```bash
# Verificar funcionamiento
./tools/scripts/check_mcp.sh

# Probar en proyecto Flutter limpio
mkdir test_project
cd test_project
flutter create .
cp -r ../tools .
cp -r ../.github .
# Verificar que funciona
```

## 🚫 Qué NO Hacer

- ❌ Usar `print()` en lugar de `logger`
- ❌ Código o comentarios en inglés
- ❌ Agregar dependencias sin documentar
- ❌ Cambiar estructura core sin discusión
- ❌ Commits sin descripción clara
- ❌ Romper compatibilidad sin aviso

## 📞 Contacto

### 💬 Discusiones
- **Ideas generales**: [GitHub Discussions](https://github.com/franciscomateomarquez/flutter-ai-template/discussions)
- **Preguntas**: [GitHub Issues](https://github.com/franciscomateomarquez/flutter-ai-template/issues) con label `question`

### 🐛 Reportar Problemas
- **Bugs**: [Crear Issue](https://github.com/franciscomateomarquez/flutter-ai-template/issues/new)
- **Solicitar features**: [Crear Issue](https://github.com/franciscomateomarquez/flutter-ai-template/issues/new) con template de feature request

## 🏆 Reconocimientos

Los contribuyentes serán reconocidos en:
- README.md principal
- Releases notes
- Contributors page

¡Gracias por hacer que esta plantilla sea mejor para toda la comunidad Flutter! 🚀

---

💡 **Tip**: Antes de trabajar en algo grande, abre un Issue para discutir la idea y evitar trabajo duplicado.
