// lib/services/api.dart

import 'dart:convert';
import 'dart:io' show Platform;
import 'package:flutter/foundation.dart';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';

// Backend URL
final String backendBaseUrl =
    kIsWeb || Platform.isWindows
        ? 'http://localhost:8000'
        : 'http://10.0.2.2:8000';

class Api {
  /// LOGI
  static Future<Map<String, dynamic>> login(
      String email, String password, String role) async {
    final url = Uri.parse('$backendBaseUrl/accounts/login/');

    try {
      final res = await http.post(
        url,
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'email': email,
          'password': password,
          'role': role,
        }),
      );

      final data = _tryDecode(res.body);

      if (res.statusCode == 200) {
        final prefs = await SharedPreferences.getInstance();
        if (data['access'] != null) {
          await prefs.setString('access_token', data['access']);
        }
        return {'ok': true, 'data': data};
      }

      return {'ok': false, 'error': data};
    } catch (e) {
      return {'ok': false, 'error': e.toString()};
    }
  }

  /// SIGNUP
  static Future<Map<String, dynamic>> signup(
      String fullName, String phone, String email, String password) async {
    final url = Uri.parse('$backendBaseUrl/citizen/signup/');

    try {
      final res = await http.post(
        url,
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'fullname': fullName,
          'phone': phone,
          'email': email,
          'password': password,
        }),
      );

      final data = _tryDecode(res.body);

      if (res.statusCode == 200 || res.statusCode == 201) {
        return {'ok': true, 'data': data};
      }

      return {'ok': false, 'error': data};
    } catch (e) {
      return {'ok': false, 'error': e.toString()};
    }
  }

  /// 🔥 CREATE COMPLAINT (FULLY FIXED)
  static Future<Map<String, dynamic>> createComplaint(
    String description,
    double? latitude,
    double? longitude,
  ) async {
    final prefs = await SharedPreferences.getInstance();
    final token = prefs.getString('access_token');

    final url = Uri.parse('$backendBaseUrl/complaint/submit/');

    /// ✅ Fallback location (if null or 0)
    double lat = (latitude == null || latitude == 0.0)
        ? 27.677393303618295
        : latitude;

    double lng = (longitude == null || longitude == 0.0)
        ? 85.33224919328894
        : longitude;

    /// 🌐 LANGUAGE DETECTION
    String detectedLanguage = _detectLanguage(description);

    final bodyData = {
      'description': description,
      'latitude': lat.toString(),   // 🔥 IMPORTANT FIX
      'longitude': lng.toString(), // 🔥 IMPORTANT FIX
      'language': detectedLanguage,
    };

    final headers = {
      'Content-Type': 'application/json',
    };

    if (token != null) {
      headers['Authorization'] = 'Bearer $token';
    }

    try {
      /// 🔍 DEBUG LOGS (VERY IMPORTANT)
      print("📤 URL: $url");
      print("📤 TOKEN: $token");
      print("📤 BODY: ${jsonEncode(bodyData)}");

      final res = await http.post(
        url,
        headers: headers,
        body: jsonEncode(bodyData),
      );

      print("📥 STATUS: ${res.statusCode}");
      print("📥 RESPONSE: ${res.body}");

      final data = _tryDecode(res.body);

      if (res.statusCode == 200 || res.statusCode == 201) {
        return {'ok': true, 'data': data};
      }

      return {'ok': false, 'error': data};
    } catch (e) {
      print("❌ ERROR: $e");
      return {'ok': false, 'error': e.toString()};
    }
  }

  /// GET COMPLAINTS
  static Future<Map<String, dynamic>> getComplaints(
      String category) async {
    final prefs = await SharedPreferences.getInstance();
    final token = prefs.getString('access_token');

    final url =
        Uri.parse('$backendBaseUrl/api/complaint/authority/$category/');

    final headers = {
      'Content-Type': 'application/json',
    };

    if (token != null) {
      headers['Authorization'] = 'Bearer $token';
    }

    try {
      final res = await http.get(url, headers: headers);
      final data = _tryDecode(res.body);

      if (res.statusCode == 200) {
        return {'ok': true, 'data': data};
      }

      return {'ok': false, 'error': data};
    } catch (e) {
      return {'ok': false, 'error': e.toString()};
    }
  }

  /// 🌐 DETECT LANGUAGE (Devanagari = Nepali, else English)
  static String _detectLanguage(String text) {
    final devanagariRegex =
        RegExp(r'[\u0900-\u097F]'); // Nepali/Hindi Devanagari range
    return devanagariRegex.hasMatch(text) ? 'ne' : 'en';
  }

  /// JSON helper
  static dynamic _tryDecode(String src) {
    try {
      return jsonDecode(src);
    } catch (_) {
      return src;
    }
  }
}