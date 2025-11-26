"use client"

// Business logic component - uses UI components but contains the logic
import { useState, useMemo, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { RequestDocument, RequestFilters, RequestStatus, RequestPriority } from '@/lib/types';
import { requestService } from '@/lib/requestService';
import { RequestCard } from './RequestCard';
import { RequestFiltersUI } from './RequestFiltersUI';
import { Box, Button, TextField, InputAdornment, Grid } from "@mui/material";
import SearchIcon from "@mui/icons-material/Search";
import AddIcon from "@mui/icons-material/Add";


export function RequestList() {
  const router = useRouter();
  const [filters, setFilters] = useState<RequestFilters>({});
  const [searchTerm, setSearchTerm] = useState('');
  const [requests, setRequests] = useState<RequestDocument[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function loadRequests() {
      try {
        setLoading(true);
        setError(null);

        const data = await requestService.filterRequests({
          ...filters,
          searchTerm: searchTerm || undefined,
        });

        setRequests(data);
      } catch (err) {
        setError("Failed to load requests");
      } finally {
        setLoading(false);
      }
    }

    loadRequests();
  }, [filters, searchTerm]);

  // const requests = useMemo(() => {
  //   return requestService.filterRequests({
  //     ...filters,
  //     searchTerm: searchTerm || undefined
  //   });
  // }, [filters, searchTerm]);

  const handleStatusFilterChange = (statuses: RequestStatus[]) => {
    setFilters(prev => ({ ...prev, status: statuses.length ? statuses : undefined }));
  };

  const handlePriorityFilterChange = (priorities: RequestPriority[]) => {
    setFilters(prev => ({ ...prev, priority: priorities.length ? priorities : undefined }));
  };

  const handleRequestClick = (id: string) => {
    router.push(`/RequestDetails/${id}`);
  };

  const handleCreateNew = () => {
    router.push('/RequestDetails/new');
  };

  return (
    <Box display="flex" flexDirection="column" gap={4}>
      {/* Search + New Button */}
      <Grid container spacing={2} alignItems="center">
        <Grid size={{ xs: 12, md: 8 }}>
          <TextField
            fullWidth
            placeholder="Search requests by title, description, or project code..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            InputProps={{
              startAdornment: (
                <InputAdornment position="start">
                  <SearchIcon fontSize="small" />
                </InputAdornment>
              ),
            }}
          />
        </Grid>

        <Grid size={{ xs: 12, md: 4 }} display="flex" justifyContent={{ xs: "flex-start", md: "flex-end" }}>
          <Button
            variant="contained"
            startIcon={<AddIcon />}
            onClick={handleCreateNew}
          >
            New Request
          </Button>
        </Grid>
      </Grid>

      {/* Filters */}
      <RequestFiltersUI
        selectedStatuses={filters.status || []}
        selectedPriorities={filters.priority || []}
        onStatusChange={handleStatusFilterChange}
        onPriorityChange={handlePriorityFilterChange}
      />

      {/* Request Cards */}
      <Box>
        {requests.length === 0 ? (
          <Box textAlign="center" py={6} color="text.secondary">
            No requests found. Create your first request to get started.
          </Box>
        ) : (
          <Box display="flex" flexDirection="column" gap={2}>
            {requests.map((req: RequestDocument) => (
              <RequestCard
                key={req.id}
                request={req}
                onClick={() => handleRequestClick(req.id)}
              />
            ))}
          </Box>
        )}
      </Box>
    </Box>

  );
}
