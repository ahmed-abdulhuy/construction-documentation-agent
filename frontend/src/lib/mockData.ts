// Mock data for demonstration - replace with actual backend later
import { RequestDocument, User } from './types';

export const mockUsers: User[] = [
  {
    id: 'u1',
    name: 'John Chen',
    email: 'john.chen@construct.com',
    role: 'engineer',
    department: 'Civil Engineering'
  },
  {
    id: 'u2',
    name: 'Sarah Martinez',
    email: 'sarah.martinez@construct.com',
    role: 'approver',
    department: 'Project Management'
  },
  {
    id: 'u3',
    name: 'Michael Johnson',
    email: 'michael.j@construct.com',
    role: 'engineer',
    department: 'Structural Engineering'
  }
];

export const mockRequests: RequestDocument[] = [
  {
    id: 'req-001',
    title: 'Additional Concrete for Foundation - Building A',
    description: 'Request for 50 cubic yards of additional concrete for foundation reinforcement due to soil conditions discovered during excavation.',
    category: 'Materials',
    priority: 'high',
    status: 'pending',
    createdBy: 'u1',
    createdByName: 'John Chen',
    createdAt: '2025-01-15T10:30:00Z',
    updatedAt: '2025-01-15T10:30:00Z',
    submittedAt: '2025-01-15T10:30:00Z',
    projectCode: 'PRJ-2025-001',
    estimatedCost: 15000
  },
  {
    id: 'req-002',
    title: 'Design Change Approval - HVAC System',
    description: 'Request approval for updated HVAC design to accommodate client requirements for improved air quality standards.',
    category: 'Design Change',
    priority: 'medium',
    status: 'approved',
    createdBy: 'u3',
    createdByName: 'Michael Johnson',
    createdAt: '2025-01-10T14:20:00Z',
    updatedAt: '2025-01-12T09:15:00Z',
    submittedAt: '2025-01-10T14:20:00Z',
    reviewedAt: '2025-01-12T09:15:00Z',
    reviewedBy: 'u2',
    reviewerName: 'Sarah Martinez',
    reviewNotes: 'Approved. Updated design meets standards and budget requirements.',
    projectCode: 'PRJ-2025-002',
    estimatedCost: 45000
  },
  {
    id: 'req-003',
    title: 'Site Safety Equipment Purchase',
    description: 'Request for procurement of additional safety harnesses, hard hats, and high-visibility vests for new crew members.',
    category: 'Equipment',
    priority: 'urgent',
    status: 'approved',
    createdBy: 'u1',
    createdByName: 'John Chen',
    createdAt: '2025-01-14T08:00:00Z',
    updatedAt: '2025-01-14T11:30:00Z',
    submittedAt: '2025-01-14T08:00:00Z',
    reviewedAt: '2025-01-14T11:30:00Z',
    reviewedBy: 'u2',
    reviewerName: 'Sarah Martinez',
    reviewNotes: 'Approved immediately due to safety priority.',
    projectCode: 'PRJ-2025-001',
    estimatedCost: 3500
  },
  {
    id: 'req-004',
    title: 'Permit Extension Request - Phase 2',
    description: 'Request for extension of building permit due to weather delays affecting construction timeline.',
    category: 'Documentation',
    priority: 'high',
    status: 'pending',
    createdBy: 'u3',
    createdByName: 'Michael Johnson',
    createdAt: '2025-01-16T16:45:00Z',
    updatedAt: '2025-01-16T16:45:00Z',
    submittedAt: '2025-01-16T16:45:00Z',
    projectCode: 'PRJ-2025-003'
  },
  {
    id: 'req-005',
    title: 'Temporary Access Road Construction',
    description: 'Draft request for construction of temporary access road to facilitate heavy equipment delivery.',
    category: 'Site Work',
    priority: 'medium',
    status: 'draft',
    createdBy: 'u1',
    createdByName: 'John Chen',
    createdAt: '2025-01-17T09:00:00Z',
    updatedAt: '2025-01-17T09:00:00Z',
    projectCode: 'PRJ-2025-001',
    estimatedCost: 8000
  }
];

// Current user for demo (engineer)
export const currentUser = mockUsers[0];
