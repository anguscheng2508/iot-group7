import ActuatorButton from "./components/ActuatorButton";
import EventList from "./components/EventList";
import SensorButton from "./components/SensorButton";
import serverGetActuator from "./utils/serverGetActuator";
import serverGetSensors from "./utils/serverGetSensors";
import serverGetEvents from "./utils/serverGetEvents";

export default async function Home() {
  const actuators = await serverGetActuator();
  const sensors = await serverGetSensors();
  const events = await serverGetEvents();
  return (
    <div className="flex p-10 w-full">
      <div className="flex-col mr-5 border border-gray-300 p-4 w-1/2">
        <div className="border-b border-gray-300 pb-4 mb-4">
          <h3 className="text-lg font-semibold">Sensors</h3>
          {sensors.map((sensor) => (
            <SensorButton key={sensor.name} {...sensor} />
          ))}
        </div>
        <div>
          <h3 className="text-lg font-semibold">Actuators</h3>
          {actuators.map((actuator) => (
            <ActuatorButton key={actuator.name} {...actuator} />
          ))}
        </div>
      </div>
      <div className="flex-1 border border-gray-300 p-4">
        <EventList initEvents={events} />
      </div>
    </div>
  );
}
