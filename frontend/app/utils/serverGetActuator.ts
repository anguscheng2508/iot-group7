import api from "./api";

export default async function serverGetActuator() {
  const data: Actuator[] = await api.getActuators();
  return data;
}
