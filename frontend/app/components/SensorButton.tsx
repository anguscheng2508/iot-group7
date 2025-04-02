"use client";

import React, { useState } from "react";
import { Modal, ModalContent, ModalHeader, ModalBody, ModalFooter, Button, useDisclosure } from "@heroui/react";
import { Line } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler,
} from "chart.js";
import zoomPlugin from "chartjs-plugin-zoom";
import useSensorData from "../hooks/useSensorData";

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend, Filler, zoomPlugin);

function SensorButton({ sensor }: { sensor: Sensor }) {
  const { isOpen, onOpen, onOpenChange } = useDisclosure();
  const { data, loading, error } = useSensorData(sensor.type);

  const [startIndex, setStartIndex] = useState(0);
  const displayCount = 20;

  const handleNext = () => {
    if (data && startIndex + displayCount < data.length) {
      setStartIndex(startIndex + displayCount);
    }
  };

  const handlePrev = () => {
    if (startIndex - displayCount >= 0) {
      setStartIndex(startIndex - displayCount);
    }
  };

  // Process data to get the current slice of 20 data points
  const recentData = data ? data.slice(startIndex, startIndex + displayCount) : [];

  const chartData = {
    labels: recentData.map((d) => new Date(d.timestamp!).toLocaleString()),
    datasets: [
      {
        label: `${sensor.name} Levels`,
        data: recentData.map((d) => d.value),
        fill: true,
        backgroundColor: "rgba(75, 192, 192, 0.2)",
        borderColor: "rgb(75, 192, 192)",
        tension: 0.4,
        pointRadius: 0,
      },
    ],
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: "top" as const,
      },
      title: {
        display: true,
        text: `${sensor.name} Levels`,
      },
      zoom: {
        pan: {
          enabled: true,
          mode: "x",
        },
        zoom: {
          wheel: {
            enabled: true,
          },
          pinch: {
            enabled: true,
          },
          mode: "x",
        },
      },
    },
    scales: {
      x: {
        display: true,
        title: {
          display: true,
          text: "Timestamp",
        },
      },
      y: {
        display: true,
        title: {
          display: true,
          text: "Value",
        },
      },
    },
  };

  return (
    <>
      <Button onPress={onOpen} color="primary">
        {sensor.name}
      </Button>
      <Modal isOpen={isOpen} onOpenChange={onOpenChange} size="2xl" backdrop="blur">
        <ModalContent>
          <>
            <ModalHeader className="flex flex-col gap-1">{sensor.name} Data</ModalHeader>
            <ModalBody className="flex-col">
              {loading ? (
                <div className="h-96 flex items-center justify-center">
                  <p>Loading...</p> {/* Replace with a skeleton loader if desired */}
                </div>
              ) : error ? (
                <p>Error loading data: {error}</p>
              ) : (
                <div className="flex-col w-full h-96 gap-12">
                  {/* @ts-ignore */}
                  <Line data={chartData} options={options} />
                </div>
              )}
            </ModalBody>
            <ModalFooter>
              <div className="flex w-full justify-between m-4">
                <Button onPress={handlePrev} disabled={startIndex === 0}>
                  Previous
                </Button>
                <Button onPress={handleNext} disabled={startIndex + displayCount >= (data ? data.length : 0)}>
                  Next
                </Button>
              </div>
            </ModalFooter>
          </>
        </ModalContent>
      </Modal>
    </>
  );
}

export default SensorButton;
