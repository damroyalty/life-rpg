import 'package:flutter/material.dart';
import 'package:fl_chart/fl_chart.dart';

class ProfilePortal extends StatelessWidget {
  const ProfilePortal({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Player Profile')),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.center,
          children: [
            CircleAvatar(
              radius: 48,
              backgroundColor: Colors.deepPurple,
              child: Icon(Icons.person, size: 48, color: Colors.white),
            ),
            SizedBox(height: 16),
            Text(
              'Adventurer Name',
              style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
            ),
            SizedBox(height: 8),
            AnimatedContainer(
              duration: Duration(seconds: 1),
              curve: Curves.easeInOut,
              width: double.infinity,
              height: 24,
              decoration: BoxDecoration(
                borderRadius: BorderRadius.circular(12),
                color: Colors.deepPurple[200],
              ),
              child: Stack(
                children: [
                  FractionallySizedBox(
                    widthFactor: 0.7,
                    child: Container(
                      decoration: BoxDecoration(
                        borderRadius: BorderRadius.circular(12),
                        color: Colors.amber,
                      ),
                    ),
                  ),
                  Center(
                    child: Text(
                      'Level 5   XP: 1400/2000',
                      style: TextStyle(
                        color: Colors.black,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                  ),
                ],
              ),
            ),
            SizedBox(height: 16),
            Text(
              'Gold: 320',
              style: TextStyle(fontSize: 18, color: Colors.amberAccent),
            ),
            SizedBox(height: 24),
            Text(
              'Attributes',
              style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
            ),
            SizedBox(height: 8),
            Expanded(
              child: RadarChart(
                RadarChartData(
                  dataSets: [
                    RadarDataSet(
                      dataEntries: [
                        RadarEntry(value: 7),
                        RadarEntry(value: 5),
                        RadarEntry(value: 8),
                        RadarEntry(value: 6),
                        RadarEntry(value: 4),
                        RadarEntry(value: 9),
                      ],
                      borderColor: Colors.deepPurple,
                      fillColor: Colors.deepPurple.withOpacity(0.3),
                    ),
                  ],
                  titleTextStyle: TextStyle(fontSize: 14, color: Colors.white),
                  getTitle: (index, angle) {
                    const labels = [
                      'Strength',
                      'Wisdom',
                      'Charisma',
                      'Endurance',
                      'Dexterity',
                      'Spirit',
                    ];
                    return RadarChartTitle(text: labels[index]);
                  },
                  radarBackgroundColor: Colors.transparent,
                  tickCount: 5,
                  radarBorderData: BorderSide(color: Colors.deepPurpleAccent),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
