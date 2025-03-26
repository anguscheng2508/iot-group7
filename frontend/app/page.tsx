import ActuatorButton from "./components/ActuatorButton";
import SensorButton from "./components/SensorButton";
import serverGetActuator from "./utils/serverGetActuator";
import serverGetSensors from "./utils/serverGetSensors";

export default async function Home() {
  const actuators = await serverGetActuator();
  const sensors = await serverGetSensors();
  console.log(actuators);
  console.log(sensors);
  return (
    <div className="flex m-5 w-full">
      <div className="flex-col mr-5 border border-gray-300 p-4 w-4/6">
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
      <div className="flex-1 border border-gray-300 p-4"></div>
    </div>
  );
}
