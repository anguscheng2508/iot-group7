import axios from "axios";

const backendApi = "https://8601-89-101-47-26.ngrok-free.app";

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
};

const dataApi = {
  getSensorData: async (sensorId: string) => {
    return axios.get(`${backendApi}/sensor/${sensorId}`).then((response) => {
      if (response.status === 200) {
        return response.data;
      } else {
        throw Error("Failed to get sensor data.");
      }
    });
  },

  getEventData: async () => {
    return axios.get(`${backendApi}/event`).then((response) => {
      if (response.status === 200) {
        return response.data;
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
