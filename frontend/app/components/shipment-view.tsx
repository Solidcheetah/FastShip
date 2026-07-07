import { useQueryClient } from "@tanstack/react-query";
import { Edit3, Package, PackageX } from "lucide-react";
import { useContext } from "react";
import { useNavigate } from "react-router";

import { Button } from "~/components/ui/button";
import { AuthContext } from "~/contexts/AuthContext";
import type { ShipmentRead } from "~/lib/client";


export default function ShipmentView({ shipment }: { shipment: ShipmentRead }) {
    const { user } = useContext(AuthContext)
    const queryClient = useQueryClient()
    const navigate = useNavigate()

    const details = [
        {
            "title": "Content",
            "description": shipment.content,
        },
        {
            "title": "Weight",
            "description": `${shipment.weight} kg`,
        },
        {
            "title": "Destination",
            "description": shipment.destination,
        },
        {
            "title": "Estimated Delivery",
            "description": shipment.estimated_delivery.split("T")[0],
        },
    ]

    return (
        <div className="flex flex-col gap-4 w-full max-w-[640px] relative">
            <div className="w-[80px] h-[80px] bg-gray-200 rounded-xl flex items-center justify-center">
                <Package size={40} />
            </div>
            {
                shipment.tags.length !== 0 &&
                <div className="flex gap-2">
                    {shipment.tags.map((tag, index) => (
                        <span
                            key={index}
                            className="inline-flex items-center rounded-md border border-transparent bg-secondary px-2 py-0.5 text-xs font-medium text-secondary-foreground"
                        >
                            {tag.name}
                        </span>
                    ))}
                </div>
            }
            <div className="grid grid-cols-2 gap-4">
                {details.map((item, index) => (
                    <div key={index} className="flex flex-col gap-1">
                        <h4 className="text-sm text-muted-foreground">{item.title}</h4>
                        <p className="text-l text-foreground font-medium">{item.description}</p>
                    </div>
                ))}
            </div>
            <h4 className="text-sm text-muted-foreground">Order History</h4>
            <div className="border rounded-l overflow-hidden">
                <table className="w-full text-sm">
                    <thead className="bg-gray-100">
                        <tr className="border-b text-left">
                            <th className="p-2 font-medium text-muted-foreground">Date</th>
                            <th className="p-2 font-medium text-muted-foreground">Location</th>
                            <th className="p-2 font-medium text-muted-foreground">Status</th>
                            <th className="p-2 font-medium text-muted-foreground">Description</th>
                        </tr>
                    </thead>
                    <tbody>
                        {shipment.timeline.map((item, index) => (
                            <tr key={index} className="border-b last:border-0">
                                <td className="p-2">
                                    {`${item.created_at.split("T")[0]} ${item.created_at.split("T")[1].slice(0, 5)}`}
                                </td>
                                <td className="p-2">{item.location}</td>
                                <td className="p-2">{item.status}</td>
                                <td className="p-2">{item.description}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
            <div className="flex gap-4 justify-end">
                {
                    user === "seller" &&
                    <Button variant="outline">
                        <PackageX />
                        Cancel Shipment
                    </Button>
                }
                {
                    user === "partner" &&

                    <Button onClick={() => {
                        navigate({
                            pathname: "/update-shipment",
                            search: `?id=${shipment.id}`,
                        })
                    }}>
                        <Edit3 />
                        Update Shipment Status
                    </Button>

                }
            </div>
        </div>
    );
}
