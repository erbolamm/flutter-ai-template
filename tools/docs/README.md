# 📚 Documentación de Dependencias

Esta carpeta contiene documentación offline para todas las dependencias principales del proyecto. Esto permite que la IA pueda consultar información detallada sin necesidad de buscar en internet.

## 📁 Estructura

```
docs/
├── README.md                    # Este archivo
├── core/                        # Dependencias obligatorias
│   ├── logger.md               # Logging profesional
│   ├── get_it.md               # Inyección de dependencias
│   └── provider.md             # Manejo de estado
├── firebase/                    # Servicios Firebase
│   ├── firebase_core.md        # Inicialización
│   ├── firebase_auth.md        # Autenticación
│   ├── cloud_firestore.md      # Base de datos
│   └── firebase_crashlytics.md # Análisis de crashes
├── ui/                         # Componentes de UI
│   ├── flutter_launcher_icons.md
│   └── flutter_native_splash.md
└── utils/                      # Utilidades
    ├── permission_handler.md
    └── google_mobile_ads.md
```

## 🎯 Propósito

1. **Acceso offline**: IA no necesita internet para consultar docs
2. **Información actualizada**: Versiones específicas del proyecto
3. **Ejemplos contextualizados**: Códigos adaptados al proyecto
4. **Configuración específica**: Setup particular de cada dependencia

## 📝 Formato de Documentación

Cada archivo sigue esta estructura:

```markdown
# Nombre de la Dependencia

## 📋 Información General
- **Versión**: X.X.X (según pubspec.yaml)
- **Propósito**: Descripción breve
- **Documentación oficial**: [enlace]

## 🚀 Instalación
(Instrucciones específicas)

## 💡 Uso Básico
(Ejemplos de código)

## ⚙️ Configuración Avanzada
(Setup específico del proyecto)

## 🐛 Problemas Comunes
(Troubleshooting)

## 📚 Recursos Adicionales
(Enlaces y referencias)
```

## 🔄 Mantenimiento

Al agregar/actualizar dependencias:

1. Actualizar `pubspec.yaml`
2. Crear/actualizar archivo `.md` correspondiente
3. Verificar ejemplos de código
4. Probar que la IA puede acceder a la info

---

💡 **Tip**: La IA puede usar `semantic_search` para encontrar información específica en estos archivos.
