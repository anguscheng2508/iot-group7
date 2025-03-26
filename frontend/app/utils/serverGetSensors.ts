import api from "./api";

export default async function serverGetSensors() {
  const data: Sensor[] = await api.getSensors();
  return data;
}
