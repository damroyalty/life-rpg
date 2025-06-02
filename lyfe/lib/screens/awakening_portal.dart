import 'package:flutter/material.dart';

class AwakeningPortal extends StatelessWidget {
  const AwakeningPortal({super.key});

  @override
  Widget build(BuildContext context) {
    final List<Map<String, String>> achievements = [
      {'title': 'First Awakening', 'desc': 'Reached Level 5!'},
      {'title': 'Streak Master', 'desc': 'Completed 7-day habit streak.'},
      {'title': 'Quest Conqueror', 'desc': 'Completed 10 quests.'},
    ];
    return Scaffold(
      appBar: AppBar(title: Text('Awakening & Achievements')),
      body: ListView.builder(
        itemCount: achievements.length,
        itemBuilder: (ctx, i) {
          return Card(
            margin: EdgeInsets.symmetric(vertical: 8, horizontal: 16),
            child: ListTile(
              leading: Icon(Icons.emoji_events, color: Colors.amber),
              title: Text(
                achievements[i]['title']!,
                style: TextStyle(fontWeight: FontWeight.bold),
              ),
              subtitle: Text(achievements[i]['desc']!),
              trailing: Icon(Icons.check_circle, color: Colors.greenAccent),
            ),
          );
        },
      ),
    );
  }
}
