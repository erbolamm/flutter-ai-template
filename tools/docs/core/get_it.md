# Get_it

## 📋 Información General
- **Versión**: ^8.0.3
- **Propósito**: Service Locator / Inyección de dependencias para Dart y Flutter
- **Documentación oficial**: [pub.dev/packages/get_it](https://pub.dev/packages/get_it)
- **Patrón**: Singleton para acceso global a servicios

## 🚀 Instalación

Ya incluido en `pubspec.yaml`:
```yaml
dependencies:
  get_it: ^8.0.3
```

## 💡 Uso Básico

### Setup inicial
```dart
// lib/core/di/service_locator.dart
import 'package:get_it/get_it.dart';

final GetIt sl = GetIt.instance;

Future<void> setupServiceLocator() async {
  // Registrar servicios
  await _registerCore();
  await _registerRepositories();
  await _registerUseCases();
}

Future<void> _registerCore() async {
  // Logger (singleton)
  sl.registerLazySingleton<Logger>(() => Logger());
  
  // HTTP Client
  sl.registerLazySingleton<http.Client>(() => http.Client());
}
```

### Tipos de registro

```dart
// Singleton - Una instancia para toda la app
sl.registerSingleton<DatabaseService>(DatabaseService());

// Lazy Singleton - Se crea cuando se necesita por primera vez
sl.registerLazySingleton<ApiService>(() => ApiService(sl()));

// Factory - Nueva instancia cada vez
sl.registerFactory<UserViewModel>(() => UserViewModel(sl()));
```

## ⚙️ Configuración Avanzada

### Service Locator completo
```dart
// lib/core/di/service_locator.dart
import 'package:get_it/get_it.dart';
import 'package:logger/logger.dart';
import 'package:http/http.dart' as http;

final GetIt sl = GetIt.instance;

Future<void> setupServiceLocator() async {
  // === CORE SERVICES ===
  _registerCoreServices();
  
  // === DATA SOURCES ===
  _registerDataSources();
  
  // === REPOSITORIES ===
  _registerRepositories();
  
  // === USE CASES ===
  _registerUseCases();
  
  // === PROVIDERS/VIEWMODELS ===
  _registerViewModels();
}

void _registerCoreServices() {
  // Logger singleton
  sl.registerLazySingleton<Logger>(() => Logger());
  
  // HTTP Client
  sl.registerLazySingleton<http.Client>(() => http.Client());
  
  // SharedPreferences
  sl.registerLazySingletonAsync<SharedPreferences>(
    () => SharedPreferences.getInstance()
  );
}

void _registerDataSources() {
  // API Data Source
  sl.registerLazySingleton<UserApiDataSource>(
    () => UserApiDataSourceImpl(sl(), sl()) // http.Client, Logger
  );
  
  // Local Data Source
  sl.registerLazySingleton<UserLocalDataSource>(
    () => UserLocalDataSourceImpl(sl()) // SharedPreferences
  );
}

void _registerRepositories() {
  // Repository (implementación)
  sl.registerLazySingleton<UserRepository>(
    () => UserRepositoryImpl(
      apiDataSource: sl(),
      localDataSource: sl(),
      logger: sl(),
    )
  );
}

void _registerUseCases() {
  // Use Cases
  sl.registerLazySingleton(() => LoginUseCase(sl()));
  sl.registerLazySingleton(() => GetUserProfileUseCase(sl()));
  sl.registerLazySingleton(() => LogoutUseCase(sl()));
}

void _registerViewModels() {
  // ViewModels/Providers (factory - nueva instancia cada vez)
  sl.registerFactory<AuthProvider>(() => AuthProvider(
    loginUseCase: sl(),
    logoutUseCase: sl(),
    logger: sl(),
  ));
}
```

### Inicialización en main.dart
```dart
// lib/main.dart
import 'core/di/service_locator.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  
  // Setup service locator
  await setupServiceLocator();
  
  // Esperar servicios asíncronos si es necesario
  await sl.allReady();
  
  runApp(MyApp());
}
```

## 🏗️ Integración con Clean Architecture

### Repository Pattern
```dart
// domain/repositories/user_repository.dart
abstract class UserRepository {
  Future<User> getUser(String id);
  Future<void> saveUser(User user);
}

// data/repositories/user_repository_impl.dart
class UserRepositoryImpl implements UserRepository {
  final UserApiDataSource _apiDataSource;
  final UserLocalDataSource _localDataSource;
  final Logger _logger;
  
  // Constructor con dependencias inyectadas
  UserRepositoryImpl({
    required UserApiDataSource apiDataSource,
    required UserLocalDataSource localDataSource,
    required Logger logger,
  }) : _apiDataSource = apiDataSource,
       _localDataSource = localDataSource,
       _logger = logger;

  @override
  Future<User> getUser(String id) async {
    _logger.d('UserRepository: Obteniendo usuario $id');
    // Implementación...
  }
}

// Registro en service locator
sl.registerLazySingleton<UserRepository>(
  () => UserRepositoryImpl(
    apiDataSource: sl(),
    localDataSource: sl(),
    logger: sl(),
  )
);
```

### Use Cases con inyección
```dart
// domain/usecases/login_usecase.dart
class LoginUseCase {
  final UserRepository _repository;
  final Logger _logger;
  
  LoginUseCase(this._repository, this._logger);
  
  Future<Either<Failure, User>> call(LoginParams params) async {
    _logger.d('LoginUseCase: Iniciando login');
    return await _repository.login(params.email, params.password);
  }
}

// Registro
sl.registerLazySingleton(() => LoginUseCase(sl(), sl()));
```

### Provider con inyección
```dart
// presentation/providers/auth_provider.dart
class AuthProvider extends ChangeNotifier {
  final LoginUseCase _loginUseCase;
  final LogoutUseCase _logoutUseCase;
  final Logger _logger;
  
  AuthProvider({
    required LoginUseCase loginUseCase,
    required LogoutUseCase logoutUseCase,
    required Logger logger,
  }) : _loginUseCase = loginUseCase,
       _logoutUseCase = logoutUseCase,
       _logger = logger;
       
  // Métodos del provider...
}

// Uso en Widget
class LoginPage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return ChangeNotifierProvider(
      create: (_) => sl<AuthProvider>(), // Inyección automática
      child: Consumer<AuthProvider>(
        builder: (context, authProvider, child) {
          // UI...
        },
      ),
    );
  }
}
```

## 🐛 Problemas Comunes

### Error: Object not registered
```dart
// ❌ Error: Servicio no registrado
final userRepo = sl<UserRepository>(); // GetItError

// ✅ Solución: Verificar registro
void _registerRepositories() {
  sl.registerLazySingleton<UserRepository>(
    () => UserRepositoryImpl(sl(), sl())
  );
}
```

### Dependencias circulares
```dart
// ❌ Error: A depende de B, B depende de A
sl.registerLazySingleton<ServiceA>(() => ServiceA(sl<ServiceB>()));
sl.registerLazySingleton<ServiceB>(() => ServiceB(sl<ServiceA>()));

// ✅ Solución: Refactorizar arquitectura o usar interfaces
abstract class IServiceA { }
abstract class IServiceB { }

sl.registerLazySingleton<IServiceA>(() => ServiceA(sl<IServiceB>()));
sl.registerLazySingleton<IServiceB>(() => ServiceB());
```

### Testing y mocking
```dart
// En tests, resetear y mockear
void setUp() {
  sl.reset(); // Limpiar registros anteriores
  
  // Registrar mocks
  sl.registerLazySingleton<UserRepository>(() => MockUserRepository());
}
```

## 🔍 Verificación y Debugging

### Verificar registros
```dart
void debugServiceLocator() {
  print('Servicios registrados: ${sl.allRegisteredNames}');
  print('¿UserRepository registrado?: ${sl.isRegistered<UserRepository>()}');
}
```

### Lazy vs Eager loading
```dart
// Lazy - Se crea cuando se pide por primera vez
sl.registerLazySingleton<ExpensiveService>(() => ExpensiveService());

// Eager - Se crea inmediatamente
final service = ExpensiveService();
sl.registerSingleton<ExpensiveService>(service);
```

## 📚 Recursos Adicionales

- [Documentación oficial](https://pub.dev/packages/get_it)
- [Get_it en GitHub](https://github.com/fluttercommunity/get_it)
- [Dependency Injection patterns](https://dart.academy/dependency-injection-in-flutter/)
- [Clean Architecture con get_it](https://resocoder.com/flutter-clean-architecture-tdd/)

---

💡 **Tip**: Organiza el service locator por capas (core → data → domain → presentation) para mantener las dependencias claras.
