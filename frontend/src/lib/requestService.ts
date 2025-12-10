// Business logic service - no UI dependencies
import { NewRequestData, RequestDocument, RequestFilters, RequestStatus } from './types';


class RequestService {
  
  // private requests: RequestDocument[] = [...mockRequests];
  private async api(path: string, options: RequestInit = {}) {
    const API_Base = "http://localhost:8000";
    const response = await fetch(`${API_Base}${path}`, {
      ...options,
      credentials: 'include',
      headers: {
        'Content-Type': 'application/json',
        ...(options.headers || {}),
      },
    });
    if (!response.ok) {
      throw new Error(`API request failed with status ${response.status}`);
    }

    try {
      return await response.json();
    } catch {
      throw new Error("Returned Invalid Json")
    }
  }

  async getMyRequests(): Promise<RequestDocument[]> {
    const requests = await this.api("/wir/"); // Fetch from API
    return requests;
  }

  async getRequestById(id: string): Promise<RequestDocument | undefined> {
    const request = await this.api(`/wir/${id}/`); // Fetch from API
    return request;
  }

  async filterRequests(filters: RequestFilters): Promise<RequestDocument[]> {
    const requests = await this.getMyRequests();
    console.info("Fetched requests:", requests);
    return requests.filter(req => {
      if (filters.status?.length && !filters.status.includes(req.status)) {
        return false;
      }
      if (filters.priority?.length && !filters.priority.includes(req.priority)) {
        return false;
      }
      if (filters.category && req.category !== filters.category) {
        return false;
      }
      if (filters.searchTerm) {
        const term = filters.searchTerm.toLowerCase();
        return (
          req.title.toLowerCase().includes(term) ||
          req.description.toLowerCase().includes(term) ||
          req.projectCode?.toLowerCase().includes(term)
        );
      }
      return true;
    }).sort((a, b) => 
      new Date(b.updatedAt).getTime() - new Date(a.updatedAt).getTime()
    );
  }

  async createRequest(data: NewRequestData): Promise<RequestDocument> {
    const options: RequestInit = {
      method: 'POST',
      body: JSON.stringify(data),
    };
    const result = await this.api('/wir/create/', options);
    const newRequest: RequestDocument = result;    
    return newRequest;
  }

  // ! Disabled until configuring UI to update requests
  // updateRequest(id: string, updates: Partial<RequestDocument>): RequestDocument | null {
  //   const index = this.requests.findIndex(req => req.id === id);
  //   if (index === -1) return null;

  //   this.requests[index] = {
  //     ...this.requests[index],
  //     ...updates,
  //     updatedAt: new Date().toISOString(),
  //   };
  //   return this.requests[index];
  // }

  //! Disabled until configuring UI to update requests
  // updateRequestStatus(
  //   id: string, 
  //   status: RequestStatus,
  //   reviewerInfo?: { reviewedBy: string; reviewerName: string; reviewNotes?: string }
  // ): RequestDocument | null {
  //   const updates: Partial<RequestDocument> = {
  //     status,
  //     updatedAt: new Date().toISOString(),
  //   };

  //   if (status !== 'draft' && status !== 'pending') {
  //     updates.reviewedAt = new Date().toISOString();
  //     if (reviewerInfo) {
  //       updates.reviewedBy = reviewerInfo.reviewedBy;
  //       updates.reviewerName = reviewerInfo.reviewerName;
  //       updates.reviewNotes = reviewerInfo.reviewNotes;
  //     }
  //   }

  //   if (status === 'pending') {
  //     updates.submittedAt = new Date().toISOString();
  //   }

  //   return this.updateRequest(id, updates);
  // }

  //! Disabled until configuring UI to delete requests
  // deleteRequest(id: string): boolean {
  //   const index = this.requests.findIndex(req => req.id === id);
  //   if (index === -1) return false;
  //   this.requests.splice(index, 1);
  //   return true;
  // }

  // ! Disabled until configuring UI to get requests by status
  // getRequestsByStatus(status: RequestStatus): RequestDocument[] {
  //   return this.requests.filter(req => req.status === status);
  // }

  // getRequestsByCreator(creatorId: string): RequestDocument[] {
  //   return this.requests.filter(req => req.createdBy === creatorId);
  // }
}

// Singleton instance
export const requestService = new RequestService();
