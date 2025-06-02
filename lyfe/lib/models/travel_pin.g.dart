
part of 'travel_pin.dart';

class TravelPinAdapter extends TypeAdapter<TravelPin> {
  @override
  final int typeId = 2;

  @override
  TravelPin read(BinaryReader reader) {
    final numOfFields = reader.readByte();
    final fields = <int, dynamic>{
      for (int i = 0; i < numOfFields; i++) reader.readByte(): reader.read(),
    };
    return TravelPin(
      lat: fields[0] as double,
      lng: fields[1] as double,
      place: fields[2] as String,
      reason: fields[3] as String,
      notes: fields[4] as String,
    );
  }

  @override
  void write(BinaryWriter writer, TravelPin obj) {
    writer
      ..writeByte(5)
      ..writeByte(0)
      ..write(obj.lat)
      ..writeByte(1)
      ..write(obj.lng)
      ..writeByte(2)
      ..write(obj.place)
      ..writeByte(3)
      ..write(obj.reason)
      ..writeByte(4)
      ..write(obj.notes);
  }

  @override
  int get hashCode => typeId.hashCode;

  @override
  bool operator ==(Object other) =>
      identical(this, other) ||
      other is TravelPinAdapter &&
          runtimeType == other.runtimeType &&
          typeId == other.typeId;
}
