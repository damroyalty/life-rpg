import 'package:hive/hive.dart';
import 'package:latlong2/latlong.dart';

part 'travel_pin.g.dart';

@HiveType(typeId: 2)
class TravelPin extends HiveObject {
  @HiveField(0)
  double lat;

  @HiveField(1)
  double lng;

  @HiveField(2)
  String place;

  @HiveField(3)
  String reason;

  @HiveField(4)
  String notes;

  TravelPin({
    required this.lat,
    required this.lng,
    required this.place,
    this.reason = '',
    this.notes = '',
  });

  LatLng get latlng => LatLng(lat, lng);
  set latlng(LatLng value) {
    lat = value.latitude;
    lng = value.longitude;
  }
}
