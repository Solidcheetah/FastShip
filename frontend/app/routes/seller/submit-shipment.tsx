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
import { Label } from "~/components/ui/label"
import { Input } from "~/components/ui/input"
import { Button } from "~/components/ui/button"
import { SubmitShipmentForm } from "~/components/submit-shipment-form"

export default function SubmitShipmentPage() {
  const { token, isLoading: isAuthLoading, user, logout } = useContext(AuthContext)
  if (!isAuthLoading && !token && user !== "seller") {
    return <Navigate to="/" />
  }
 
  return (
    <SidebarProvider>
      <AppSidebar currentRoute="Submit Shipment"/>
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
                <BreadcrumbPage>Submit Shipment</BreadcrumbPage>
              </BreadcrumbItem>
            </BreadcrumbList>
          </Breadcrumb>
        </header> 
        <div>
          <SubmitShipmentForm />
        </div>
      </SidebarInset>
    </SidebarProvider>
  )
}


