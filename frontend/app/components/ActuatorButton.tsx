"use client";

import React, { useState } from "react";
import { Spinner, Tabs, Tab } from "@heroui/react";
import api from "../utils/api";

function ActuatorButton({ actuator }: { actuator: Actuator }) {
  const [loading, setLoading] = useState(false);
  const [currentStatus, setCurrentStatus] = useState(actuator.status);

  const handleToggle = async (status: ActuatorStatus) => {
    if (status === currentStatus) return;

    setLoading(true);

    try {
      await api.putActuatorStatus(actuator, status);
      setCurrentStatus(status);
    } catch (err) {
      console.error("Failed to update actuator status.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex gap-2 p-4 rounded-lg shadow-md w-full justify-between items-center">
      <span className="text-black">{actuator.name} Status:</span>

      {/* {loading && <Spinner />} */}

      <Tabs
        aria-label="Options"
        selectedKey={currentStatus}
        onSelectionChange={(key) => handleToggle(key as ActuatorStatus)}
      >
        <Tab key="ON" title="On" />
        <Tab key="OFF" title="Off" />
        <Tab key="AUTO" title="Auto" />
      </Tabs>
    </div>
  );
}

export default ActuatorButton;
