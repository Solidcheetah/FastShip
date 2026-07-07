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

export default function AccountPage() {
  const { token, isLoading: isAuthLoading, user, logout } = useContext(AuthContext)
  if (!isAuthLoading && !token) {
    return <Navigate to="/" />
  }

  const { isLoading: isShipmentsLoading, isError, data } = useQuery({
    queryKey: ["account"],
    queryFn: async () => {
      const getUserProfile = user === "seller" ? api.seller.getSellerProfile : api.partner.getDeliveryPartnerProfile
      const {data} = await getUserProfile()
      return data
    }
  })

  if (isError) {
    return (
      <div className="flex min-h-screen flex-col items-center justify-center gap-2 text-center">
        <h1 className="text-lg font-semibold text-destructive">Failed to load S</h1>
        <p className="text-sm text-muted-foreground">Something went wrong while fetching your account profile. Please try again later.</p>
      </div>
    )
  }

  return (
    <SidebarProvider>
      <AppSidebar currentRoute="Account"/>
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
                <BreadcrumbPage>Account</BreadcrumbPage>
              </BreadcrumbItem>
            </BreadcrumbList>
          </Breadcrumb>
        </header> 
        {isShipmentsLoading ? (
          <div className="flex flex-1 flex-col gap-4 p-4">
            <div className="grid auto-rows-min gap-4 md:grid-cols-3">
              <Skeleton className="aspect-video rounded-xl" />
              <Skeleton className="aspect-video rounded-xl" />
              <Skeleton className="aspect-video rounded-xl" />
            </div>
            <Skeleton className="min-h-screen flex-1 md:min-h-min" />
          </div>
        ) : (
          <>
            <div className="flex flex-col gap-4 max-w-[400px] p-2.5">
                <Label htmlFor="name">Name</Label>
                <Input name="name" value={data?.name ?? "..."} readOnly/> 
                <Label htmlFor="email">Email</Label>
                <Input name="email" value={data?.email ?? "..."} readOnly/> 
                <Button onClick={logout} className="ml-auto">Log out</Button>
            </div>
          </>
        )}
      </SidebarInset>
    </SidebarProvider>
  )
}


