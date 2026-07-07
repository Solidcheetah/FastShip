import { useQuery } from "@tanstack/react-query"
import { useContext } from "react"
import { Navigate } from "react-router"
import { AppSidebar } from "~/components/app-sidebar"
import {
  Breadcrumb,
  BreadcrumbItem,
  BreadcrumbLink,
  BreadcrumbList,
  BreadcrumbPage,
  BreadcrumbSeparator,
} from "~/components/ui/breadcrumb"
import { Separator } from "~/components/ui/separator"
import { Skeleton } from "~/components/ui/skeleton"
import {
  SidebarInset,
  SidebarProvider,
  SidebarTrigger,
} from "~/components/ui/sidebar"
import { AuthContext } from "~/contexts/AuthContext"
import api from "~/lib/api"
import { getShipmentsCountForStatus } from "~/lib/utils"
import { ShipmentStatus } from "~/lib/client"
import ShipmentCard from "~/components/shipment-card"

export default function DashboardPage() {
  const { token, isLoading: isAuthLoading, user } = useContext(AuthContext)
  if (!isAuthLoading && !token) {
    return <Navigate to="/" />
  }

  const { isLoading: isShipmentsLoading, isError, data } = useQuery({
    queryKey: ["shipments"],
    queryFn: async () => {
      const { data } = user === "seller" ? await api.seller.getShipments() : await api.partner.getPartnerShipments()
      return data
    }
  })

  if (isError) {
    return (
      <div className="flex min-h-screen flex-col items-center justify-center gap-2 text-center">
        <h1 className="text-lg font-semibold text-destructive">Failed to load shipments</h1>
        <p className="text-sm text-muted-foreground">Something went wrong while fetching your shipments. Please try again later.</p>
      </div>
    )
  }

  return (
    <SidebarProvider>
      <AppSidebar currentRoute="Dashboard"/>
      <SidebarInset>
        <header className="flex h-16 shrink-0 items-center gap-2 border-b px-4">
          <SidebarTrigger className="-ml-1" />
          <Separator
            orientation="vertical"
            className="mr-2 data-vertical:h-4 data-vertical:self-auto"
          />
          <Breadcrumb>
            <BreadcrumbList>
              <BreadcrumbItem>
                <BreadcrumbPage>Dashboard</BreadcrumbPage>
              </BreadcrumbItem>
            </BreadcrumbList>
          </Breadcrumb>
        </header> 
        {isShipmentsLoading || !data ? (
          <div className="flex flex-1 flex-col gap-4 p-4">
            <div className="grid auto-rows-min gap-4 md:grid-cols-3">
              <Skeleton className="aspect-video rounded-xl" />
              <Skeleton className="aspect-video rounded-xl" />
              <Skeleton className="aspect-video rounded-xl" />
            </div>
            <Skeleton className="min-h-screen flex-1 md:min-h-min" />
          </div>
        ) : (
          <div className="flex flex-1 flex-col gap-6 p-4">
            <div className="grid auto-rows-min gap-4 md:grid-cols-4">
              <NumberLabel value={data.length} label="Total Shipments" />
              <NumberLabel value={getShipmentsCountForStatus(data, ShipmentStatus.Placed)} label="Placed" />
              <NumberLabel value={getShipmentsCountForStatus(data, ShipmentStatus.InTransit)} label="In Transit" />
              <NumberLabel value={getShipmentsCountForStatus(data, ShipmentStatus.Delivered)} label="Delivered" />
            </div>
            <div className="grid auto-rows-min items-start gap-4 md:grid-cols-4">
              {data.map((shipment) => (
                <ShipmentCard key={shipment.id} shipment={shipment} />
              ))}
            </div>
          </div>
        )}
      </SidebarInset>
    </SidebarProvider>
  )
}


function NumberLabel({ value, label }: { value: number; label: string }) {
  return (
    <div className="flex flex-col gap-2 rounded-xl border border-gray-200 p-4">
      <h1 className="text-4xl font-bold">{value}</h1>
      <p className="text-gray-500">{label}</p>
    </div>
  )
}
