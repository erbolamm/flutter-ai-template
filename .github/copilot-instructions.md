# 🤖 Plantilla de Instrucciones para Agentes AI - Flutter

Este archivo es una **plantilla universal** para proyectos Flutter. Actúa como índice unificado de reglas modulares que pueden acoplarse a cualquier aplicación Flutter existente o nueva.

## 🎯 Cómo Usar Esta Plantilla

1. **Copia** toda la carpeta `.github` a tu proyecto Flutter
2. **Personaliza** el objetivo del proyecto en `instructions/contexto.instructions.md`
3. **Adapta** las dependencias según las necesidades específicas de tu aplicación
4. **Configura** el servidor MCP si necesitas capacidades avanzadas

## 📌 Archivos Fuente Modulares
| Tema | Archivo | Propósito |
|------|---------|-----------|
| Contexto & Código | `instructions/contexto.instructions.md` | **PERSONALIZAR:** Objetivo del proyecto, estilo, SOLID, logging |
| Interacción | `instructions/iteraccion.instructions.md` | Estilo conversacional, confirmaciones (1/2/3), pensamiento crítico |
| MCP Local | `instructions/mcp.instructions.md` | Servidor MCP: propósito, endpoints, capacidades y generalización |
| Guía Técnica | (este índice) | Resumen operativo + enlaces |

## 🧱 Arquitectura Recomendada (Clean Architecture)
Presentation Layer -> (Domain + Core) -> Data Layer

- **Presentation**: Widgets, páginas, controladores de estado
- **Domain**: Casos de uso, entidades, contratos de repositorios
- **Data**: Implementaciones de repositorios, fuentes de datos
- **Core**: Servicios transversales (DI, navegación, logging, utilidades)

> **Principio clave**: `domain` no debe depender de frameworks externos (Firebase/UI); `data` implementa los contratos; `core` provee servicios reutilizables.

## 🔑 Dependencias Base Recomendadas

> **Importante**: Estas dependencias están como ejemplo en `tools/pubspec.example.yaml`. **NO copies este archivo** - añade solo las dependencias que necesites a tu `pubspec.yaml` existente.

### Dependencias Obligatorias
```yaml
dependencies:
  # Framework base
  flutter:
    sdk: flutter
  
  # Logging (OBLIGATORIO - nunca usar print())
  logger: ^2.0.2
  
  # Inyección de dependencias
  get_it: ^8.0.3
  
  # Manejo de estado
  provider: ^6.1.2

dev_dependencies:
  # Linting y análisis de código
  flutter_lints: ^6.0.0
  
  # Configuración de iconos y splash
  flutter_launcher_icons: ^0.14.4
  flutter_native_splash: ^2.4.6
```

### Dependencias Opcionales (según necesidades del proyecto)
```yaml
# Firebase (si necesitas backend)
firebase_core: ^3.6.0
firebase_auth: ^5.3.1
cloud_firestore: ^5.4.3
firebase_crashlytics: ^5.0.1

# Permisos
permission_handler: ^11.3.1

# Ads
google_mobile_ads: ^5.2.0
```

> **Importante**: Consulta `tools/pubspec.example.yaml` para ver el archivo completo de ejemplo.

## ⚙️ Service Locator / Inyección de Dependencias
Ubicación recomendada: `lib/core/di/service_locator.dart`

**Patrón básico para registrar servicios:**
```dart
import 'package:get_it/get_it.dart';

final GetIt sl = GetIt.instance;

Future<void> setupServiceLocator() async {
  // Registrar servicios únicos
  if (!sl.isRegistered<MiRepositorio>()) {
    sl.registerLazySingleton<MiRepositorio>(
      () => MiRepositorioImpl(sl())
    );
  }
}
```

**Contratos/Interfaces:** Define en `lib/domain/repositories/`  
**Implementaciones:** Coloca en `lib/data/repositories/`

## 🔄 Flujos de Desarrollo Recomendados
1. **Análisis de requisitos** -> definir entidades y casos de uso en `domain/`
2. **Contratos de datos** -> crear interfaces de repositorios
3. **Implementación de datos** -> desarrollar repositorios en `data/`
4. **Presentación** -> crear widgets y controladores de estado
5. **Integración** -> configurar inyección de dependencias
6. **Testing** -> escribir tests unitarios y de integración

## 📝 Convenciones de Código
- **Idioma**: Código y comentarios en español
- **Nomenclatura**: 
  - Clases: `PascalCase`
  - Variables y funciones: `camelCase` 
  - Archivos: `snake_case`
- **Arquitectura**: Evita lógica pesada en Widgets; muévela a casos de uso/servicios
- **Objetos**: Prefiere inmutables cuando sea posible
- **Logging**: Usa siempre `logger`, **nunca** `print()`

## 🧪 Testing
- **Ubicación**: Tests en `test/` siguiendo la estructura del código
- **Enfoque**: Mockear interfaces, no instancias reales de servicios externos
- **Comando**: `flutter test --reporter compact`
- **Cobertura**: Priorizar lógica de dominio y casos de uso críticos

## 🖼️ Assets y Recursos
- **Iconos**: Configuración en `flutter_launcher_icons.yaml`
- **Splash Screen**: Sección `flutter_native_splash` en `pubspec.yaml`
- **Assets**: Organizar en carpetas lógicas dentro de `assets/`

## 🛠️ Comandos Esenciales
- Deps: `flutter pub get`  
- Análisis: `flutter analyze`  
- Tests: `flutter test --reporter compact`  
- Iconos: `flutter pub run flutter_launcher_icons -f flutter_launcher_icons.yaml`  
- MCP Start: `./start_mcp.sh [puerto]`  
- MCP Check: `./check_mcp.sh`  

## 🚫 Evitar
Llamar Firebase desde Widgets, usar `print`, añadir libs redundantes, lógica de negocio en UI, dependencias circulares, exponer MCP sin protección fuera de localhost.

## ✅ Pre-Commit Checklist
`flutter analyze` sin issues, tests relevantes verdes, sin dependencias circulares, logs sin datos sensibles, endpoints MCP respondiendo (si se modificó server).

## 🟢 Paso 0 (Agentes) Verificación MCP
Antes de ejecutar tareas NO triviales (búsquedas globales, análisis de duplicados, inventarios de clases, métricas, refactors amplios) el agente debe:
1. Intentar `GET http://localhost:3000/health`.
2. Si falla, intentar puertos alternativos: 3001, 3002, 3003, 3004.
3. Si todos fallan, pedir: "Arranca el servidor MCP con ./start_mcp.sh y avísame cuando esté listo".
4. Confirmado health, cachear capacidades (`GET /capabilities`).
5. Continuar ejecución optimizada usando `/run` donde aplique.
Si el usuario rechaza iniciar MCP, dividir la tarea en pasos menores y advertir posible mayor latencia/limitación.

## ❓Dudas / Extensiones
Si falta detalle (ej. pipeline audio o scheduling), solicitar lectura dirigida indicando carpeta y objetivo. Para MCP ver `instructions/mcp.instructions.md`.

> Fuente canónica: archivos modulares listados arriba. Este índice no debe contener reglas nuevas que no estén reflejadas allí.
