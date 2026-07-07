import { useQuery } from "@tanstack/react-query"
import { useContext, useState } from "react"
import { Navigate, useSearchParams } from "react-router"
import { AppSidebar } from "~/components/app-sidebar"
import { Separator } from "~/components/ui/separator"
import {
  SidebarInset,
  SidebarProvider,
  SidebarTrigger,
} from "~/components/ui/sidebar"
import { UpdateShipmentForm } from "~/components/update-shipment-form"
import { AuthContext } from "~/contexts/AuthContext"
import api from "~/lib/api"

export default function UpdateShipmentPage() {

  // Get Authentication State
  const { token, isLoading: isAuthLoading, user } = useContext(AuthContext)
  // Wait for auth to hydrate before deciding where to send the user
  if (!isAuthLoading && !token) {
    return <Navigate to="/" />
  }
  if (!isAuthLoading && token && user !== "partner") {
    return <Navigate to="/dashboard" />
  }

  const [params] = useSearchParams()

  const [id, setId] = useState<string | null>(params.get("id"))

  const { data } = useQuery({
    queryKey: [id],
    queryFn: async () => {
      if (!id) return null
      const response = await api.shipment.getShipment({ id })
      return response.data
    },
    enabled: !!id,
  })

  return (
    <SidebarProvider
      style={
        {
          "--sidebar-width": "19rem",
        } as React.CSSProperties
      }
    >
      <AppSidebar currentRoute="Update Shipment" />
      <SidebarInset>
        <header className="flex h-16 shrink-0 items-center gap-2 px-4">
          <SidebarTrigger className="-ml-1" />
          <Separator
            orientation="vertical"
            className="mr-2 data-[orientation=vertical]:h-4"
          />
          <h2>Update Shipment</h2>
        </header>
        <div className="flex flex-1 flex-col gap-4 p-4 pt-0 max-w-[600px]">
          <UpdateShipmentForm shipment={data} shipmentId={id} onScan={(id) => {setId(id)}}/>
        </div>
      </SidebarInset>
    </SidebarProvider>
  )
}
