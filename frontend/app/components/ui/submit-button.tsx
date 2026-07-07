import { useFormStatus } from "react-dom"

import { Button } from "~/components/ui/button"

export function SubmitButton({
  text,
  ...props
}: { text: string } & React.ComponentProps<typeof Button>) {
  const { pending } = useFormStatus()

  return (
    <Button type="submit" disabled={pending} {...props}>
      {pending ? "Submitting..." : text}
    </Button>
  )
}
