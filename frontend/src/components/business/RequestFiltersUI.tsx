// UI component for filters
import { RequestStatus, RequestPriority } from '@/lib/types';
import Chip from "@mui/material/Chip";
import Stack from "@mui/material/Stack";
import Typography from "@mui/material/Typography";

interface RequestFiltersUIProps {
  selectedStatuses: RequestStatus[];
  selectedPriorities: RequestPriority[];
  onStatusChange: (statuses: RequestStatus[]) => void;
  onPriorityChange: (priorities: RequestPriority[]) => void;
}

export function RequestFiltersUI({
  selectedStatuses,
  selectedPriorities,
  onStatusChange,
  onPriorityChange,
}: RequestFiltersUIProps) {
  const statuses: { value: RequestStatus; label: string }[] = [
    { value: 'draft', label: 'Draft' },
    { value: 'pending', label: 'Pending' },
    { value: 'approved', label: 'Approved' },
    { value: 'rejected', label: 'Rejected' },
  ];

  const priorities: { value: RequestPriority; label: string }[] = [
    { value: 'low', label: 'Low' },
    { value: 'medium', label: 'Medium' },
    { value: 'high', label: 'High' },
    { value: 'urgent', label: 'Urgent' },
  ];

  const toggleStatus = (status: RequestStatus) => {
    if (selectedStatuses.includes(status)) {
      onStatusChange(selectedStatuses.filter(s => s !== status));
    } else {
      onStatusChange([...selectedStatuses, status]);
    }
  };

  const togglePriority = (priority: RequestPriority) => {
    if (selectedPriorities.includes(priority)) {
      onPriorityChange(selectedPriorities.filter(p => p !== priority));
    } else {
      onPriorityChange([...selectedPriorities, priority]);
    }
  };

  return (
    <Stack spacing={2}>
      {/* Status Filter */}
      <Stack direction="row" alignItems="center" spacing={1} flexWrap="wrap">
        <Typography variant="body2" fontWeight={600}>
          Status:
        </Typography>

        {statuses.map(({ value, label }) => {
          const selected = selectedStatuses.includes(value);

          return (
            <Chip
              key={value}
              label={label}
              clickable
              onClick={() => toggleStatus(value)}
              variant={selected ? "filled" : "outlined"}
              color={selected ? "primary" : "default"}
              sx={{
                cursor: "pointer",
                borderRadius: "8px",
              }}
            />
          );
        })}
      </Stack>

      {/* Priority Filter */}
      <Stack direction="row" alignItems="center" spacing={1} flexWrap="wrap">
        <Typography variant="body2" fontWeight={600}>
          Priority:
        </Typography>

        {priorities.map(({ value, label }) => {
          const selected = selectedPriorities.includes(value);

          return (
            <Chip
              key={value}
              label={label}
              clickable
              onClick={() => togglePriority(value)}
              variant={selected ? "filled" : "outlined"}
              color={selected ? "primary" : "default"}
              sx={{
                cursor: "pointer",
                borderRadius: "8px",
              }}
            />
          );
        })}
      </Stack>
    </Stack>

  );
}
