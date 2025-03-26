"use client";

import React from "react";
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

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend, Filler, zoomPlugin);

function DataDisplay({ name, historicalData }: { name: string; historicalData: DataPoint[] }) {
  // Sample data to reduce the number of points
  const sampleRate = 10; // Adjust this value to control the number of points
  const sampledData = historicalData.filter((_, index) => index % sampleRate === 0);

  const labels = sampledData.map((dataPoint) => {
    const date = new Date(dataPoint.date);
    const month = String(date.getMonth() + 1).padStart(2, "0");
    const day = String(date.getDate()).padStart(2, "0");
    const year = date.getFullYear();
    return `${month}/${day}/${year}`;
  });

  const pm25Values = sampledData.map((dataPoint) => dataPoint.pm25);

  const data = {
    labels,
    datasets: [
      {
        label: `PM 2.5 Levels in ${name}`,
        data: pm25Values,
        fill: true,
        backgroundColor: "rgba(75, 192, 192, 0.2)",
        borderColor: "rgb(75, 192, 192)",
        tension: 0.4,
        pointRadius: 0, // Hide points for a cleaner look
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
        text: `${name} PM 2.5 Levels`,
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
          text: "Date",
        },
      },
      y: {
        display: true,
        title: {
          display: true,
          text: "PM 2.5",
        },
      },
    },
  };

  return (
    <div className="w-full h-96">
      {/* @ts-ignore */}
      <Line data={data} options={options} />
    </div>
  );
}

export default DataDisplay;
