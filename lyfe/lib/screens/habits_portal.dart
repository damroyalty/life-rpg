import 'package:flutter/material.dart';
import 'package:hive_flutter/hive_flutter.dart';

import '../models/habit.dart';

class HabitsPortal extends StatefulWidget {
  const HabitsPortal({super.key});

  @override
  State<HabitsPortal> createState() => _HabitsPortalState();
}

class _HabitsPortalState extends State<HabitsPortal> {
  late Box<Habit> habitBox;

  @override
  void initState() {
    super.initState();
    habitBox = Hive.box<Habit>('habits');
  }

  void completeHabit(int i) {
    setState(() {
      final habit = habitBox.getAt(i)!;
      habit.streak++;
      if (habit.streak >= habit.goal) {
        showDialog(
          context: context,
          builder: (_) => AlertDialog(
            title: Text('Streak Complete!'),
            content: Text('You gained 100 XP!'),
            actions: [
              TextButton(
                child: Text('Yay!'),
                onPressed: () => Navigator.pop(context),
              ),
            ],
          ),
        );
        habit.streak = 0;
      }
      habit.save();
    });
  }

  void _addHabit() async {
    final nameController = TextEditingController();
    final goalController = TextEditingController();
    final result = await showDialog<Map<String, dynamic>>(
      context: context,
      builder: (context) => AlertDialog(
        title: Text('Add Habit'),
        content: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            TextField(
              controller: nameController,
              decoration: InputDecoration(labelText: 'Habit Name'),
            ),
            TextField(
              controller: goalController,
              keyboardType: TextInputType.number,
              decoration: InputDecoration(labelText: 'Streak Goal (days)'),
            ),
          ],
        ),
        actions: [
          TextButton(
            child: Text('Cancel'),
            onPressed: () => Navigator.pop(context),
          ),
          ElevatedButton(
            child: Text('Add'),
            onPressed: () {
              final name = nameController.text.trim();
              final goal = int.tryParse(goalController.text.trim());
              if (name.isNotEmpty && goal != null && goal > 0) {
                Navigator.pop(context, {'name': name, 'goal': goal});
              }
            },
          ),
        ],
      ),
    );
    if (result != null) {
      setState(() {
        habitBox.add(Habit(name: result['name'], goal: result['goal']));
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Habits Tracker'),
        actions: [
          IconButton(
            icon: Icon(Icons.add),
            tooltip: 'Add Habit',
            onPressed: _addHabit,
          ),
        ],
      ),
      body: ValueListenableBuilder(
        valueListenable: habitBox.listenable(),
        builder: (context, Box<Habit> box, _) {
          if (box.isEmpty) {
            return Center(child: Text('No habits yet. Tap + to add.'));
          }
          return ListView.builder(
            itemCount: box.length,
            itemBuilder: (ctx, i) {
              final habit = box.getAt(i)!;
              double percent = habit.streak / habit.goal;
              return Card(
                margin: EdgeInsets.symmetric(vertical: 8, horizontal: 16),
                child: ListTile(
                  leading: Icon(Icons.repeat, color: Colors.greenAccent),
                  title: Text(
                    habit.name,
                    style: TextStyle(fontWeight: FontWeight.bold),
                  ),
                  subtitle: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      LinearProgressIndicator(
                        value: percent,
                        backgroundColor: Colors.grey[800],
                        color: Colors.greenAccent,
                      ),
                      SizedBox(height: 4),
                      Text('Streak: ${habit.streak} / ${habit.goal}'),
                    ],
                  ),
                  trailing: IconButton(
                    icon: Icon(Icons.check_circle, color: Colors.green),
                    onPressed: () => completeHabit(i),
                  ),
                ),
              );
            },
          );
        },
      ),
    );
  }
}
