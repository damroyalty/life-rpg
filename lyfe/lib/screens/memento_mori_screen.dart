import 'package:flutter/material.dart';
import 'package:intl/intl.dart';
import 'package:hive_flutter/hive_flutter.dart';

class MementoMoriScreen extends StatefulWidget {
  const MementoMoriScreen({super.key});

  @override
  State<MementoMoriScreen> createState() => _MementoMoriScreenState();
}

class _MementoMoriScreenState extends State<MementoMoriScreen> {
  DateTime? birthDate;
  int? deathAge;
  static const int weeksInYear = 52;
  static const int maxYears = 120;

  final birthController = TextEditingController();
  final deathAgeController = TextEditingController();

  @override
  void initState() {
    super.initState();
    _loadFromHive();
  }

  Future<void> _loadFromHive() async {
    await Hive.initFlutter();
    var box = await Hive.openBox('mementoMori');
    final birth = box.get('birthDate');
    final death = box.get('deathAge');
    if (birth != null) {
      birthDate = DateTime.tryParse(birth);
      birthController.text = birthDate != null
          ? DateFormat('yyyy-MM-dd').format(birthDate!)
          : '';
    }
    if (death != null) {
      deathAge = death;
      deathAgeController.text = death.toString();
    }
    setState(() {});
  }

  Future<void> _saveToHive() async {
    var box = await Hive.openBox('mementoMori');
    await box.put('birthDate', birthDate?.toIso8601String());
    await box.put('deathAge', deathAge);
  }

  List<Widget> _buildMementoGrid() {
    if (birthDate == null || deathAge == null) return [];
    final now = DateTime.now();
    final totalWeeks = deathAge! * weeksInYear;
    final livedWeeks = now.difference(birthDate!).inDays ~/ 7;
    List<Widget> rows = [];
    for (int year = 0; year < deathAge!; year++) {
      List<Widget> weekRow = [];
      for (int week = 0; week < weeksInYear; week++) {
        int idx = year * weeksInYear + week;
        final isLived = idx < livedWeeks;
        final isValid = idx < totalWeeks;
        weekRow.add(
          Container(
            margin: const EdgeInsets.all(0.5),
            width: 8,
            height: 8,
            decoration: BoxDecoration(
              color: isValid
                  ? (isLived ? Colors.black : Colors.grey[300])
                  : Colors.transparent,
              borderRadius: BorderRadius.circular(2),
            ),
          ),
        );
      }
      rows.add(
        Row(
          mainAxisSize: MainAxisSize.min,
          children: [
            ...weekRow,
            if ((year + 1) % 5 == 0)
              Padding(
                padding: const EdgeInsets.only(left: 8.0),
                child: Text(
                  '${year + 1}',
                  style: TextStyle(
                    fontSize: 16,
                    color: Colors.deepPurple,
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ),
          ],
        ),
      );
    }
    return rows;
  }

  @override
  Widget build(BuildContext context) {
    final lived = (birthDate != null && deathAge != null)
        ? DateTime.now().difference(birthDate!).inDays ~/ 7
        : 0;
    final total = (deathAge ?? 0) * weeksInYear;
    return Scaffold(
      appBar: AppBar(title: Text('Memento Mori')),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            TextField(
              controller: birthController,
              readOnly: true,
              style: TextStyle(fontSize: 16, color: Colors.white),
              decoration: InputDecoration(
                labelText: 'Birth date',
                labelStyle: TextStyle(color: Colors.deepPurpleAccent),
                floatingLabelBehavior: FloatingLabelBehavior.auto,
                filled: true,
                fillColor: Colors.grey[900],
                enabledBorder: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(12),
                  borderSide: BorderSide(
                    color: Colors.deepPurpleAccent,
                    width: 1.5,
                  ),
                ),
                focusedBorder: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(12),
                  borderSide: BorderSide(color: Colors.amber, width: 2),
                ),
                contentPadding: EdgeInsets.symmetric(
                  vertical: 14,
                  horizontal: 16,
                ),
              ),
              onTap: () async {
                final picked = await showDatePicker(
                  context: context,
                  initialDate: DateTime(2000),
                  firstDate: DateTime(1900),
                  lastDate: DateTime.now(),
                );
                if (picked != null) {
                  setState(() {
                    birthDate = picked;
                    birthController.text = DateFormat(
                      'yyyy-MM-dd',
                    ).format(picked);
                  });
                  await _saveToHive();
                }
              },
            ),
            SizedBox(height: 10),
            TextField(
              controller: deathAgeController,
              keyboardType: TextInputType.number,
              style: TextStyle(fontSize: 16, color: Colors.white),
              decoration: InputDecoration(
                labelText: 'Expected age at death',
                labelStyle: TextStyle(color: Colors.deepPurpleAccent),
                floatingLabelBehavior: FloatingLabelBehavior.auto,
                filled: true,
                fillColor: Colors.grey[900],
                enabledBorder: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(12),
                  borderSide: BorderSide(
                    color: Colors.deepPurpleAccent,
                    width: 1.5,
                  ),
                ),
                focusedBorder: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(12),
                  borderSide: BorderSide(color: Colors.amber, width: 2),
                ),
                contentPadding: EdgeInsets.symmetric(
                  vertical: 14,
                  horizontal: 16,
                ),
              ),
              onChanged: (val) async {
                final age = int.tryParse(val);
                if (age != null && age > 0 && age <= maxYears) {
                  setState(() {
                    deathAge = age;
                  });
                  await _saveToHive();
                }
              },
            ),
            if (birthDate != null && deathAge != null)
              Row(
                children: [
                  Spacer(),
                  Padding(
                    padding: const EdgeInsets.only(
                      top: 8.0,
                      right: 4.0,
                      bottom: 8.0,
                    ),
                    child: Text(
                      'Scroll down to see all years.',
                      style: TextStyle(
                        fontSize: 12,
                        color: Colors.deepPurple,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                  ),
                ],
              ),
            SizedBox(height: 8),
            if (birthDate != null && deathAge != null)
              Expanded(
                child: SingleChildScrollView(
                  scrollDirection: Axis.horizontal,
                  child: SingleChildScrollView(
                    scrollDirection: Axis.vertical,
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        ..._buildMementoGrid(),
                        SizedBox(height: 16),
                        Container(
                          padding: EdgeInsets.all(8),
                          decoration: BoxDecoration(
                            color: Colors.deepPurple.withOpacity(0.08),
                            borderRadius: BorderRadius.circular(8),
                          ),
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              Text(
                                'Key:',
                                style: TextStyle(fontWeight: FontWeight.bold),
                              ),
                              Row(
                                children: [
                                  Container(
                                    width: 16,
                                    height: 16,
                                    color: Colors.black,
                                  ),
                                  SizedBox(width: 6),
                                  Text(
                                    '= Week lived',
                                    style: TextStyle(fontSize: 12),
                                  ),
                                  SizedBox(width: 16),
                                  Container(
                                    width: 16,
                                    height: 16,
                                    color: Colors.grey[300],
                                  ),
                                  SizedBox(width: 6),
                                  Text(
                                    '= Week left',
                                    style: TextStyle(fontSize: 12),
                                  ),
                                ],
                              ),
                              SizedBox(height: 4),
                              Text(
                                'Each row = 1 year (52 weeks).',
                                style: TextStyle(fontSize: 12),
                              ),
                              Text(
                                'Each square = 1 week.',
                                style: TextStyle(fontSize: 12),
                              ),
                              Text(
                                'Every 5th year is marked on the right.',
                                style: TextStyle(fontSize: 12),
                              ),
                            ],
                          ),
                        ),
                      ],
                    ),
                  ),
                ),
              ),
          ],
        ),
      ),
    );
  }
}
