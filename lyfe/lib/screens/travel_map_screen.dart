import 'package:flutter/material.dart';
import 'package:flutter_map/flutter_map.dart';
import 'package:latlong2/latlong.dart';
import 'package:hive_flutter/hive_flutter.dart';
import '../models/travel_pin.dart';

class TravelMapScreen extends StatefulWidget {
  const TravelMapScreen({super.key});

  @override
  State<TravelMapScreen> createState() => _TravelMapScreenState();
}

class _TravelMapScreenState extends State<TravelMapScreen> {
  late Box<TravelPin> pinBox;
  int? _draggingPinIndex;

  @override
  void initState() {
    super.initState();
    pinBox = Hive.box<TravelPin>('travel_pins');
  }

  void _addPin(LatLng latlng) async {
    final details = await showDialog<Map<String, String>>(
      context: context,
      builder: (context) {
        final TextEditingController placeController = TextEditingController();
        final TextEditingController reasonController = TextEditingController();
        final TextEditingController notesController = TextEditingController();
        return AlertDialog(
          title: Text('Log a Place'),
          content: SingleChildScrollView(
            child: Column(
              children: [
                TextField(
                  controller: placeController,
                  decoration: InputDecoration(labelText: 'Place Name'),
                ),
                TextField(
                  controller: reasonController,
                  decoration: InputDecoration(labelText: 'Reason/Plan'),
                ),
                TextField(
                  controller: notesController,
                  decoration: InputDecoration(labelText: 'Details/Notes'),
                ),
              ],
            ),
          ),
          actions: [
            TextButton(
              child: Text('Cancel'),
              onPressed: () => Navigator.pop(context),
            ),
            ElevatedButton(
              child: Text('Add'),
              onPressed: () {
                Navigator.pop(context, {
                  'place': placeController.text,
                  'reason': reasonController.text,
                  'notes': notesController.text,
                });
              },
            ),
          ],
        );
      },
    );
    if (details != null && details['place']!.isNotEmpty) {
      setState(() {
        pinBox.add(
          TravelPin(
            lat: latlng.latitude,
            lng: latlng.longitude,
            place: details['place']!,
            reason: details['reason'] ?? '',
            notes: details['notes'] ?? '',
          ),
        );
      });
    }
  }

  void _editPin(int index) async {
    final pin = pinBox.getAt(index)!;
    final placeController = TextEditingController(text: pin.place);
    final reasonController = TextEditingController(text: pin.reason);
    final notesController = TextEditingController(text: pin.notes);
    final result = await showDialog<Map<String, String>>(
      context: context,
      builder: (context) => AlertDialog(
        title: Text('Edit Place'),
        content: SingleChildScrollView(
          child: Column(
            children: [
              TextField(
                controller: placeController,
                decoration: InputDecoration(labelText: 'Place Name'),
              ),
              TextField(
                controller: reasonController,
                decoration: InputDecoration(labelText: 'Reason/Plan'),
              ),
              TextField(
                controller: notesController,
                decoration: InputDecoration(labelText: 'Details/Notes'),
              ),
            ],
          ),
        ),
        actions: [
          TextButton(
            child: Text('Cancel'),
            onPressed: () => Navigator.pop(context),
          ),
          ElevatedButton(
            child: Text('Save'),
            onPressed: () {
              Navigator.pop(context, {
                'place': placeController.text,
                'reason': reasonController.text,
                'notes': notesController.text,
              });
            },
          ),
        ],
      ),
    );
    if (result != null && result['place']!.isNotEmpty) {
      setState(() {
        pin.place = result['place']!;
        pin.reason = result['reason'] ?? '';
        pin.notes = result['notes'] ?? '';
        pin.save();
      });
    }
  }

  void _deletePin(int index) {
    setState(() {
      pinBox.deleteAt(index);
    });
  }

  void _movePin(int index, LatLng latlng) {
    setState(() {
      final pin = pinBox.getAt(index)!;
      pin.lat = latlng.latitude;
      pin.lng = latlng.longitude;
      pin.save();
      _draggingPinIndex = null;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Travel Map')),
      body: ValueListenableBuilder(
        valueListenable: pinBox.listenable(),
        builder: (context, Box<TravelPin> box, _) {
          return FlutterMap(
            options: MapOptions(
              initialCenter: LatLng(20, 0),
              initialZoom: 2.0,
              onTap: (tapPosition, latlng) {
                if (_draggingPinIndex != null) {
                  _movePin(_draggingPinIndex!, latlng);
                } else {
                  _addPin(latlng);
                }
              },
            ),
            children: [
              TileLayer(
                urlTemplate:
                    'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
                subdomains: ['a', 'b', 'c'],
                userAgentPackageName: 'com.example.lyfe',
              ),
              MarkerLayer(
                markers: [
                  for (int i = 0; i < box.length; i++)
                    Marker(
                      width: 40,
                      height: 40,
                      point: box.getAt(i)!.latlng,
                      child: GestureDetector(
                        onTap: () {
                          showDialog(
                            context: context,
                            builder: (_) => AlertDialog(
                              title: Text(box.getAt(i)!.place),
                              content: Column(
                                mainAxisSize: MainAxisSize.min,
                                crossAxisAlignment: CrossAxisAlignment.start,
                                children: [
                                  if (box.getAt(i)!.reason.isNotEmpty)
                                    Text('Reason: ${box.getAt(i)!.reason}'),
                                  if (box.getAt(i)!.notes.isNotEmpty)
                                    Text('Notes: ${box.getAt(i)!.notes}'),
                                ],
                              ),
                              actions: [
                                TextButton(
                                  child: Text('Edit'),
                                  onPressed: () {
                                    Navigator.pop(context);
                                    _editPin(i);
                                  },
                                ),
                                TextButton(
                                  child: Text(
                                    'Delete',
                                    style: TextStyle(color: Colors.red),
                                  ),
                                  onPressed: () {
                                    Navigator.pop(context);
                                    _deletePin(i);
                                  },
                                ),
                                TextButton(
                                  child: Text(
                                    _draggingPinIndex == i
                                        ? 'Tap Map to Place'
                                        : 'Move',
                                  ),
                                  onPressed: () {
                                    setState(() {
                                      _draggingPinIndex = i;
                                    });
                                    Navigator.pop(context);
                                  },
                                ),
                                TextButton(
                                  child: Text('Close'),
                                  onPressed: () => Navigator.pop(context),
                                ),
                              ],
                            ),
                          );
                        },
                        child: Icon(
                          _draggingPinIndex == i
                              ? Icons.location_searching
                              : Icons.location_on,
                          color: _draggingPinIndex == i
                              ? Colors.blue
                              : Colors.redAccent,
                          size: 32,
                        ),
                      ),
                    ),
                ],
              ),
            ],
          );
        },
      ),
    );
  }
}
