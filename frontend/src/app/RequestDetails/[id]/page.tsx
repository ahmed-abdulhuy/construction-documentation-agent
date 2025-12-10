"use client";

// app/requestDetails/[id]/page.tsx
import { requestService } from "@/lib/requestService";
import RequestDetail from "@/components/business/RequestDetail";
import NewRequest from "@/app/RequestDetails/[id]/newRequest";
import { useEffect, useState } from "react";
import { RequestDocument } from "@/lib/types";
import { useParams, useRouter } from "next/navigation";


export default function RequestDetailPage() {
  const params = useParams();
  const router = useRouter();
  const { id } = params as { id: string };
  const [request, setRequest] = useState<RequestDocument | undefined>();
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    console.log("Request ID from params:", id);
    if (!id) {
      router.replace("/NotFound");
      return;
    }
    if (id === "new") {
      return; // Handled separately
    }

    async function LoadRequest() {
      try {
        const fetchedRequest = await requestService.getRequestById(id);
        console.log("Fetched Request:", fetchedRequest);
        if (!fetchedRequest) {
          router.replace("/NotFound");
          return;
        }
        setRequest(fetchedRequest);

      } catch {
        router.replace("/NotFound");
      } finally {
        setLoading(false);
      }
    }
    LoadRequest();
  }, [id, router]);

  console.log("Request ID:", id);
  if (!id) {
    router.push("/NotFound");
  }
  
  if(id === "new") {
    return <NewRequest />
  }
  if(loading) {
    return <div>Loading...</div>;
  }
  
  console.log("Request Data:", request);
  // if (!request) {
  //   router.push("/NotFound"); // automatically shows Next.js 404 page
  // }

  return <RequestDetail request={request} />;
}

