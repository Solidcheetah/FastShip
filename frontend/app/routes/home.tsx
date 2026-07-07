import type { Route } from "./+types/home";
import { Welcome } from "../welcome/welcome";
import { Button } from "~/components/ui/button";
import { Link } from "react-router";

export function meta({}: Route.MetaArgs) {
  return [
    { title: "New React Router App" },
    { name: "description", content: "Welcome to React Router!" },
  ];
}

export default function Home() {
  return (
    <div className="flex min-h-screen flex-col items-center justify-center gap-4">
      <h1 className="text-3xl font-bold">Welcome</h1>
      <Button className="w-48" asChild>
        <Link to="/seller/login">Seller Login</Link>
      </Button>
      <Button className="w-48" asChild>
        <Link to="/partner/login">Partner Login</Link>
      </Button>
    </div>
  )
  
}
