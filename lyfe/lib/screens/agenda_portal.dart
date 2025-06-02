import 'package:flutter/material.dart';
import 'package:table_calendar/table_calendar.dart';

class AgendaPortal extends StatefulWidget {
  const AgendaPortal({super.key});

  @override
  State<AgendaPortal> createState() => _AgendaPortalState();
}

class _AgendaPortalState extends State<AgendaPortal> {
  DateTime _focusedDay = DateTime.now();
  DateTime? _selectedDay;
  final Map<DateTime, List<String>> _events = {
    DateTime.utc(2025, 5, 31): ['Quest: Slay the Procrastination Dragon'],
    DateTime.utc(2025, 6, 1): ['Habit: Morning Ritual'],
    DateTime.utc(2025, 6, 2): ['Holiday: Festival of Light'],
  };

  List<String> _getEventsForDay(DateTime day) {
    return _events[DateTime.utc(day.year, day.month, day.day)] ?? [];
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Agenda & Calendar')),
      body: Column(
        children: [
          TableCalendar(
            firstDay: DateTime.utc(2025, 1, 1),
            lastDay: DateTime.utc(2026, 12, 31),
            focusedDay: _focusedDay,
            selectedDayPredicate: (day) => isSameDay(_selectedDay, day),
            onDaySelected: (selectedDay, focusedDay) {
              setState(() {
                _selectedDay = selectedDay;
                _focusedDay = focusedDay;
              });
            },
            eventLoader: _getEventsForDay,
            calendarStyle: CalendarStyle(
              todayDecoration: BoxDecoration(
                color: Colors.deepPurple,
                shape: BoxShape.circle,
              ),
              selectedDecoration: BoxDecoration(
                color: Colors.amber,
                shape: BoxShape.circle,
              ),
            ),
          ),
          SizedBox(height: 16),
          Expanded(
            child: ListView(
              children: _getEventsForDay(_selectedDay ?? _focusedDay)
                  .map(
                    (e) => ListTile(
                      leading: Icon(Icons.event, color: Colors.deepPurple),
                      title: Text(e),
                    ),
                  )
                  .toList(),
            ),
          ),
        ],
      ),
    );
  }
}
