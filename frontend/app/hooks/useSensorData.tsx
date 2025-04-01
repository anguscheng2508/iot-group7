"use client";
import { useState, useEffect } from "react";
import api from "../utils/api";

function useSensorData(sensorId: string) {
  const [data, setData] = useState<SensorData[] | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchSensorData = async () => {
      try {
        setLoading(true);
        const sensorData = await api.getSensorData(sensorId);
        setData(sensorData);
      } catch (err) {
        setError("Failed to fetch sensor data.");
      } finally {
        setLoading(false);
      }
    };

    fetchSensorData();
  }, [sensorId]);

  return { data, loading, error };
}

export default useSensorData;
