import 'dart:convert';
import 'package:http/http.dart' as http;

class ApiService {
  static const String _baseUrl = "http://localhost:5000/api";

  static Future<Map<String, dynamic>> completeQuest(int questId) async {
    final response = await http.post(
      Uri.parse("$_baseUrl/quests/complete"),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({"id": questId}),
    );
    return jsonDecode(response.body);
  }

  static Future<Map<String, dynamic>> getProfile() async {
    final response = await http.get(Uri.parse('$_baseUrl/profile'));
    return jsonDecode(response.body);
  }

  static Future<List<dynamic>> getQuests() async {
    final response = await http.get(Uri.parse('$_baseUrl/quests'));
    return jsonDecode(response.body);
  }

  static Future<List<dynamic>> getHabits() async {
    final response = await http.get(Uri.parse('$_baseUrl/habits'));
    return jsonDecode(response.body);
  }

  static Future<void> updateProfile(Map<String, dynamic> updates) async {
    await http.post(
      Uri.parse('$_baseUrl/profile/update'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode(updates),
    );
  }
}