import { cn } from "~/lib/utils"
import { Button } from "~/components/ui/button"
import {
  Field,
  FieldDescription,
  FieldGroup,
  FieldLabel,
  FieldSeparator,
} from "~/components/ui/field"
import { Input } from "~/components/ui/input"
import { useContext } from "react"
import { AuthContext, type UserType } from "~/contexts/AuthContext"
import api from "~/lib/api"
import { toast } from "sonner"

export function ForgotPasswordForm({
  className,
  user, 
  ...props
}:{user: UserType} & React.ComponentProps<"form">) {

  const {login} = useContext(AuthContext)

  async function sendResetLink(data: FormData){
    const email = data.get("email")?.toString()


    if(!email){
      return 
    }
    const userApi = user === "seller" ? api.seller : api.partner
    await userApi.forgotPassword({email})
    toast("Reset link sent")
  }
  return (
    <form className={cn("flex flex-col gap-6", className)} {...props} action={sendResetLink}>
      <FieldGroup>
        <div className="flex flex-col items-center gap-1 text-center">
          <h1 className="text-2xl font-bold">Reset Password</h1>
          <p className="text-sm text-balance text-muted-foreground">
            Enter your email address
          </p>
        </div>
        <Field>
          <FieldLabel htmlFor="email">Email</FieldLabel>
          <Input
            id="email"
            type="email"
            name="email"
            placeholder="m@example.com"
            required
            className="bg-background"
          />
        </Field>
       
        <Field>
          <Button type="submit">Send Reset Link</Button>
        </Field>
      </FieldGroup>
    </form>
  )
}
