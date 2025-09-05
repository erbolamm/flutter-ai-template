# ----------------------------
# ATAJOS RÁPIDOS PARA SERVIDOR MCP
# ----------------------------
# Agregar estas líneas a tu ~/.zshrc o ~/.bashrc

# Alias para iniciar el servidor MCP
alias mcp-start='cd /Users/franciscomateomarquez/apps/me_llaman && ./start_mcp.sh'

# Alias para verificar el servidor MCP
alias mcp-check='cd /Users/franciscomateomarquez/apps/me_llaman && ./check_mcp.sh'

# Alias para hacer peticiones rápidas al MCP
alias mcp-health='curl -s http://localhost:3000/health | jq .'
alias mcp-caps='curl -s http://localhost:3000/capabilities | jq .'

# Función para hacer peticiones personalizadas al MCP
mcp-run() {
    if [ -z "$1" ]; then
        echo "Uso: mcp-run <capability> [params_json]"
        echo "Ejemplo: mcp-run health"
        echo "Ejemplo: mcp-run analyze '{\"file\":\"test.dart\"}'"
        return 1
    fi
    
    local capability="$1"
    local params="${2:-{}}"
    
    curl -s -X POST http://localhost:3000/run \
        -H 'Content-Type: application/json' \
        -d "{\"capability\":\"$capability\", \"params\":$params}" | jq .
}

# Función para ir rápidamente al directorio del proyecto
alias mcp-cd='cd /Users/franciscomateomarquez/apps/me_llaman'

echo "🚀 Atajos MCP cargados:"
echo "  • mcp-start    - Iniciar servidor MCP"
echo "  • mcp-check    - Verificar estado del servidor"
echo "  • mcp-health   - Health check rápido"
echo "  • mcp-caps     - Ver capacidades disponibles"
echo "  • mcp-run      - Ejecutar capacidad específica"
echo "  • mcp-cd       - Ir al directorio del proyecto"
