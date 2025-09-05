#!/bin/bash
# Script rápido para verificar el estado del servidor MCP
# Uso: ./check_mcp.sh [puerto]

PORT=${1:-3000}
URL="http://localhost:$PORT"

echo "🔍 Verificando servidor MCP en puerto $PORT..."
echo ""

# Health check
echo "🏥 Health check:"
if curl -s "$URL/health" 2>/dev/null | jq . 2>/dev/null; then
    echo "✅ Servidor activo"
else
    echo "❌ Servidor no responde"
    echo ""
    echo "💡 Para iniciar el servidor:"
    echo "   ./start_mcp.sh"
    exit 1
fi

echo ""
echo "📋 Capacidades disponibles:"
curl -s "$URL/capabilities" 2>/dev/null | jq -r '.capabilities[] | "  - \(.name): \(.description // "Sin descripción")"' 2>/dev/null || echo "❌ Error obteniendo capacidades"

echo ""
echo "🔗 URLs útiles:"
echo "  • Health: $URL/health"
echo "  • Capacidades: $URL/capabilities"
echo ""
echo "🧪 Comando de prueba:"
echo "  curl -s -X POST $URL/run -H 'Content-Type: application/json' -d '{\"capability\":\"health\"}'"
