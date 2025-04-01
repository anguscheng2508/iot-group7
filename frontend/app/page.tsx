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
    <div className="flex p-10 w-full h-screen">
      <div className="flex-col mr-5 border border-gray-300 p-4 w-1/2 h-full">
        <div className="border-b border-gray-300 pb-4 mb-4 gap-5">
          <h3 className="text-2xl font-semibold">Sensors</h3>
          <div className="flex gap-2">
            {sensors.map((sensor) => (
              <SensorButton key={sensor.name} sensor={sensor} />
            ))}
          </div>
        </div>
        <div className="flex-col gap-5">
          <h3 className="text-2xl font-semibold">Actuators</h3>
          <div className="flex-col gap-2 w-full">
            {actuators.map((actuator) => (
              <ActuatorButton key={actuator.name} actuator={actuator} />
            ))}
          </div>
        </div>
      </div>

      <EventList initEvents={events} />
    </div>
  );
}
