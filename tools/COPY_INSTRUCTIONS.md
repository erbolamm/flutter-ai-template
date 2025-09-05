# 🚀 INSTRUCCIONES PARA COPIAR LA PLANTILLA

## 📁 Estructura de la Plantilla
```
📦 Plantilla Flutter Universal/
├── 📂 .github/                    # ✅ COPIAR - Instrucciones AI  
│   ├── copilot-instructions.md    #     Índice maestro
│   └── instructions/              #     Módulos de reglas
│       ├── contexto.instructions.md      # Personalizar objetivo
│       ├── iteraccion.instructions.md    # Estilo de interacción  
│       └── mcp.instructions.md           # Guía servidor MCP
├── 📂 tools/                      # ✅ COPIAR - Herramientas
│   ├── mcp/                       #     Servidor MCP (🔒 protegido)
│   ├── scripts/                   #     Scripts de utilidad
│   ├── pubspec.example.yaml       #     Ejemplo de dependencias
│   ├── README.md                  #     Documentación técnica
│   └── COPY_INSTRUCTIONS.md       #     Esta guía
├── 📄 README.md                   # ❌ NO COPIAR - Es específico de plantilla
```

## 🎯 PASOS PARA COPIAR

### 1. Copiar Carpetas Esenciales
En tu proyecto Flutter existente:
```bash
# Desde la plantilla hacia tu proyecto
cp -r .github/ /ruta/tu/proyecto/flutter/
cp -r tools/ /ruta/tu/proyecto/flutter/
```

### 2. Copiar Scripts (Opcional)
Los scripts están en `tools/scripts/` y puedes crear enlaces simbólicos en la raíz:
```bash
# Desde la raíz de tu proyecto
ln -s tools/scripts/start_mcp.sh start_mcp.sh
ln -s tools/scripts/check_mcp.sh check_mcp.sh
ln -s tools/scripts/mcp_aliases.sh mcp_aliases.sh
```

### 3. ⚠️ NO Copiar Estos Archivos
- ❌ `README.md` (es específico de la plantilla)
- ❌ `pubspec.yaml` (usarás el tuyo existente)
- ❌ Carpetas `lib/`, `test/` si existieran

### 4. Personalizar Dependencias  
1. Abre `tools/pubspec.example.yaml`
2. Copia las dependencias que necesites
3. **Pégalas manualmente** en tu `pubspec.yaml` existente
4. Ejecuta `flutter pub get`

### 5. Personalizar Contexto
1. Abre `.github/instructions/contexto.instructions.md`
2. Encuentra la sección **"Objetivo Principal del Proyecto"**
3. **Reemplaza** la instrucción genérica por tu descripción específica:

```markdown
## 🎯 1. Objetivo Principal del Proyecto

* **Resumen**: [DESCRIBE AQUÍ TU APLICACIÓN ESPECÍFICA]
```

Ejemplo:
```markdown
* **Resumen**: Esta aplicación es un gestor de tareas personal que permite 
  a los usuarios crear, organizar y hacer seguimiento de sus proyectos 
  mediante un sistema de etiquetas y recordatorios inteligentes.
```

### 6. Verificar Instalación
```bash
# Probar servidor MCP
./start_mcp.sh

# En otra terminal, verificar
curl http://localhost:3000/health
```

## ✅ RESULTADO FINAL

Después de copiar la plantilla, tendrás:

- 🤖 **Agente AI configurado** con tus reglas y preferencias
- 🧩 **Servidor MCP funcional** para análisis avanzados
- 📋 **Dependencias recomendadas** según mejores prácticas
- 🛡️ **Archivos protegidos** para evitar modificaciones accidentales
- 🎯 **Contexto personalizado** específico a tu aplicación

**¡Tu agente AI ahora conoce perfectamente tu proyecto y tus estándares!** 🚀

---

## 🔄 Actualizar Plantilla en Proyectos Existentes

Si ya tienes la plantilla en un proyecto y quieres actualizarla:

1. **Respaldar personalización**:
   ```bash
   cp .github/instructions/contexto.instructions.md contexto_backup.md
   ```

2. **Reemplazar archivos**:
   ```bash
   rm -rf .github/ tools/
   # Copiar nueva versión de la plantilla
   ```

3. **Restaurar personalización**:
   ```bash
   # Editar .github/instructions/contexto.instructions.md
   # Pegar tu descripción específica desde contexto_backup.md
   ```
