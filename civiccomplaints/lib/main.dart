import 'package:flutter/material.dart';
import 'screens/choose_role_screen.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Complaint App',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        primarySwatch: Colors.blue,
        // ✅ Set default app font to a font that supports both Nepali and English
        fontFamily: 'NotoDevanagari', 
        textTheme: const TextTheme(
          bodyMedium: TextStyle(fontSize: 16), // Default body text
          bodyLarge: TextStyle(fontSize: 18),
          titleLarge: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
        ),
      ),
      home: const ChooseRoleScreen(), // First screen
    );
  }
}