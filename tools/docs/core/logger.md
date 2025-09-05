# Logger

## 📋 Información General
- **Versión**: ^2.0.2
- **Propósito**: Sistema de logging profesional para Flutter/Dart
- **Documentación oficial**: [pub.dev/packages/logger](https://pub.dev/packages/logger)
- **⚠️ OBLIGATORIO**: Este paquete es OBLIGATORIO en el proyecto. NUNCA usar `print()`

## 🚀 Instalación

Ya incluido en `pubspec.yaml`:
```yaml
dependencies:
  logger: ^2.0.2
```

## 💡 Uso Básico

### Crear una instancia del logger
```dart
import 'package:logger/logger.dart';

final Logger logger = Logger();
```

### Niveles de logging
```dart
// Debug (desarrollo)
logger.d('Mensaje de debug');

// Información
logger.i('Usuario autenticado correctamente');

// Warning
logger.w('Conexión lenta detectada');

// Error
logger.e('Error al cargar datos', error: exception, stackTrace: stackTrace);

// Fatal
logger.f('Error crítico del sistema');
```

### Logging con objetos complejos
```dart
// Objetos JSON
logger.d('Respuesta API: ${jsonEncode(responseData)}');

// Con contexto adicional
logger.i('Navegación completada', 
  error: null, 
  stackTrace: StackTrace.current
);
```

## ⚙️ Configuración Avanzada

### Logger personalizado para producción
```dart
// En lib/core/utils/app_logger.dart
import 'package:logger/logger.dart';

class AppLogger {
  static late Logger _logger;
  
  static void initialize({bool isDebug = false}) {
    _logger = Logger(
      level: isDebug ? Level.debug : Level.info,
      printer: PrettyPrinter(
        methodCount: 2,
        errorMethodCount: 8,
        lineLength: 120,
        colors: true,
        printEmojis: true,
        printTime: true,
      ),
    );
  }
  
  static Logger get instance => _logger;
}

// Uso
final logger = AppLogger.instance;
```

### Filtros y formateo
```dart
Logger loggerWithFilter = Logger(
  filter: ProductionFilter(), // Solo errores en producción
  printer: SimplePrinter(), // Formato simple
  output: FileOutput(), // Guardar en archivo
);
```

## 🏗️ Integración con Arquitectura Clean

### En repositorios (Data Layer)
```dart
class UserRepositoryImpl implements UserRepository {
  final Logger _logger = Logger();
  
  @override
  Future<User> getUser(String id) async {
    try {
      _logger.d('Obteniendo usuario con ID: $id');
      
      final userData = await _apiService.getUser(id);
      _logger.i('Usuario obtenido exitosamente');
      
      return User.fromJson(userData);
    } catch (e, stackTrace) {
      _logger.e('Error al obtener usuario', 
        error: e, 
        stackTrace: stackTrace
      );
      rethrow;
    }
  }
}
```

### En casos de uso (Domain Layer)
```dart
class LoginUseCase {
  final Logger _logger = Logger();
  final UserRepository _userRepository;
  
  Future<Either<Failure, User>> call(LoginParams params) async {
    try {
      _logger.d('Iniciando proceso de login');
      
      final user = await _userRepository.login(params.email, params.password);
      _logger.i('Login exitoso para: ${params.email}');
      
      return Right(user);
    } catch (e, stackTrace) {
      _logger.e('Error en login', error: e, stackTrace: stackTrace);
      return Left(LoginFailure());
    }
  }
}
```

### En widgets (Presentation Layer)
```dart
class LoginPage extends StatelessWidget {
  final Logger _logger = Logger();
  
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Consumer<AuthProvider>(
        builder: (context, authProvider, child) {
          // Log de estados de UI
          _logger.d('Estado de autenticación: ${authProvider.state}');
          
          return authProvider.isLoading 
            ? const CircularProgressIndicator()
            : LoginForm();
        },
      ),
    );
  }
}
```

## 🐛 Problemas Comunes

### Error: No logger instance
```dart
// ❌ Error: Logger no inicializado
final logger = Logger(); // Crear en cada clase

// ✅ Mejor: Singleton o inyección de dependencias
// Opción 1: Singleton
class AppLogger {
  static final Logger _instance = Logger();
  static Logger get instance => _instance;
}

// Opción 2: Inyección de dependencias con get_it
sl.registerLazySingleton<Logger>(() => Logger());
```

### Logs no aparecen en release
```dart
// ✅ Configurar filtro para release
Logger logger = Logger(
  filter: kReleaseMode 
    ? ProductionFilter() // Solo errores en release
    : DevelopmentFilter(), // Todo en debug
);
```

### Performance en producción
```dart
// ✅ Evitar logs costosos en producción
if (kDebugMode) {
  logger.d('Datos complejos: ${expensiveOperation()}');
}
```

## 🚫 Reglas del Proyecto

### PROHIBIDO
```dart
// ❌ NUNCA usar print()
print('Esto está prohibido');
debugPrint('Esto también');

// ❌ NUNCA usar print() ni en desarrollo ni en producción
if (kDebugMode) {
  print('Ni siquiera así');
}
```

### CORRECTO
```dart
// ✅ SIEMPRE usar logger
logger.d('Mensaje de desarrollo');
logger.i('Información importante');
logger.e('Error que debe registrarse');
```

## 📚 Recursos Adicionales

- [Documentación oficial](https://pub.dev/packages/logger)
- [Logger en GitHub](https://github.com/leisim/logger)
- [Ejemplos avanzados](https://pub.dev/packages/logger/example)
- [Best practices logging](https://dart.academy/logging-in-flutter/)

---

💡 **Recordatorio**: En este proyecto, `logger` es OBLIGATORIO y `print()` está PROHIBIDO en cualquier circunstancia.
