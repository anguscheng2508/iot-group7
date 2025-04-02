import axios from "axios";

// const backendApi = "https://8601-89-101-47-26.ngrok-free.app";
const backendApi = "http://localhost:8000";

const hardwareApi = {
  getSensors: async () => {
    return axios.get(`${backendApi}/sensor`).then((response) => {
      if (response.status === 200) {
        return response.data;
      } else {
        throw Error("Failed to get sensors.");
      }
    });
  },
  getActuators: async () => {
    return axios.get(`${backendApi}/actuator`).then((response) => {
      if (response.status === 200) {
        return response.data;
      } else {
        throw Error("Failed to get actuators.");
      }
    });
  },
  putActuatorStatus: async (actuator: Actuator) => {
    return axios.put(`${backendApi}/actuator/${actuator.type}`, actuator).then((response) => {
      if (response.status === 200) {
        return response.data;
      } else {
        throw Error("Failed to update actuator status.");
      }
    });
  },
};

const dataApi = {
  getSensorData: async (sensorId: string) => {
    return axios.get(`${backendApi}/sensor-data/${sensorId}`).then((response) => {
      if (response.status === 200) {
        return response.data;
      } else {
        throw Error("Failed to get sensor data.");
      }
    });
  },

  getEventData: async (): Promise<IEvent[]> => {
    return axios.get(`${backendApi}/event`).then((response) => {
      if (response.status === 200) {
        return response.data.map((event: any) => {
          return {
            ...event,
            deviceName: event["device_name"],
          } as IEvent;
        });
      } else {
        throw Error("Failed to get events.");
      }
    });
  },
};

const defaultExport = {
  ...hardwareApi,
  ...dataApi,
};

export default defaultExport;
