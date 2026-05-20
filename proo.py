import 'package:flutter/material.dart';

void main() => runApp(const CitizenPulseApp());

class CitizenPulseApp extends StatelessWidget {
  const CitizenPulseApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: "CitizenPulse Report Hub",
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(
          seedColor: Colors.deepOrange,
          primary: Colors.deepOrange.shade800,
          secondary: Colors.amber.shade700,
        ),
        useMaterial3: true,
        scaffoldBackgroundColor: const Color(0xFFF1F5F9),
      ),
      home: const PotholeReportDashboard(),
    );
  }
}

class PotholeReport {
  final String id;
  final String location;
  final String sizeCategory; 
  final String trafficDensity; 
  String status; 
  final String imageUrl;
  final String description;
  final String priorityLevel; 

  PotholeReport({
    required this.id,
    required this.location,
    required this.sizeCategory,
    required this.trafficDensity,
    required this.status,
    required this.imageUrl,
    required this.description,
    required this.priorityLevel,
  });
}

class PotholeReportDashboard extends StatefulWidget {
  const PotholeReportDashboard({super.key});

  @override
  State<PotholeReportDashboard> createState() => _PotholeReportDashboardState();
}

class _PotholeReportDashboardState extends State<PotholeReportDashboard> {
  final List<String> _systemAuditLogs = [
    "--- Infrastructure Communication Core Online ---",
    "[SYS] Bound to local Chrome target compilation channel.",
  ];

  final List<PotholeReport> _globalReportRegistry = [
    PotholeReport(
      id: "REP-104",
      location: "Kolar Main Highway Junction",
      sizeCategory: "Large",
      trafficDensity: "High",
      status: "Dispatched",
      imageUrl: "https://images.unsplash.com/photo-1515162305285-0293e4767cc2?q=80&w=600",
      description: "Deep crater forming right on the double lines. Causes immediate weaving hazards.",
      priorityLevel: "CRITICAL",
    ),
    PotholeReport(
      id: "REP-102",
      location: "4th Cross Lane, Residential Ward 3",
      sizeCategory: "Small",
      trafficDensity: "Low",
      status: "Pending",
      imageUrl: "https://images.unsplash.com/photo-1621259182978-f09e5e2ae16a?q=80&w=600",
      description: "Minor surface wear starting to chip away near the drainage cover.",
      priorityLevel: "LOW",
    )
  ];

  final _locationCtrl = TextEditingController();
  final _descCtrl = TextEditingController();
  
  String _selectedSize = "Medium";
  String _selectedTraffic = "Low";
  
  final List<String> _simulatedPotholePhotos = [
    "https://images.unsplash.com/photo-1599740487739-16f9f3032fbb?q=80&w=600",
    "https://images.unsplash.com/photo-1584467541268-b040f83be3fd?q=80&w=600",
    "https://images.unsplash.com/photo-1613545325278-f24b0cae1224?q=80&w=600"
  ];
  int _photoPointerIndex = 0;

  void _logEvent(String section, String text) {
    final timeStr = DateTime.now().toString().substring(11, 19);
    setState(() {
      _systemAuditLogs.add("[$timeStr] [$section] $text");
    });
  }

  String _calculatePriorityMetrics(String size, String traffic) {
    if (size == "Large" && traffic == "High") return "CRITICAL";
    if (size == "Large" || traffic == "High") return "MEDIUM";
    return "LOW";
  }

  void _advanceReportStatus(PotholeReport report) {
    setState(() {
      if (report.status == "Pending") {
        report.status = "Dispatched";
        _logEvent("WORKFLOW", "${report.id} escalated to [Dispatched]. Maintenance crew assigned.");
      } else if (report.status == "Dispatched") {
        report.status = "Resolved";
        _logEvent("WORKFLOW", "${report.id} transitioned to [Resolved]. Repair completed successfully.");
      }
    });
  }

  void _handleFormSubmission() {
    final locationText = _locationCtrl.text.trim();
    final descriptionText = _descCtrl.text.trim();

    if (locationText.isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(backgroundColor: Colors.amber, content: Text("Validation Blocked: Location data required.")),
      );
      return;
    }

    final computedPriority = _calculatePriorityMetrics(_selectedSize, _selectedTraffic);
    final uniqueId = "REP-${DateTime.now().millisecondsSinceEpoch.toString().substring(9)}";

    setState(() {
      _globalReportRegistry.insert(
        0, 
        PotholeReport(
          id: uniqueId,
          location: locationText,
          sizeCategory: _selectedSize,
          trafficDensity: _selectedTraffic,
          status: "Pending",
          imageUrl: _simulatedPotholePhotos[_photoPointerIndex],
          description: descriptionText.isEmpty ? "No description provided." : descriptionText,
          priorityLevel: computedPriority,
        ),
      );
      _photoPointerIndex = (_photoPointerIndex + 1) % _simulatedPotholePhotos.length;
    });

    _logEvent("DATABASE", "Created new incident ticket entry node: $uniqueId");

    _locationCtrl.clear();
    _descCtrl.clear();
  }

  Color _getStatusColor(String currentStatus) {
    switch (currentStatus) {
      case "Pending": return Colors.amber.shade800;
      case "Dispatched": return Colors.blue.shade700;
      case "Resolved": return Colors.green.shade700;
      default: return Colors.grey;
    }
  }

  IconData _getStatusIcon(String currentStatus) {
    switch (currentStatus) {
      case "Pending": return Icons.hourglass_empty;
      case "Dispatched": return Icons.local_shipping_outlined;
      case "Resolved": return Icons.check_circle_outline_rounded;
      default: return Icons.help_outline;
    }
  }

  @override
  Widget build(BuildContext context) {
    int totalCount = _globalReportRegistry.length;
    int resolvedCount = _globalReportRegistry.where((e) => e.status == "Resolved").length;

    return Scaffold(
      body: Row(
        children: [
          Expanded(
            flex: 4,
            child: Padding(
              padding: const EdgeInsets.all(24.0),
              child: Column(
                children: [
                  Expanded(
                    child: SingleChildScrollView(
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          const Text("Incident Entry Module", style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold, color: Colors.blueGrey)),
                          const SizedBox(height: 16),
                          Card(
                            elevation: 4,
                            shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
                            child: Padding(
                              padding: const EdgeInsets.all(20.0),
                              child: Column(
                                children: [
                                  Container(
                                    height: 160,
                                    width: double.infinity,
                                    decoration: BoxDecoration(
                                      borderRadius: BorderRadius.circular(12),
                                      image: DecorationImage(image: NetworkImage(_simulatedPotholePhotos[_photoPointerIndex]), fit: BoxFit.cover),
                                    ),
                                    alignment: Alignment.bottomCenter,
                                    child: Container(
                                      width: double.infinity, color: Colors.black54, padding: const EdgeInsets.symmetric(vertical: 6),
                                      child: const Text("📸 Simulated Image Buffer Active", textAlign: TextAlign.center, style: TextStyle(color: Colors.white, fontSize: 11)),
                                    ),
                                  ),
                                  const SizedBox(height: 16),
                                  TextField(
                                    controller: _locationCtrl,
                                    decoration: InputDecoration(labelText: "Incident Geographic Location", prefixIcon: const Icon(Icons.location_on_outlined), border: OutlineInputBorder(borderRadius: BorderRadius.circular(12))),
                                  ),
                                  const SizedBox(height: 14),
                                  DropdownButtonFormField<String>(
                                    // FIXED: Swapped 'value' parameter target to 'initialValue' to fix line 233 warnings
                                    initialValue: _selectedSize,
                                    decoration: InputDecoration(labelText: "Pothole Metric Classification", border: OutlineInputBorder(borderRadius: BorderRadius.circular(12))),
                                    items: const [
                                      DropdownMenuItem(value: "Small", child: Text("Small (< 6\" Deep)")),
                                      DropdownMenuItem(value: "Medium", child: Text("Medium (6\"-12\" Deep)")),
                                      DropdownMenuItem(value: "Large", child: Text("Large (> 12\" Deep)")),
                                    ],
                                    onChanged: (val) => setState(() => _selectedSize = val!),
                                  ),
                                  const SizedBox(height: 14),
                                  DropdownButtonFormField<String>(
                                    // FIXED: Swapped 'value' parameter target to 'initialValue' to fix line 244 warnings
                                    initialValue: _selectedTraffic,
                                    decoration: InputDecoration(labelText: "Street Route Volume Density", border: OutlineInputBorder(borderRadius: BorderRadius.circular(12))),
                                    items: const [
                                      DropdownMenuItem(value: "Low", child: Text("Low Traffic Density")),
                                      DropdownMenuItem(value: "High", child: Text("High Traffic Density")),
                                    ],
                                    onChanged: (val) => setState(() => _selectedTraffic = val!),
                                  ),
                                  const SizedBox(height: 14),
                                  TextField(
                                    controller: _descCtrl,
                                    decoration: InputDecoration(labelText: "Ancillary Context Observations", border: OutlineInputBorder(borderRadius: BorderRadius.circular(12))),
                                  ),
                                  const SizedBox(height: 20),
                                  ElevatedButton.icon(
                                    style: ElevatedButton.styleFrom(backgroundColor: Colors.deepOrange.shade800, foregroundColor: Colors.white, minimumSize: const Size(double.infinity, 54), shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12))),
                                    onPressed: _handleFormSubmission,
                                    icon: const Icon(Icons.cloud_upload_outlined),
                                    label: const Text("DISPATCH LIVE TICKET", style: TextStyle(fontWeight: FontWeight.bold)),
                                  )
                                ],
                              ),
                            ),
                          ),
                        ],
                      ),
                    ),
                  ),
                  const SizedBox(height: 16),
                  SizedBox(
                    height: 180,
                    width: double.infinity,
                    child: Card(
                      color: const Color(0xFF1E293B),
                      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                      child: Padding(
                        padding: const EdgeInsets.all(12.0),
                        child: ListView.builder(
                          reverse: true,
                          itemCount: _systemAuditLogs.length,
                          itemBuilder: (context, index) {
                            final inverseIdx = _systemAuditLogs.length - 1 - index;
                            return Padding(
                              padding: const EdgeInsets.symmetric(vertical: 2),
                              child: Text(_systemAuditLogs[inverseIdx], style: const TextStyle(color: Colors.greenAccent, fontFamily: "monospace", fontSize: 11)),
                            );
                          },
                        ),
                      ),
                    ),
                  )
                ],
              ),
            ),
          ),
          const VerticalDivider(width: 1, color: Colors.black12),
          Expanded(
            flex: 6,
            child: Padding(
              padding: const EdgeInsets.all(24.0),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      Text("Active Municipal Framework Incidents", style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold, color: Colors.blueGrey.shade900)),
                      Row(
                        children: [
                          _buildCountBadge("Total Tickets", totalCount, Colors.blueGrey),
                          const SizedBox(width: 12),
                          _buildCountBadge("Resolved Tasks", resolvedCount, Colors.green),
                        ],
                      )
                    ],
                  ),
                  const SizedBox(height: 20),
                  Expanded(
                    child: ListView.builder(
                      itemCount: _globalReportRegistry.length,
                      itemBuilder: (context, index) {
                        final report = _globalReportRegistry[index];
                        final isCritical = report.priorityLevel == "CRITICAL";
                        Color operationalColor = _getStatusColor(report.status);
                        
                        return Card(
                          margin: const EdgeInsets.symmetric(vertical: 8),
                          elevation: 2,
                          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(14)),
                          child: Row(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              Container(
                                width: 140, height: 145,
                                decoration: BoxDecoration(
                                  borderRadius: const BorderRadius.only(topLeft: Radius.circular(14), bottomLeft: Radius.circular(14)),
                                  image: DecorationImage(image: NetworkImage(report.imageUrl), fit: BoxFit.cover),
                                ),
                              ),
                              Expanded(
                                child: Padding(
                                  padding: const EdgeInsets.all(16.0),
                                  child: Column(
                                    crossAxisAlignment: CrossAxisAlignment.start,
                                    children: [
                                      Row(
                                        mainAxisAlignment: MainAxisAlignment.spaceBetween,
                                        children: [
                                          Text(report.id, style: const TextStyle(fontFamily: 'monospace', fontWeight: FontWeight.bold, color: Colors.blueGrey)),
                                          Container(
                                            padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                                            decoration: BoxDecoration(color: isCritical ? Colors.red.shade50 : Colors.blue.shade50, borderRadius: BorderRadius.circular(6)),
                                            child: Text(report.priorityLevel, style: TextStyle(fontSize: 11, fontWeight: FontWeight.bold, color: isCritical ? Colors.red.shade800 : Colors.blue.shade800)),
                                          )
                                        ],
                                      ),
                                      const SizedBox(height: 6),
                                      Text(report.location, style: const TextStyle(fontSize: 15, fontWeight: FontWeight.bold)),
                                      const SizedBox(height: 4),
                                      Text(report.description, maxLines: 1, overflow: TextOverflow.ellipsis, style: const TextStyle(fontSize: 12, color: Colors.grey)),
                                      const SizedBox(height: 14),
                                      Row(
                                        mainAxisAlignment: MainAxisAlignment.spaceBetween,
                                        children: [
                                          Row(
                                            children: [
                                              Icon(_getStatusIcon(report.status), size: 16, color: operationalColor),
                                              const SizedBox(width: 6),
                                              Text(
                                                "Status: ${report.status.toUpperCase()}", 
                                                style: TextStyle(fontSize: 12, fontWeight: FontWeight.bold, color: operationalColor),
                                              ),
                                            ],
                                          ),
                                          if (report.status != "Resolved")
                                            ElevatedButton.icon(
                                              style: ElevatedButton.styleFrom(
                                                backgroundColor: operationalColor.withValues(alpha: 0.1),
                                                foregroundColor: operationalColor,
                                                elevation: 0,
                                                padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
                                                // FIXED: Removed the invalid parameter 'dense' from line 398 to clear the compiler crash
                                              ),
                                              onPressed: () => _advanceReportStatus(report),
                                              icon: const Icon(Icons.next_plan_outlined, size: 14),
                                              label: Text(report.status == "Pending" ? "PROCEED TO DISPATCH" : "MARK AS RESOLVED", style: const TextStyle(fontSize: 11, fontWeight: FontWeight.bold)),
                                            )
                                          else
                                            const Row(
                                              children: [
                                                Icon(Icons.verified_user, size: 14, color: Colors.green),
                                                SizedBox(width: 4),
                                                Text("ARCHIVED / CLOSED", style: TextStyle(fontSize: 11, fontWeight: FontWeight.bold, color: Colors.green)),
                                              ],
                                            )
                                        ],
                                      )
                                    ],
                                  ),
                                ),
                              )