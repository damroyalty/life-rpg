import 'package:hive/hive.dart';

part 'quest.g.dart';

@HiveType(typeId: 1)
class Quest extends HiveObject {
  @HiveField(0)
  String title;

  @HiveField(1)
  String desc;

  @HiveField(2)
  int xp;

  @HiveField(3)
  int gold;

  Quest({
    required this.title,
    required this.desc,
    required this.xp,
    required this.gold,
  });
}
