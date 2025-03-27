"use client";

import React, { useState } from "react";
import { Button } from "@heroui/react";
import serverGetEvents from "../utils/serverGetEvents";

function EventList({ initEvents }: { initEvents: IEvent[] }) {
  const [events, setEvents] = useState<IEvent[]>(initEvents);
  const [isLoading, setIsLoading] = useState(false);
  const handlePress = async () => {
    setIsLoading(true);
    const events = await serverGetEvents();
    setIsLoading(false);
    setEvents(events);
  };
  return (
    <section className="max-h-screen overflow-y-auto">
      <div className="flex justify-between items-center pb-4">
        <h3 className="font-bold">Event List</h3>
        <button
          onClick={handlePress}
          className="border-gray-300 border-1 px-2 py-1 hover:bg-gray-200"
        >
          Refresh
        </button>
      </div>
      {isLoading ? (
        <div className="m-auto">Loading...</div>
      ) : (
        events.map((event: IEvent) => {
          return (
            <div
              key={Math.random()}
              className="flex flex-col gap-y-1 border-b border-gray-300 pb-4 mb-4"
            >
              <h4>
                <span className="text-gray-500">Device</span>:{" "}
                {event.deviceName}
              </h4>
              <span>
                <span className="text-gray-500">Description</span>:{" "}
                {event.description}
              </span>
              <span>
                <span className="text-gray-500">Time</span>:{" "}
                {formatDate(event?.timestamp?.toString() || null)}
              </span>
            </div>
          );
        })
      )}
    </section>
  );
}

/**
 * @param datetimeStr yyyy-mm-ddThh:mm:ss format
 * @returns mm/dd/yyyy format
 */
const formatDate = (datetimeStr: string | null): string | null => {
  if (!datetimeStr) {
    return null;
  }

  const date = new Date(datetimeStr);

  if (!isNaN(date.getTime())) {
    const hours = String(date.getHours()).padStart(2, "0");
    const minutes = String(date.getMinutes()).padStart(2, "0");

    const monthNames = [
      "January",
      "February",
      "March",
      "April",
      "May",
      "June",
      "July",
      "August",
      "September",
      "October",
      "November",
      "December",
    ];
    const month = monthNames[date.getMonth()];

    const day = date.getDate();
    const year = date.getFullYear();

    return `${hours}:${minutes} | ${month} ${day}, ${year}`;
  } else {
    return null;
  }
};

export default EventList;
