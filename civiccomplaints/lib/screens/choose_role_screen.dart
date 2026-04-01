import 'package:flutter/material.dart';
import '../widgets/app_button.dart';
import '../theme/app_colors.dart';
import 'login_screen.dart';

class ChooseRoleScreen extends StatelessWidget {
  const ChooseRoleScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Container(
        // ✅ Clean background using theme color
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
          child: Padding(
            padding: const EdgeInsets.symmetric(horizontal: 30.0),
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                // ✅ Title
                const Text(
                  'Civic Complaints',
                  textAlign: TextAlign.center,
                  style: TextStyle(
                    fontSize: 32,
                    fontWeight: FontWeight.bold,
                    color: Colors.white,
                  ),
                ),
                

                // ✅ Citizen Button (using AppButton)
                AppButton(
                  text: 'Citizen',
                  color: AppColors.secondary,
                  onTap: () {
                    Navigator.push(
                      context,
                      MaterialPageRoute(
                        builder: (_) =>
                            const LoginScreen(role: 'citizen'),
                      ),
                    );
                  },
                ),

                const SizedBox(height: 20),

                // ✅ Authority Button
                AppButton(
                  text: 'Authority',
                  color: AppColors.secondary,
                  onTap: () {
                    Navigator.push(
                      context,
                      MaterialPageRoute(
                        builder: (_) =>
                            const LoginScreen(role: 'authority'),
                      ),
                    );
                  },
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}