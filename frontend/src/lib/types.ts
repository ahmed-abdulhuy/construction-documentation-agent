// Core domain types - independent of UI library

export type RequestStatus = 'draft' | 'pending' | 'approved' | 'rejected';

export type RequestPriority = 'low' | 'medium' | 'high' | 'urgent';

export type UserRole = 'engineer' | 'approver' | 'admin';

export interface User {
  id: string;
  name: string;
  email: string;
  role: UserRole;
  department?: string;
}

export interface RequestDocument {
  id: string;
  title: string;
  description: string;
  category: string;
  priority: RequestPriority;
  status: RequestStatus;
  createdBy: string;
  createdByName: string;
  createdAt: string;
  updatedAt: string;
  submittedAt?: string;
  reviewedAt?: string;
  reviewedBy?: string;
  reviewerName?: string;
  reviewNotes?: string;
  attachments?: string[];
  projectCode?: string;
  estimatedCost?: number;
}

export interface RequestFilters {
  status?: RequestStatus[];
  priority?: RequestPriority[];
  category?: string;
  searchTerm?: string;
}
