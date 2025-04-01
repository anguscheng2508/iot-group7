"use client";

import React, { useState } from "react";
import { Spinner, Switch } from "@heroui/react";
import api from "../utils/api";

function ActuatorButton({ actuator }: { actuator: Actuator }) {
  const [status, setStatus] = useState(actuator.status);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleToggle = async () => {
    const newStatus = !status;
    setLoading(true);
    setError(null);

    try {
      await api.putActuatorStatus({ ...actuator, status: newStatus });
      setStatus(newStatus);
    } catch (err) {
      setError("Failed to update actuator status.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex gap-2 p-4 rounded-lg shadow-md w-56 justify-between items-center">
      <span className="text-black">{actuator.name} Status:</span>
      {loading ? <Spinner /> : <Switch isSelected={status} onChange={handleToggle} isDisabled={loading} />}
    </div>
  );
}

export default ActuatorButton;
