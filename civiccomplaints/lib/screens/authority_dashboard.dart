import 'package:flutter/material.dart';
import 'package:civiccomplaints/services/api.dart';
import 'package:url_launcher/url_launcher.dart';

import '../widgets/app_card.dart';
import '../theme/app_colors.dart';

class AuthorityDashboard extends StatefulWidget {
  final String authorityName;
  final String? authorityCategory;

  const AuthorityDashboard({
    super.key,
    required this.authorityName,
    this.authorityCategory,
  });

  @override
  State<AuthorityDashboard> createState() =>
      _AuthorityDashboardState();
}

class _AuthorityDashboardState
    extends State<AuthorityDashboard> {
  static const _authorityToCategory = {
    'water': 'water',
    'water authority': 'water',
    'electricity': 'electricity',
    'electricity authority': 'electricity',
    'road': 'road',
    'road authority': 'road',
    'garbage': 'garbage',
    'garbage authority': 'garbage',
  };

  String _selectedCategory = 'water';
  bool _loading = false;
  String? _error;
  List<Map<String, dynamic>> _complaints = [];
  final Set<int> _expandedItems = {};

  @override
  void initState() {
    super.initState();
    _selectedCategory =
        _inferCategoryFromAuthority(widget.authorityName);
    _loadComplaints();
  }

  String _inferCategoryFromAuthority(String authorityName) {
    final key = authorityName.toLowerCase();
    for (final entry in _authorityToCategory.entries) {
      if (key.contains(entry.key)) return entry.value;
    }
    return 'water';
  }

  Future<void> _loadComplaints() async {
    setState(() {
      _loading = true;
      _error = null;
    });

    final res = await Api.getComplaints(_selectedCategory);

    if (res['ok'] == true && res['data'] is List) {
      setState(() {
        _complaints =
            List<Map<String, dynamic>>.from(res['data']);
        _loading = false;
      });
    } else {
      setState(() {
        _loading = false;
        _error =
            res['error']?.toString() ?? 'Could not load complaints';
        _complaints = [];
      });
    }
  }

  String _niceCategory(String category) =>
      category[0].toUpperCase() + category.substring(1);

  Future<void> _launchMap(
      String latitude, String longitude, String mapLink) async {
    final url = mapLink.isNotEmpty
        ? mapLink
        : 'https://www.google.com/maps?q=$latitude,$longitude';

    final uri = Uri.parse(url);
    if (!await launchUrl(uri)) {
      throw 'Could not launch $url';
    }
  }

  Map<String, String> _parseCitizen(Map<String, dynamic> c) {
    final citizenRaw = c['citizen'];

    String name = 'Unknown';
    String email = 'Unknown';
    String phone = 'Unknown';

    if (citizenRaw is Map) {
      name = citizenRaw['fullname']?.toString() ?? 'Unknown';
      email = citizenRaw['email']?.toString() ?? 'Unknown';
      phone = citizenRaw['phone']?.toString() ?? 'Unknown';
    } else {
      name = c['citizen_name']?.toString() ?? 'Unknown';
      email = c['citizen_email']?.toString() ?? 'Unknown';
      phone = c['citizen_phone']?.toString() ?? 'Unknown';
    }

    return {'name': name, 'email': email, 'phone': phone};
  }

  Widget _buildComplaintCard(
      Map<String, dynamic> c, int index) {
    final status = (c['status'] ?? 'Pending').toString();
    final description = c['description'] ?? '';

    final citizen = _parseCitizen(c);

    final latitude = (c['latitude'] ?? '').toString();
    final longitude = (c['longitude'] ?? '').toString();
    final mapLink = c['map_location'] ?? '';

    final isExpanded = _expandedItems.contains(index);

    // ✅ Status color logic
    Color badgeColor;
    Color textColor;

    switch (status.toLowerCase()) {
      case 'resolved':
        badgeColor = Colors.green.withOpacity(0.2);
        textColor = Colors.green;
        break;
      case 'in progress':
        badgeColor = Colors.blue.withOpacity(0.2);
        textColor = Colors.blue;
        break;
      default:
        badgeColor = Colors.orange.withOpacity(0.2);
        textColor = Colors.orange;
    }

    return AppCard(
      child: InkWell(
        onTap: () {
          setState(() {
            // Toggle expand
            if (isExpanded) {
              _expandedItems.remove(index);
            } else {
              _expandedItems.add(index);
            }

            // ✅ Change status (frontend only)
            final currentStatus =
                (_complaints[index]['status'] ?? '')
                    .toString()
                    .toLowerCase();

            if (currentStatus == 'pending') {
              _complaints[index]['status'] = 'In Progress';
            }
          });
        },
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // 🔹 Header
            Row(
              mainAxisAlignment:
                  MainAxisAlignment.spaceBetween,
              children: [
                Text(
                  _niceCategory(_selectedCategory),
                  style: const TextStyle(
                    fontSize: 16,
                    fontWeight: FontWeight.bold,
                    color: AppColors.textPrimary,
                  ),
                ),

                // 🔹 Status badge
                Container(
                  padding: const EdgeInsets.symmetric(
                      horizontal: 10, vertical: 4),
                  decoration: BoxDecoration(
                    color: badgeColor,
                    borderRadius:
                        BorderRadius.circular(8),
                  ),
                  child: Text(
                    status.toUpperCase(),
                    style: TextStyle(
                      fontSize: 12,
                      fontWeight: FontWeight.bold,
                      color: textColor,
                    ),
                  ),
                ),
              ],
            ),

            if (isExpanded) ...[
              const SizedBox(height: 10),

              Text(
                description,
                style: const TextStyle(
                    color: AppColors.textSecondary),
              ),

              const SizedBox(height: 10),

              Wrap(
                spacing: 8,
                runSpacing: 6,
                children: [
                  Chip(label: Text('👤 ${citizen['name']}')),
                  Chip(label: Text('📧 ${citizen['email']}')),
                  Chip(label: Text('📞 ${citizen['phone']}')),

                  if (latitude.isNotEmpty &&
                      longitude.isNotEmpty)
                    ActionChip(
                      label: const Text('View Map'),
                      onPressed: () => _launchMap(
                          latitude, longitude, mapLink),
                    ),
                ],
              ),
            ],
          ],
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('${widget.authorityName} Dashboard'),
      ),
      body: Container(
        color: AppColors.background,
        child: SafeArea(
          child: _loading
              ? const Center(
                  child: CircularProgressIndicator(),
                )
              : _error != null
                  ? Center(
                      child: Text(
                        'Error: $_error',
                        style: const TextStyle(
                            color: Colors.red),
                      ),
                    )
                  : RefreshIndicator(
                      onRefresh: _loadComplaints,
                      child: _complaints.isEmpty
                          ? Center(
                              child: Text(
                                'No complaints found for ${_niceCategory(_selectedCategory)}.',
                              ),
                            )
                          : ListView.builder(
                              itemCount:
                                  _complaints.length,
                              itemBuilder: (_, i) =>
                                  _buildComplaintCard(
                                      _complaints[i], i),
                            ),
                    ),
        ),
      ),
    );
  }
}