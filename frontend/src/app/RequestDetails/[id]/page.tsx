// app/requestDetails/[id]/page.tsx
import { redirect } from "next/navigation";
import { requestService } from "@/lib/requestService";
import RequestDetail from "@/components/business/RequestDetail";

interface Props {
  params: {
    id: string;
  };
} 


export default async function RequestDetailPage({ params }: Props) {
  const { id } = await params;
  if (!id) {
    redirect("/");
  }

  const request = requestService.getRequestById(id);

  if (!request) {
    redirect("/NotFound"); // automatically shows Next.js 404 page
  }

  return <RequestDetail request={request} />;
}

