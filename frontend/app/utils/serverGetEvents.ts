"use server";

import api from "../utils/api";

export default async function getEvents(): Promise<IEvent[]> {
  await new Promise((resolve) => setTimeout(resolve, 3000));
  return await api.getEventData();
}
