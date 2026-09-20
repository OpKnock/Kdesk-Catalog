---
type: agent_requested
description: "Flutter mobile development. Real flutter CLI."
---

# flutter

Flutter mobile development. Real flutter CLI.

## Instructions

# Flutter

Flutter mobile development using real CLI.

## When to Use

- Cross-platform mobile apps
- Beautiful UIs
- High-performance apps

## Commands

```bash
# Create project
flutter create my_app

# Run on device
flutter run

# Run on specific device
flutter run -d <device_id>

# List devices
flutter devices

# Build APK
flutter build apk

# Build iOS
flutter build ios

# Run tests
flutter test

# Analyze
flutter analyze

# Clean
flutter clean

# Get packages
flutter pub get

# Upgrade packages
flutter pub upgrade
```

## Widget

```dart
// lib/widgets/user_card.dart
import 'package:flutter/material.dart';

class UserCard extends StatelessWidget {
  final String name;
  final String email;
  
  const UserCard({
    Key? key,
    required this.name,
    required this.email,
  }) : super(key: key);
  
  @override
  Widget build(BuildContext context) {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              name,
              style: const TextStyle(
                fontSize: 18,
                fontWeight: FontWeight.bold,
              ),
            ),
            const SizedBox(height: 8),
            Text(
              email,
              style: const TextStyle(color: Colors.grey),
            ),
          ],
        ),
      ),
    );
  }
}
```

## State Management

```dart
// lib/providers/user_provider.dart
import 'package:flutter/foundation.dart';

class UserProvider extends ChangeNotifier {
  List<User> _users = [];
  bool _loading = false;
  
  List<User> get users => _users;
  bool get loading => _loading;
  
  Future<void> fetchUsers() async {
    _loading = true;
    notifyListeners();
    
    final response = await http.get(Uri.parse('https://api.example.com/users'));
    _users = (jsonDecode(response.body) as List)
        .map((json) => User.fromJson(json))
        .toList();
    
    _loading = false;
    notifyListeners();
  }
}
```

## Navigation

```dart
// lib/main.dart
import 'package:flutter/material.dart';

void main() => runApp(MyApp());

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'My App',
      theme: ThemeData(primarySwatch: Colors.blue),
      home: HomeScreen(),
    );
  }
}

class HomeScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Home')),
      body: Center(
        child: ElevatedButton(
          onPressed: () {
            Navigator.push(
              context,
              MaterialPageRoute(builder: (context) => DetailScreen()),
            );
          },
          child: const Text('Go to Detail'),
        ),
      ),
    );
  }
}
```

## pubspec.yaml

```yaml
name: my_app
description: A new Flutter project.
version: 1.0.0+1

environment:
  sdk: '>=3.0.0 <4.0.0'

dependencies:
  flutter:
    sdk: flutter
  http: ^1.1.0
  provider: ^6.0.0
  
dev_dependencies:
  flutter_test:
    sdk: flutter
  flutter_lints: ^3.0.0
```

## Capabilities

### flutter
Flutter mobile development. Real flutter CLI.

**Commands:**
- `flutter create my_app`
- `flutter run`
- `flutter run -d demo-device-id`
- `flutter devices`
- `flutter build apk`
- `flutter build ios`
- `flutter test`
- `flutter analyze`
- `flutter clean`
- `flutter pub get`
- `flutter pub upgrade`

**Examples:**
- flutter create my_app
- flutter run
- flutter run -d demo-device-id