import 'package:flutter/material.dart';
import 'profile_portal.dart';
import 'quests_portal.dart';
import 'habits_portal.dart';
import 'agenda_portal.dart';
import 'awakening_portal.dart';
import 'reward_center.dart';
import 'travel_map_screen.dart';
import 'memento_mori_screen.dart';

class HomeScreen extends StatelessWidget {
  const HomeScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final List<Map<String, dynamic>> portals = [
      {'name': 'Profile', 'widget': ProfilePortal()},
      {'name': 'Quests', 'widget': QuestsPortal()},
      {'name': 'Habits', 'widget': HabitsPortal()},
      {'name': 'Agenda', 'widget': AgendaPortal()},
      {'name': 'Awakening', 'widget': AwakeningPortal()},
      {'name': 'Rewards', 'widget': RewardCenter()},
      {'name': 'Travel Map', 'widget': TravelMapScreen()},
      {'name': 'Memento Mori', 'widget': MementoMoriScreen()},
    ];
    return Scaffold(
      appBar: AppBar(title: Text('Life RPG Portal Hub')),
      body: ListView.builder(
        itemCount: portals.length,
        itemBuilder: (ctx, index) {
          return ListTile(
            title: Text(portals[index]['name']),
            trailing: Icon(Icons.arrow_forward_ios),
            onTap: () {
              Navigator.of(context).push(
                MaterialPageRoute(builder: (_) => portals[index]['widget']),
              );
            },
          );
        },
      ),
    );
  }
}
