import 'package:flutter/material.dart';
import 'package:hive_flutter/hive_flutter.dart';

import 'models/habit.dart';
import 'models/quest.dart';
import 'models/travel_pin.dart';
import 'screens/home_screen.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await Hive.initFlutter();
  Hive.registerAdapter(HabitAdapter());
  Hive.registerAdapter(QuestAdapter());
  Hive.registerAdapter(TravelPinAdapter());
  await Hive.openBox<Habit>('habits');
  await Hive.openBox<Quest>('quests');
  await Hive.openBox<TravelPin>('travel_pins');
  runApp(LifeRPG());
}

class LifeRPG extends StatelessWidget {
  const LifeRPG({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Lyfe RPG',
      debugShowCheckedModeBanner: false,
      theme: ThemeData.dark().copyWith(
        primaryColor: Colors.deepPurpleAccent,
        scaffoldBackgroundColor: Colors.grey[900],
      ),
      home: HomeScreen(),
    );
  }
}
