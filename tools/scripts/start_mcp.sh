#!/bin/bash
# Atajo rápido para iniciar el servidor MCP local
# Uso: ./start_mcp.sh [puerto]

set -e

# Cambiar al directorio del proyecto (ir a la raíz desde tools/scripts/)
cd "$(dirname "$0")/../.."

# Puerto por defecto o personalizado
PORT=${1:-3000}
export MCP_PORT=$PORT

echo "🚀 Iniciando servidor MCP local en puerto $PORT..."
echo "📁 Directorio: $(pwd)"
echo "⏰ $(date)"
echo ""

# Verificar que Python esté disponible
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 no encontrado. Instala Python 3.7+ para continuar."
    exit 1
fi

echo "🐍 Python: $(python3 --version)"

# Verificar e instalar dependencias de Python
if [ -f "tools/mcp/requirements.txt" ]; then
    echo "📦 Verificando dependencias de Python..."
    
    # Verificar si PyYAML está instalado
    if ! python3 -c "import yaml" &>/dev/null; then
        echo "📦 Instalando dependencias de Python..."
        
        # Intentar instalación con --user primero
        if python3 -m pip install -r tools/mcp/requirements.txt --user &>/dev/null; then
            echo "✅ Dependencias instaladas con --user"
        elif python3 -m pip install -r tools/mcp/requirements.txt --break-system-packages &>/dev/null; then
            echo "✅ Dependencias instaladas con --break-system-packages"
        else
            echo "❌ Error instalando dependencias. Instala manualmente:"
            echo "   pip install pyyaml"
            echo "   o"
            echo "   python3 -m pip install pyyaml --user"
            exit 1
        fi
    else
        echo "✅ Dependencias de Python OK"
    fi
fi

# Iniciar el servidor
echo "🎯 Iniciando servidor MCP..."
echo "🌐 URL: http://localhost:$PORT"
echo "💾 Health check: http://localhost:$PORT/health"
echo "📋 Capacidades: http://localhost:$PORT/capabilities"
echo ""
echo "⚡ Para probar:"
echo "   curl http://localhost:$PORT/health"
echo ""
echo "🛑 Para detener: Ctrl+C"
echo "════════════════════════════════════════════════════════════════"

python3 tools/mcp/server.py $PORT
