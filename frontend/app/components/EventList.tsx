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
    <div className="flex-col border border-gray-300 p-4 w-1/2 h-full gap-3">
      <div className="flex justify-between items-center font-bold text-lg w-full h-auto">
        <span>Event List</span>
        <Button onPress={handlePress}>Refresh</Button>
      </div>
      {isLoading ? (
        <div className="m-auto">Loading...</div>
      ) : (
        <div className="flex-col overflow-y-auto h-[95%] w-full">
          {events.map((event: IEvent, index: number) => {
            return (
              <div key={index} className="flex flex-col gap-y-1 border-b border-gray-300 pb-4 mb-4">
                <div>
                  <span className="text-gray-500">Device</span>: {event.deviceName}
                </div>
                <span>
                  <span className="text-gray-500">Description</span>: {event.description}
                </span>
                <span>
                  <span className="text-gray-500">Time</span>: {formatDate(event?.timestamp?.toString() || null)}
                </span>
              </div>
            );
          })}
        </div>
      )}
    </div>
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
