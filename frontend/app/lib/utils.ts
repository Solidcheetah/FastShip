import { clsx, type ClassValue } from "clsx"
import { twMerge } from "tailwind-merge"
import type { ShipmentRead } from "./client";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

function getLatestStatus(shipment: ShipmentRead) {
  return shipment.timeline[shipment.timeline.length - 1].status
}

function getShipmentsCountWithStatus(
  shipments: ShipmentRead[],
  status: string
) {
  console.log(shipments)
  return shipments.filter((shipment) => getLatestStatus(shipment) === status).length;
}

export { getLatestStatus, getShipmentsCountWithStatus as getShipmentsCountForStatus }