import axios from "axios";

const backendApi = "https://4ac9-134-226-214-244.ngrok-free.app";
// const backendApi = "http://localhost:8000";

// Create an Axios instance
const api = axios.create({
  baseURL: backendApi,
  headers: {
    "ngrok-skip-browser-warning": "true",
  },
});

const hardwareApi = {
  getSensors: async () => {
    return api.get(`${backendApi}/sensor`).then((response) => {
      if (response.status === 200) {
        return response.data;
      } else {
        throw Error("Failed to get sensors.");
      }
    });
  },
  getActuators: async () => {
    return api.get(`${backendApi}/actuator`).then((response) => {
      if (response.status === 200) {
        return response.data;
      } else {
        throw Error("Failed to get actuators.");
      }
    });
  },
  putActuatorStatus: async (actuator: Actuator, status: ActuatorStatus) => {
    return api
      .put(`${backendApi}/actuator/${actuator.type}`, null, {
        params: { action: status, request_from: "user_interface" },
      })
      .then((response) => {
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
    return api.get(`${backendApi}/sensor-data/${sensorId}`).then((response) => {
      if (response.status === 200) {
        return response.data;
      } else {
        throw Error("Failed to get sensor data.");
      }
    });
  },

  getEventData: async (): Promise<IEvent[]> => {
    return api.get(`${backendApi}/event`).then((response) => {
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
