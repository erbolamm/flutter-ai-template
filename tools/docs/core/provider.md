# Provider

## 📋 Información General
- **Versión**: ^6.1.2
- **Propósito**: Manejo de estado declarativo para Flutter
- **Documentación oficial**: [pub.dev/packages/provider](https://pub.dev/packages/provider)
- **Patrón**: InheritedWidget mejorado con notificaciones reactivas

## 🚀 Instalación

Ya incluido en `pubspec.yaml`:
```yaml
dependencies:
  provider: ^6.1.2
```

## 💡 Uso Básico

### ChangeNotifier básico
```dart
// lib/presentation/providers/counter_provider.dart
import 'package:flutter/material.dart';
import 'package:logger/logger.dart';

class CounterProvider extends ChangeNotifier {
  final Logger _logger = Logger();
  
  int _count = 0;
  int get count => _count;
  
  void increment() {
    _count++;
    _logger.d('Contador incrementado a: $_count');
    notifyListeners(); // Notifica cambios a la UI
  }
  
  void decrement() {
    _count--;
    _logger.d('Contador decrementado a: $_count');
    notifyListeners();
  }
  
  void reset() {
    _count = 0;
    _logger.i('Contador reiniciado');
    notifyListeners();
  }
}
```

### Uso en Widget
```dart
// lib/presentation/pages/counter_page.dart
class CounterPage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Contador')),
      body: ChangeNotifierProvider(
        create: (_) => CounterProvider(),
        child: Consumer<CounterProvider>(
          builder: (context, counterProvider, child) {
            return Center(
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Text(
                    'Contador: ${counterProvider.count}',
                    style: Theme.of(context).textTheme.headlineMedium,
                  ),
                  SizedBox(height: 20),
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                    children: [
                      ElevatedButton(
                        onPressed: counterProvider.decrement,
                        child: Text('-'),
                      ),
                      ElevatedButton(
                        onPressed: counterProvider.increment,
                        child: Text('+'),
                      ),
                    ],
                  ),
                ],
              ),
            );
          },
        ),
      ),
    );
  }
}
```

## ⚙️ Configuración Avanzada

### Provider con inyección de dependencias
```dart
// lib/presentation/providers/auth_provider.dart
import 'package:flutter/material.dart';
import 'package:logger/logger.dart';
import '../../domain/usecases/login_usecase.dart';
import '../../domain/usecases/logout_usecase.dart';
import '../../domain/entities/user.dart';

class AuthProvider extends ChangeNotifier {
  final LoginUseCase _loginUseCase;
  final LogoutUseCase _logoutUseCase;
  final Logger _logger;
  
  // Constructor con inyección de dependencias
  AuthProvider({
    required LoginUseCase loginUseCase,
    required LogoutUseCase logoutUseCase,
    required Logger logger,
  }) : _loginUseCase = loginUseCase,
       _logoutUseCase = logoutUseCase,
       _logger = logger;

  // Estados
  AuthState _state = AuthState.initial;
  AuthState get state => _state;
  
  User? _currentUser;
  User? get currentUser => _currentUser;
  
  String? _errorMessage;
  String? get errorMessage => _errorMessage;
  
  bool get isLoading => _state == AuthState.loading;
  bool get isAuthenticated => _state == AuthState.authenticated;
  
  // Métodos
  Future<void> login(String email, String password) async {
    _setState(AuthState.loading);
    
    try {
      _logger.d('AuthProvider: Iniciando login para $email');
      
      final result = await _loginUseCase(LoginParams(
        email: email,
        password: password,
      ));
      
      result.fold(
        (failure) {
          _errorMessage = failure.message;
          _setState(AuthState.error);
          _logger.e('AuthProvider: Error en login - ${failure.message}');
        },
        (user) {
          _currentUser = user;
          _errorMessage = null;
          _setState(AuthState.authenticated);
          _logger.i('AuthProvider: Login exitoso para ${user.email}');
        },
      );
    } catch (e, stackTrace) {
      _errorMessage = 'Error inesperado durante el login';
      _setState(AuthState.error);
      _logger.e('AuthProvider: Excepción en login', 
        error: e, stackTrace: stackTrace);
    }
  }
  
  Future<void> logout() async {
    try {
      _logger.d('AuthProvider: Cerrando sesión');
      await _logoutUseCase();
      
      _currentUser = null;
      _errorMessage = null;
      _setState(AuthState.unauthenticated);
      _logger.i('AuthProvider: Sesión cerrada exitosamente');
    } catch (e, stackTrace) {
      _logger.e('AuthProvider: Error en logout', 
        error: e, stackTrace: stackTrace);
    }
  }
  
  void _setState(AuthState newState) {
    _state = newState;
    notifyListeners();
  }
  
  void clearError() {
    _errorMessage = null;
    notifyListeners();
  }
}

enum AuthState {
  initial,
  loading,
  authenticated,
  unauthenticated,
  error,
}
```

### MultiProvider para múltiples providers
```dart
// lib/main.dart
import 'package:provider/provider.dart';
import 'core/di/service_locator.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await setupServiceLocator();
  
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MultiProvider(
      providers: [
        // Provider con inyección de dependencias
        ChangeNotifierProvider(
          create: (_) => sl<AuthProvider>(),
        ),
        
        // Provider que depende de otro provider
        ChangeNotifierProxyProvider<AuthProvider, ProfileProvider>(
          create: (_) => sl<ProfileProvider>(),
          update: (_, authProvider, profileProvider) {
            return profileProvider!..updateUser(authProvider.currentUser);
          },
        ),
        
        // Provider de solo lectura
        Provider<ConfigService>(
          create: (_) => sl<ConfigService>(),
        ),
        
        // Stream provider para datos en tiempo real
        StreamProvider<List<Notification>>(
          create: (_) => sl<NotificationService>().notificationsStream,
          initialData: const [],
        ),
      ],
      child: MaterialApp(
        title: 'Mi App Flutter',
        home: AuthWrapper(),
      ),
    );
  }
}
```

## 🏗️ Integración con Clean Architecture

### Wrapper de autenticación
```dart
// lib/presentation/widgets/auth_wrapper.dart
class AuthWrapper extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Consumer<AuthProvider>(
      builder: (context, authProvider, child) {
        switch (authProvider.state) {
          case AuthState.loading:
            return const LoadingScreen();
            
          case AuthState.authenticated:
            return const MainScreen();
            
          case AuthState.unauthenticated:
          case AuthState.error:
            return const LoginScreen();
            
          default:
            return const SplashScreen();
        }
      },
    );
  }
}
```

### Selector para optimización
```dart
// Escuchar solo cambios específicos
class UserProfile extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Selector<AuthProvider, User?>(
      selector: (_, authProvider) => authProvider.currentUser,
      builder: (context, user, child) {
        if (user == null) return Text('Usuario no disponible');
        
        return Column(
          children: [
            Text('Nombre: ${user.name}'),
            Text('Email: ${user.email}'),
          ],
        );
      },
    );
  }
}
```

## 🐛 Problemas Comunes

### Error: Provider not found
```dart
// ❌ Error: Trying to read a provider outside of its scope
final authProvider = Provider.of<AuthProvider>(context);

// ✅ Solución: Asegurar que el provider esté en el árbol de widgets
class MyWidget extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return ChangeNotifierProvider(
      create: (_) => AuthProvider(),
      child: Consumer<AuthProvider>(
        builder: (context, authProvider, child) {
          return Text('Estado: ${authProvider.state}');
        },
      ),
    );
  }
}
```

### Ciclos infinitos con notifyListeners()
```dart
// ❌ Error: Llamar notifyListeners en build
class BadProvider extends ChangeNotifier {
  int _count = 0;
  int get count {
    notifyListeners(); // ❌ Ciclo infinito
    return _count;
  }
}

// ✅ Solución: Solo llamar en métodos de acción
class GoodProvider extends ChangeNotifier {
  int _count = 0;
  int get count => _count; // Solo getter
  
  void increment() {
    _count++;
    notifyListeners(); // ✅ Correcto
  }
}
```

### Memory leaks con streams/listeners
```dart
class MyProvider extends ChangeNotifier {
  StreamSubscription? _subscription;
  
  MyProvider() {
    _subscription = someStream.listen((data) {
      // Manejar datos
      notifyListeners();
    });
  }
  
  @override
  void dispose() {
    _subscription?.cancel(); // ✅ Limpiar recursos
    super.dispose();
  }
}
```

## 📚 Recursos Adicionales

- [Documentación oficial](https://pub.dev/packages/provider)
- [Provider en GitHub](https://github.com/rrousselGit/provider)
- [State Management Guide](https://docs.flutter.dev/development/data-and-backend/state-mgmt)
- [Provider Best Practices](https://flutter.dev/docs/development/data-and-backend/state-mgmt/simple)

---

💡 **Tip**: Usa `Selector` en lugar de `Consumer` cuando solo necesites escuchar cambios específicos para optimizar rendimiento.
