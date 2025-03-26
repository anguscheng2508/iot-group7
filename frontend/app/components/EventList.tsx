import api from "../utils/api";

async function EventList() {
  const events = await api.getEventData();
  console.log(events);

  return (
    <section className="max-h-screen overflow-y-auto">
      <h3 className="font-bold pb-4">Event List</h3>
      {events.map((event: IEvent) => {
        return (
          <div
            key={Math.random()}
            className="flex flex-col gap-y-1 border-b border-gray-300 pb-4 mb-4"
          >
            <h4>
              <span className="text-gray-500">Device</span>: {event.deviceName}
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
      })}
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
