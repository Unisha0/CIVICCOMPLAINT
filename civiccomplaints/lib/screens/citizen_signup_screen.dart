import 'package:flutter/material.dart';
import 'package:civiccomplaints/services/api.dart';

import '../widgets/app_button.dart';
import '../widgets/app_textfield.dart';
import '../widgets/app_card.dart';
import '../theme/app_colors.dart';

import 'login_screen.dart';

class CitizenSignupScreen extends StatefulWidget {
  const CitizenSignupScreen({super.key});

  @override
  State<CitizenSignupScreen> createState() =>
      _CitizenSignupScreenState();
}

class _CitizenSignupScreenState
    extends State<CitizenSignupScreen> {
  final nameController = TextEditingController();
  final emailController = TextEditingController();
  final phoneController = TextEditingController();
  final passwordController = TextEditingController();

  bool isLoading = false;

  void handleSignup() {
    _doSignup();
  }

  Future<void> _doSignup() async {
    final fullName = nameController.text.trim();
    final email = emailController.text.trim();
    final phone = phoneController.text.trim();
    final password = passwordController.text;

    if (fullName.isEmpty ||
        email.isEmpty ||
        phone.isEmpty ||
        password.isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('All fields are required')),
      );
      return;
    }

    setState(() => isLoading = true);

    final res = await Api.signup(fullName, phone, email, password);

    setState(() => isLoading = false);

    if (res['ok'] == true) {
      Navigator.pushReplacement(
        context,
        MaterialPageRoute(
          builder: (_) => LoginScreen(
            role: 'citizen',
            initialEmail: email,
            initialPassword: password,
            autoLogin: true,
          ),
        ),
      );
    } else {
      final err = res['error'];
      String msg = 'Signup failed';

      if (err is Map) {
        if (err.containsKey('non_field_errors')) {
          msg = err['non_field_errors'].toString();
        } else if (err.containsKey('email')) {
          msg = err['email'].toString();
        } else {
          msg = err.toString();
        }
      } else if (err is String) {
        msg = err.trim().startsWith('<') ? 'Server error' : err;
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
              padding:
                  const EdgeInsets.symmetric(horizontal: 20),
              child: AppCard(
                child: Column(
                  crossAxisAlignment:
                      CrossAxisAlignment.stretch,
                  children: [
                    // 🔹 Title
                    const Text(
                      'Citizen Signup',
                      textAlign: TextAlign.center,
                      style: TextStyle(
                        fontSize: 26,
                        fontWeight: FontWeight.bold,
                        color: AppColors.textPrimary,
                      ),
                    ),

                    const SizedBox(height: 20),

                    // 🔹 Name
                    AppTextField(
                      hint: 'Full Name',
                      controller: nameController,
                      icon: Icons.person,
                    ),

                    // 🔹 Email
                    AppTextField(
                      hint: 'Email',
                      controller: emailController,
                      icon: Icons.email,
                    ),

                    // 🔹 Phone
                    AppTextField(
                      hint: 'Phone (97/98xxxxxxx)',
                      controller: phoneController,
                      keyboardType: TextInputType.phone,
                      icon: Icons.phone,
                    ),

                    // 🔹 Password
                    AppTextField(
                      hint: 'Password',
                      controller: passwordController,
                      obscure: true,
                      icon: Icons.lock,
                    ),

                    const SizedBox(height: 20),

                    // 🔹 Signup Button
                    AppButton(
                      text: 'Signup',
                      color: AppColors.secondary,
                      isLoading: isLoading,
                      onTap: handleSignup,
                    ),

                    const SizedBox(height: 15),

                    // 🔹 Back to login
                    GestureDetector(
                      onTap: () => Navigator.pop(context),
                      child: const Text(
                        "Already have an account? Login",
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