# 📋 INSTRUCCIONES DE USO - Plantilla Universal Flutter

## 🎯 Cómo Usar Esta Plantilla

### 1. Copiar Carpetas
Copia **únicamente estas carpetas** a tu proyecto Flutter existente:
```
.github/     # Instrucciones para agentes AI
tools/       # Servidor MCP y herramientas
```

### 2. Scripts de Utilidades (Opcionales)
También puedes copiar estos scripts si los necesitas:
```
start_mcp.sh
check_mcp.sh  
mcp_aliases.sh
setup_mcp_shortcuts.sh
```

### 3. ⚠️ IMPORTANTE - No Sobrescribir
**NO copies estos archivos** para evitar conflictos:
- ❌ `pubspec.yaml` (usarás el de tu proyecto existente)
- ❌ Carpeta `lib/` (si existiera)
- ❌ Carpeta `test/` (si existiera)
- ❌ `README.md` del proyecto específico

### 4. Dependencias Recomendadas
Consulta `tools/pubspec.example.yaml` para ver las dependencias que recomendamos añadir a tu `pubspec.yaml` existente, pero **añádelas manualmente** según las necesidades de tu proyecto.

### 5. Personalizar Contexto
1. Abre `.github/instructions/contexto.instructions.md`
2. En la sección **"Objetivo Principal del Proyecto"**
3. Reemplaza la instrucción genérica por una descripción específica de tu aplicación
4. El resto de las reglas se adaptarán automáticamente a tu contexto

### 6. Verificar Funcionamiento
```bash
# Probar el servidor MCP
./start_mcp.sh

# Verificar que funciona
curl http://localhost:3000/health
```

## 🛡️ Protección de Archivos Críticos

### Archivos Protegidos
La carpeta `tools/` contiene archivos configurados como **solo lectura** que **no deben modificarse** a menos que sepas exactamente lo que haces:

```
tools/mcp/
├── server.py          # 🔒 Servidor MCP (ejecutable protegido)
├── requirements.txt   # 🔒 Dependencias Python
├── capabilities.yaml  # 🔒 Configuración de capacidades
├── allowlist.yaml     # 🔒 Lista de permisos
└── README.md         # 🔒 Documentación técnica
```

### ⚠️ Modificar Archivos Protegidos
Si necesitas modificar algún archivo protegido:

1. **Cambiar permisos temporalmente**:
   ```bash
   chmod +w tools/mcp/archivo.yaml
   ```

2. **Hacer tus cambios**

3. **Restaurar protección**:
   ```bash
   chmod -w tools/mcp/archivo.yaml
   ```

### 🔄 Restaurar Permisos Originales
Si se pierden los permisos de protección:
```bash
chmod 755 tools/mcp/
chmod 644 tools/mcp/*.yaml tools/mcp/*.txt tools/mcp/README.md
chmod +x tools/mcp/server.py
```

## 🎯 Resultado Final

Después de copiar la plantilla, tu agente AI podrá:
- ✅ Entender completamente tu proyecto y sus reglas
- ✅ Usar el servidor MCP para análisis avanzados
- ✅ Aplicar tus gustos y prioridades de desarrollo
- ✅ Mantener consistencia en el estilo de código
- ✅ Seguir las mejores prácticas que has definido

---

**¡La plantilla está lista para ser acoplada a cualquier proyecto Flutter sin conflictos!** 🚀
