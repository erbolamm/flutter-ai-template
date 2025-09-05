#!/bin/bash
# Script de configuración automática para atajos MCP
# Uso: ./setup_mcp_shortcuts.sh

echo "🔧 Configurando atajos rápidos para servidor MCP..."
echo ""

# Detectar shell
if [ -n "$ZSH_VERSION" ]; then
    SHELL_RC="$HOME/.zshrc"
    SHELL_NAME="zsh"
elif [ -n "$BASH_VERSION" ]; then
    SHELL_RC="$HOME/.bashrc"
    SHELL_NAME="bash"
else
    echo "⚠️  Shell no detectado automáticamente. Configuración manual requerida."
    echo "📁 Archivo de aliases: $(pwd)/mcp_aliases.sh"
    exit 1
fi

echo "🐚 Shell detectado: $SHELL_NAME"
echo "📁 Archivo de configuración: $SHELL_RC"
echo ""

# Verificar si ya están configurados
if grep -q "ATAJOS RÁPIDOS PARA SERVIDOR MCP" "$SHELL_RC" 2>/dev/null; then
    echo "✅ Los atajos MCP ya están configurados en $SHELL_RC"
else
    echo "📝 Agregando atajos MCP a $SHELL_RC..."
    echo "" >> "$SHELL_RC"
    cat mcp_aliases.sh >> "$SHELL_RC"
    echo "✅ Atajos agregados a $SHELL_RC"
fi

echo ""
echo "🎯 Para activar los atajos en la sesión actual:"
echo "   source $SHELL_RC"
echo ""
echo "🚀 O simplemente abre una nueva terminal"
echo ""
echo "📋 Atajos disponibles después de recargar:"
echo "   • mcp-start    - Iniciar servidor MCP"
echo "   • mcp-check    - Verificar estado del servidor"
echo "   • mcp-health   - Health check rápido"
echo "   • mcp-caps     - Ver capacidades disponibles"
echo "   • mcp-run      - Ejecutar capacidad específica"
echo "   • mcp-cd       - Ir al directorio del proyecto"
