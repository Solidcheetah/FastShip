import * as React from "react"

import { SearchForm } from "~/components/search-form"
import { VersionSwitcher } from "~/components/version-switcher"
import {
  Sidebar,
  SidebarContent,
  SidebarGroup,
  SidebarGroupContent,
  SidebarGroupLabel,
  SidebarHeader,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
  SidebarRail,
} from "~/components/ui/sidebar"
import { AuthContext } from "~/contexts/AuthContext"

// This is sample data.
const data = {
  versions: ["1.0.1", "1.1.0-alpha", "2.0.0-beta1"],
  navMain: [
    {
      title: "Getting Started",
      url: "#",
      items: [
        {
          title: "Installation",
          url: "#",
        },
        {
          title: "Project Structure",
          url: "#",
        },
      ],
    },
    {
      title: "Build Your Application",
      url: "#",
      items: [
        {
          title: "Routing",
          url: "#",
        },
        {
          title: "Data Fetching",
          url: "#",
          isActive: true,
        },
        {
          title: "Rendering",
          url: "#",
        },
        {
          title: "Caching",
          url: "#",
        },
        {
          title: "Styling",
          url: "#",
        },
        {
          title: "Optimizing",
          url: "#",
        },
        {
          title: "Configuring",
          url: "#",
        },
        {
          title: "Testing",
          url: "#",
        },
        {
          title: "Authentication",
          url: "#",
        },
        {
          title: "Deploying",
          url: "#",
        },
        {
          title: "Upgrading",
          url: "#",
        },
        {
          title: "Examples",
          url: "#",
        },
      ],
    },
    {
      title: "API Reference",
      url: "#",
      items: [
        {
          title: "Components",
          url: "#",
        },
        {
          title: "File Conventions",
          url: "#",
        },
        {
          title: "Functions",
          url: "#",
        },
        {
          title: "next.config.js Options",
          url: "#",
        },
        {
          title: "CLI",
          url: "#",
        },
        {
          title: "Edge Runtime",
          url: "#",
        },
      ],
    },
    {
      title: "Architecture",
      url: "#",
      items: [
        {
          title: "Accessibility",
          url: "#",
        },
        {
          title: "Fast Refresh",
          url: "#",
        },
        {
          title: "Next.js Compiler",
          url: "#",
        },
        {
          title: "Supported Browsers",
          url: "#",
        },
        {
          title: "Turbopack",
          url: "#",
        },
      ],
    },
  ],
}

export function AppSidebar({currentRoute, ...props }: {currentRoute: string} & React.ComponentProps<typeof Sidebar>) {
  const menuItems = [
    {
      title: "Dashboard",
      url: "/dashboard"
    },
    {
      title: "Account",
      url: "/account"
    }
  ]
  const {user} = React.useContext(AuthContext)

  return (
    <Sidebar {...props}>
      <SidebarHeader>
        <VersionSwitcher
          versions={data.versions}
          defaultVersion={data.versions[0]}
        />

      </SidebarHeader>
      <SidebarContent>
        {/* We create a SidebarGroup for each parent. */}

              <SidebarMenu className="gap-1">
        {menuItems.map((item) => (
                  <SidebarMenuItem key={item.title}>
                    <SidebarMenuButton asChild isActive={currentRoute === item.title}>
                      <a href={item.url}>{item.title}</a>
                    </SidebarMenuButton>
                  </SidebarMenuItem>
            ))}
              </SidebarMenu>
              {
                user === "seller" && (
                  <SidebarMenuItem>
                    <SidebarMenuButton isActive={currentRoute === "Submit Shipment"}>
                      <a href="/submit-shipment">
                        Submit Shipment
                      </a>
                    </SidebarMenuButton>
                  </SidebarMenuItem>
                )
              }
              {
                user === "partner" && (
                  <SidebarMenuItem>
                    <SidebarMenuButton isActive={currentRoute === "Update Shipment"}>
                      <a href="/update-shipment">
                        Update Shipment
                      </a>
                    </SidebarMenuButton>
                  </SidebarMenuItem>
                )
              }
              


      </SidebarContent>
      <SidebarRail />
    </Sidebar>
  )
}
