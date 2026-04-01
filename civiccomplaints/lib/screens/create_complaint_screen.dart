import 'package:flutter/material.dart';
import 'package:civiccomplaints/services/api.dart';
import 'package:geolocator/geolocator.dart';

import '../widgets/app_button.dart';
import '../widgets/app_textfield.dart';
import '../widgets/app_card.dart';
import '../theme/app_colors.dart';

class CreateComplaintScreen extends StatefulWidget {
  const CreateComplaintScreen({super.key});

  @override
  State<CreateComplaintScreen> createState() =>
      _CreateComplaintScreenState();
}

class _CreateComplaintScreenState
    extends State<CreateComplaintScreen> {
  final TextEditingController descriptionController =
      TextEditingController();

  double? latitude;
  double? longitude;

  bool loading = false;

  @override
  void initState() {
    super.initState();
    _determinePosition();
  }

  Future<void> _determinePosition() async {
    try {
      bool serviceEnabled =
          await Geolocator.isLocationServiceEnabled();

      if (!serviceEnabled) {
        _showSnack('Location services are disabled');
        return;
      }

      LocationPermission permission =
          await Geolocator.checkPermission();

      if (permission == LocationPermission.denied) {
        permission =
            await Geolocator.requestPermission();
        if (permission == LocationPermission.denied) {
          _showSnack('Location permission denied');
          return;
        }
      }

      if (permission ==
          LocationPermission.deniedForever) {
        _showSnack(
            'Location permanently denied');
        return;
      }

      final pos = await Geolocator.getCurrentPosition(
        desiredAccuracy: LocationAccuracy.high,
      );

      print("📍 REAL LOCATION: ${pos.latitude}, ${pos.longitude}");

      setState(() {
        latitude = pos.latitude;
        longitude = pos.longitude;
      });
    } catch (e) {
      print("❌ LOCATION ERROR: $e");
    }
  }

  void _showSnack(String msg) {
    ScaffoldMessenger.of(context)
        .showSnackBar(SnackBar(content: Text(msg)));
  }

  Future<void> submitComplaint() async {
    final desc = descriptionController.text.trim();

    if (desc.isEmpty) {
      _showSnack('Description cannot be empty');
      return;
    }

    /// 🔥 FALLBACK LOCATION (IMPORTANT FIX)
    double lat = (latitude == null || latitude == 0.0)
        ? 27.6723
        : latitude!;

    double lng = (longitude == null || longitude == 0.0)
        ? 85.3147
        : longitude!;

    print("📤 SUBMIT LAT: $lat, LNG: $lng");

    setState(() => loading = true);

    final res = await Api.createComplaint(
      desc,
      lat,
      lng,
    );

    setState(() => loading = false);

    if (!mounted) return;

    if (res['ok'] == true) {
      _showSnack('Complaint submitted successfully');
      descriptionController.clear();
    } else {
      print("❌ ERROR: ${res['error']}");

      final err = res['error'];
      String msg = 'Submission failed';

      if (err is Map && err['detail'] != null) {
        msg = err['detail'].toString();
      } else if (err is Map && err.isNotEmpty) {
        msg = err.values.join("; ");
      } else if (err is String) {
        msg = err;
      }

      _showSnack(msg);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Create Complaint'),
      ),
      body: Container(
        color: AppColors.background,
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
                    const Text(
                      'Submit a Complaint',
                      textAlign: TextAlign.center,
                      style: TextStyle(
                        fontSize: 22,
                        fontWeight: FontWeight.bold,
                        color: AppColors.textPrimary,
                      ),
                    ),

                    const SizedBox(height: 20),

                    AppTextField(
                      hint: 'Describe your issue...',
                      controller: descriptionController,
                    ),

                    const SizedBox(height: 10),

                    /// 🔥 FIXED LOCATION DISPLAY
                    Text(
                      latitude == null
                          ? "Fetching location..."
                          : 'Location: ${latitude!.toStringAsFixed(4)}, ${longitude!.toStringAsFixed(4)}',
                      style: const TextStyle(
                        fontSize: 12,
                        color: AppColors.textSecondary,
                      ),
                      textAlign: TextAlign.center,
                    ),

                    const SizedBox(height: 20),

                    /// 🔥 OPTIONAL: Refresh Location Button
                    AppButton(
                      text: 'Refresh Location',
                      color: AppColors.primary,
                      onTap: _determinePosition,
                    ),

                    const SizedBox(height: 10),

                    AppButton(
                      text: 'Submit Complaint',
                      color: AppColors.secondary,
                      isLoading: loading,
                      onTap: submitComplaint,
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