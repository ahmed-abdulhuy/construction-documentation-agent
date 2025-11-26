import { redirect } from "next/navigation";
import { requestService } from "@/lib/requestService";
import { RequestForm } from "@/components/business/RequestForm";


interface Props {
  params: { id: string };
}

export default function RequestFormPage({ params }: Props) {
  const { id } = params;

  // 1. Create Mode
  if (id === "new") {
    return <RequestForm mode="create" />;
  }

  // 2. Invalid or missing ID
  if (!id) {
    redirect("/");
  }

  // 3. Fetch the request
  const request = requestService.getRequestById(id);

  // 4. Not Found
  if (!request) {
    redirect("/NotFound");
  }

  // 5. Edit mode
  return <RequestForm mode="edit" initialData={request} />;
}
