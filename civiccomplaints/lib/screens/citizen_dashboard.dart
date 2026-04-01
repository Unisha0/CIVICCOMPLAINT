import 'package:flutter/material.dart';

import '../widgets/app_button.dart';
import '../widgets/app_card.dart';
import '../theme/app_colors.dart';

import 'create_complaint_screen.dart';

class CitizenDashboard extends StatelessWidget {
  final String citizenName;

  const CitizenDashboard({
    super.key,
    required this.citizenName,
  });

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Citizen Dashboard'),
      ),

      body: Container(
        width: double.infinity,

        // ✅ Theme background
        decoration: const BoxDecoration(
          color: Color.fromARGB(255, 250, 247, 245),
        ),

        child: SafeArea(
          child: Padding(
            padding: const EdgeInsets.all(16),
            child: Column(
              children: [
                // 🔹 Welcome Card
                AppCard(
                  child: Column(
                    children: [
                      const Icon(
                        Icons.person,
                        size: 50,
                        color: AppColors.primary,
                      ),
                      const SizedBox(height: 10),
                      Text(
                        'Welcome, $citizenName!',
                        textAlign: TextAlign.center,
                        style: const TextStyle(
                          fontSize: 20,
                          fontWeight: FontWeight.bold,
                          color: AppColors.textPrimary,
                        ),
                      ),
                    ],
                  ),
                ),

                const SizedBox(height: 20),

                // 🔹 Actions Card
                AppCard(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.stretch,
                    children: [
                      const Text(
                        'Quick Actions',
                        style: TextStyle(
                          fontSize: 18,
                          fontWeight: FontWeight.bold,
                          color: AppColors.textPrimary,
                        ),
                      ),

                      const SizedBox(height: 15),

                      // ✅ Create Complaint
                      AppButton(
                        text: 'Create Complaint',
                        color: AppColors.secondary,
                        icon: Icons.add,
                        onTap: () {
                          Navigator.push(
                            context,
                            MaterialPageRoute(
                              builder: (_) =>
                                  const CreateComplaintScreen(),
                            ),
                          );
                        },
                      ),

                      const SizedBox(height: 12),

                    ],
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}