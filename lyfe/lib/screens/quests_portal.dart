import 'package:flutter/material.dart';
import 'package:hive_flutter/hive_flutter.dart';

import '../models/quest.dart';

class QuestsPortal extends StatefulWidget {
  const QuestsPortal({super.key});

  @override
  State<QuestsPortal> createState() => _QuestsPortalState();
}

class _QuestsPortalState extends State<QuestsPortal> {
  late Box<Quest> questBox;

  @override
  void initState() {
    super.initState();
    questBox = Hive.isBoxOpen('quests')
        ? Hive.box<Quest>('quests')
        : Hive.openBox<Quest>('quests') as Box<Quest>;
  }

  void _addQuest() async {
    final titleController = TextEditingController();
    final descController = TextEditingController();
    final xpController = TextEditingController();
    final goldController = TextEditingController();
    final result = await showDialog<Map<String, dynamic>>(
      context: context,
      builder: (context) => AlertDialog(
        title: Text('Add Quest'),
        content: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            TextField(
              controller: titleController,
              decoration: InputDecoration(labelText: 'Quest Title'),
            ),
            TextField(
              controller: descController,
              decoration: InputDecoration(labelText: 'Description'),
            ),
            TextField(
              controller: xpController,
              keyboardType: TextInputType.number,
              decoration: InputDecoration(labelText: 'XP'),
            ),
            TextField(
              controller: goldController,
              keyboardType: TextInputType.number,
              decoration: InputDecoration(labelText: 'Gold'),
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
              final title = titleController.text.trim();
              final desc = descController.text.trim();
              final xp = int.tryParse(xpController.text.trim());
              final gold = int.tryParse(goldController.text.trim());
              if (title.isNotEmpty &&
                  desc.isNotEmpty &&
                  xp != null &&
                  gold != null) {
                Navigator.pop(context, {
                  'title': title,
                  'desc': desc,
                  'xp': xp,
                  'gold': gold,
                });
              }
            },
          ),
        ],
      ),
    );
    if (result != null) {
      setState(() {
        questBox.add(
          Quest(
            title: result['title'],
            desc: result['desc'],
            xp: result['xp'],
            gold: result['gold'],
          ),
        );
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Quests'),
        actions: [
          IconButton(
            icon: Icon(Icons.add),
            tooltip: 'Add Quest',
            onPressed: _addQuest,
          ),
        ],
      ),
      body: ValueListenableBuilder(
        valueListenable: questBox.listenable(),
        builder: (context, Box<Quest> box, _) {
          if (box.isEmpty) {
            return Center(child: Text('No quests yet. Tap + to add.'));
          }
          return ListView.builder(
            itemCount: box.length,
            itemBuilder: (ctx, i) {
              final quest = box.getAt(i)!;
              return Card(
                margin: EdgeInsets.symmetric(vertical: 8, horizontal: 16),
                elevation: 4,
                child: ListTile(
                  leading: Icon(Icons.shield, color: Colors.deepPurple),
                  title: Text(
                    quest.title,
                    style: TextStyle(fontWeight: FontWeight.bold),
                  ),
                  subtitle: Text(quest.desc),
                  trailing: Column(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      Row(
                        mainAxisSize: MainAxisSize.min,
                        children: [
                          Icon(Icons.star, color: Colors.amber, size: 18),
                          Text(' ${quest.xp}'),
                        ],
                      ),
                      Row(
                        mainAxisSize: MainAxisSize.min,
                        children: [
                          Icon(
                            Icons.monetization_on,
                            color: Colors.amberAccent,
                            size: 18,
                          ),
                          Text(' ${quest.gold}'),
                        ],
                      ),
                    ],
                  ),
                  onTap: () {
                    showDialog(
                      context: context,
                      builder: (_) => AlertDialog(
                        title: Text('Quest Complete!'),
                        content: Text(
                          'You have gained ${quest.xp} XP and ${quest.gold} gold!',
                        ),
                        actions: [
                          TextButton(
                            child: Text('Awesome!'),
                            onPressed: () => Navigator.pop(context),
                          ),
                        ],
                      ),
                    );
                  },
                ),
              );
            },
          );
        },
      ),
    );
  }
}
