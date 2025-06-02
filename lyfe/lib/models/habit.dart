import 'package:hive/hive.dart';

part 'habit.g.dart';

@HiveType(typeId: 0)
class Habit extends HiveObject {
  @HiveField(0)
  String name;

  @HiveField(1)
  int streak;

  @HiveField(2)
  int goal;

  Habit({required this.name, this.streak = 0, required this.goal});
}
