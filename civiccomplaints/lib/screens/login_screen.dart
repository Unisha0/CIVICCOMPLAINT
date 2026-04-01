import 'package:flutter/material.dart';
import 'package:civiccomplaints/services/api.dart';

import '../widgets/app_button.dart';
import '../widgets/app_textfield.dart';
import '../widgets/app_card.dart';
import '../theme/app_colors.dart';

import 'citizen_dashboard.dart';
import 'authority_dashboard.dart';
import 'citizen_signup_screen.dart';

class LoginScreen extends StatefulWidget {
  final String role;
  final String? initialEmail;
  final String? initialPassword;
  final bool autoLogin;

  const LoginScreen({
    super.key,
    required this.role,
    this.initialEmail,
    this.initialPassword,
    this.autoLogin = false,
  });

  @override
  State<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  final emailController = TextEditingController();
  final passwordController = TextEditingController();

  bool isLoading = false;

  @override
  void initState() {
    super.initState();
    if (widget.initialEmail != null) emailController.text = widget.initialEmail!;
    if (widget.initialPassword != null) passwordController.text = widget.initialPassword!;
    if (widget.autoLogin) {
      WidgetsBinding.instance.addPostFrameCallback((_) {
        _doLogin();
      });
    }
  }

  void handleLogin() {
    _doLogin();
  }

  Future<void> _doLogin() async {
    final email = emailController.text.trim();
    final password = passwordController.text;

    if (email.isEmpty || password.isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Email and password are required')),
      );
      return;
    }

    setState(() => isLoading = true);

    final res = await Api.login(email, password, widget.role);

    setState(() => isLoading = false);

    if (res['ok'] == true) {
      if (widget.role == 'citizen') {
        Navigator.pushReplacement(
          context,
          MaterialPageRoute(
            builder: (_) => CitizenDashboard(citizenName: email),
          ),
        );
      } else {
        Navigator.pushReplacement(
          context,
          MaterialPageRoute(
            builder: (_) => AuthorityDashboard(authorityName: email),
          ),
        );
      }
    } else {
      final error = res['error'];
      String msg = 'Login failed';

      if (error is Map) {
        if (error.containsKey('error')) {
          msg = error['error'].toString();
        } else if (error.containsKey('detail')) {
          msg = error['detail'].toString();
        } else {
          msg = error.toString();
        }
      } else if (error is String) {
        msg = error.trim().startsWith('<') ? 'Server error' : error;
      }

      ScaffoldMessenger.of(context)
          .showSnackBar(SnackBar(content: Text(msg)));
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Container(
        // ✅ Theme-based background
        decoration: const BoxDecoration(
          gradient: LinearGradient(
            colors: [
              AppColors.primary,
              AppColors.primary,
            ],
            begin: Alignment.topLeft,
            end: Alignment.bottomRight,
          ),
        ),

        child: Center(
          child: SingleChildScrollView(
            child: Padding(
              padding: const EdgeInsets.symmetric(horizontal: 20),
              child: AppCard(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.stretch,
                  children: [
                    // 🔹 Title
                    Text(
                      widget.role == 'citizen'
                          ? 'Citizen Login'
                          : 'Authority Login',
                      textAlign: TextAlign.center,
                      style: const TextStyle(
                        fontSize: 26,
                        fontWeight: FontWeight.bold,
                        color: AppColors.textPrimary,
                      ),
                    ),

                    const SizedBox(height: 25),

                    // 🔹 Email
                    AppTextField(
                      hint: 'Email or ID',
                      controller: emailController,
                      icon: Icons.person,
                    ),

                    // 🔹 Password
                    AppTextField(
                      hint: 'Password',
                      controller: passwordController,
                      obscure: true,
                      icon: Icons.lock,
                    ),

                    const SizedBox(height: 20),

                    // 🔹 Login Button
                    AppButton(
                      text: 'Login',
                      color: AppColors.secondary,
                      isLoading: isLoading,
                      onTap: handleLogin,
                    ),

                    const SizedBox(height: 15),

                    // 🔹 Signup (only citizen)
                    if (widget.role == 'citizen')
                      GestureDetector(
                        onTap: () {
                          Navigator.push(
                            context,
                            MaterialPageRoute(
                              builder: (_) => CitizenSignupScreen(),
                            ),
                          );
                        },
                        child: const Text(
                          "Don't have an account? Signup",
                          textAlign: TextAlign.center,
                          style: TextStyle(
                            color: AppColors.primary,
                            fontSize: 14,
                            decoration: TextDecoration.underline,
                          ),
                        ),
                      ),
                  ],
                ),
              ),
            ),
          ),
        ),
      ),
    );
  }
}