"use client";

import React, { useState } from "react";
import { Button } from "@nextui-org/react";
import DataDisplay from "./DataDisplay";
import api from "../utils/api";
import toast from "react-hot-toast";

function sortData(data: DataPoint[]) {
  return data.sort((a: DataPoint, b: DataPoint) => {
    return new Date(a.date).getTime() - new Date(b.date).getTime();
  });
}

function HistoricalDataDisplay({ historicalData }: { historicalData: HistoricalData }) {
  const [dublinData, setDublinData] = useState<DataPoint[]>(sortData(historicalData.dublin));
  const [madisonData, setMadisonData] = useState<DataPoint[]>(sortData(historicalData.madison));

  const updateData = async () => {
    const data: HistoricalData = await api.getUpdatedHistoricalData();
    if (data) {
      setDublinData(sortData(data.dublin));
      setMadisonData(sortData(data.madison));
    }
  };

  return (
    <div className="flex flex-col gap-5 items-center justify-center w-full">
      <h1 className="text-xl">Historical PM 2.5 Data in Dublin and Madison</h1>
      <Button
        onClick={() => {
          toast.promise(updateData(), {
            loading: "Data Updating...",
            success: "Data Update Success",
            error: "Data Update Failed",
          });
        }}
        color="primary"
      >
        Update Data
      </Button>
      <div className="flex flex-col md:flex-row gap-5 h-full w-full items-center justify-center">
        <DataDisplay name="Dublin" historicalData={dublinData} />
        <DataDisplay name="Madison, WI" historicalData={madisonData} />
      </div>
    </div>
  );
}

export default HistoricalDataDisplay;
