"use client";
import { Button } from "@nextui-org/react";
import React, { useState } from "react";
import api from "../utils/api";
import toast from "react-hot-toast";
import DataDisplay from "./DataDisplay";

function PredictPanel({ modelNames }: { modelNames: string[] }) {
  const [showPredict, setShowPredict] = useState(false);
  const [dublinData, setDublinData] = useState<DataPoint[]>();
  const [madisonData, setMadisonData] = useState<DataPoint[]>();

  function sortData(data: DataPoint[]) {
    return data.sort((a: DataPoint, b: DataPoint) => {
      return new Date(a.date).getTime() - new Date(b.date).getTime();
    });
  }

  async function getPredictionData(method: string) {
    const data: HistoricalData = await api.postPrediction(method);
    if (data) {
      setDublinData(sortData(data.dublin));
      setMadisonData(sortData(data.madison));
    }
    setShowPredict(true);
  }

  return (
    <div className="flex flex-col gap-3 w-full">
      <h2 className="text-center text-lg mt-3">Predict the future PM 2.5 of both cities.</h2>
      <h3>Please select a model: </h3>
      <div className="flex gap-3">
        {modelNames.map((name) => (
          <Button
            key={name}
            color="default"
            onClick={() => {
              toast.promise(getPredictionData(name), {
                loading: "Predicting...",
                success: "Predict Success",
                error: "Predict Failed",
              });
            }}
          >
            {name}
          </Button>
        ))}
      </div>
      {showPredict && (
        <div className="flex flex-col md:flex-row h-full w-full items-center justify-center">
          <DataDisplay name="Dublin" historicalData={dublinData!} />
          <DataDisplay name="Madison, WI" historicalData={madisonData!} />{" "}
        </div>
      )}
    </div>
  );
}

export default PredictPanel;
