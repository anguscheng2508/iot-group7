"use client";

import React, { useState, useEffect } from "react";
import { Modal, ModalContent, ModalHeader, ModalBody, ModalFooter, Button, useDisclosure } from "@heroui/react";
import dynamic from "next/dynamic";
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
import useSensorData from "../hooks/useSensorData";

// Dynamically import the Line component with SSR disabled
const Line = dynamic(() => import("react-chartjs-2").then((mod) => mod.Line), {
  ssr: false,
});

function SensorButton({ sensor }: { sensor: Sensor }) {
  const { isOpen, onOpen, onOpenChange } = useDisclosure();
  const { data, loading, error } = useSensorData(sensor.type);

  const [startIndex, setStartIndex] = useState(0);
  const [isChartReady, setIsChartReady] = useState(false); // Track when chart is ready
  const displayCount = 20;

  // Register Chart.js components and zoom plugin only on the client side
  useEffect(() => {
    import("chartjs-plugin-zoom").then((zoom) => {
      ChartJS.register(
        CategoryScale,
        LinearScale,
        PointElement,
        LineElement,
        Title,
        Tooltip,
        Legend,
        Filler,
        zoom.default // Use .default for ES modules
      );
      setIsChartReady(true); // Mark chart as ready after registration
    });
  }, []);

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
                  <p>Loading...</p>
                </div>
              ) : error ? (
                <p>Error loading data: {error}</p>
              ) : !isChartReady ? (
                <div className="h-96 flex items-center justify-center">
                  <p>Loading chart...</p>
                </div>
              ) : (
                <div className="flex-col w-full h-96 gap-12">
                  {/* @ts-expect-error */}
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
