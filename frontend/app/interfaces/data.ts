// Enum for SensorType
enum SensorType {
  TEMPERATURE = "Temperature",
  HUMIDITY = "Humidity",
  DISTANCE = "Distance",
  CO2 = "CO2",
}

// Enum for ActuatorType
enum ActuatorType {
  PUMP = "Pump",
  ALARM = "Alarm",
  LIGHT = "Light",
  WINDOW = "Window",
  FAN = "Fan",
}

// Interface for Event
// Avoid name collision with Event class
interface IEvent {
  deviceName: SensorType | ActuatorType;
  description: string;
  timestamp?: Date; // Optional field
}

// Interface for SensorData
interface SensorData {
  sensor: SensorType;
  timestamp?: Date; // Optional field
  value: number;
}

// Interface for Sensor
interface Sensor {
  name: string;
  type: SensorType;
}

// Interface for Actuator
interface Actuator {
  name: string;
  type: ActuatorType;
  status: boolean;
}
