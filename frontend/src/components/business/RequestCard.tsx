// Presentational component with minimal logic
import { RequestDocument } from '@/lib/types';
import {
  Card,
  CardContent,
  Box,
  Typography,
  Chip,
  Stack,
} from "@mui/material";
import DescriptionIcon from "@mui/icons-material/Description";
import CalendarMonthIcon from "@mui/icons-material/CalendarMonth";
import PersonIcon from "@mui/icons-material/Person";
import MonetizationOnIcon from "@mui/icons-material/MonetizationOn";

interface RequestCardProps {
  request: RequestDocument;
  onClick?: () => void;
}

export function RequestCard({ request, onClick }: RequestCardProps) {
  const statusConfig = {
    draft: { label: "Draft", color: "default" as const },
    pending: { label: "Pending Review", color: "warning" as const },
    approved: { label: "Approved", color: "success" as const },
    rejected: { label: "Rejected", color: "error" as const },
  };

  // Priority visual mapping
  const priorityConfig = {
    low: { label: "Low", color: "secondary" as const },
    medium: { label: "Medium", color: "primary" as const },
    high: { label: "High", color: "warning" as const },
    urgent: { label: "Urgent", color: "error" as const },
  };

  const statusInfo = statusConfig[request.status];
  const priorityInfo = priorityConfig[request.priority];

  return (
    <Card
      variant="outlined"
      sx={{
        cursor: "pointer",
        borderLeftWidth: 6,
        borderLeftColor:
          request.status === "approved"
            ? "success.main"
            : request.status === "rejected"
            ? "error.main"
            : request.status === "pending"
            ? "warning.main"
            : "grey.400",
        transition: "0.2s",
        "&:hover": {
          boxShadow: 4,
        },
      }}
      onClick={onClick}
    >
      <CardContent>
        <Stack spacing={2}>
          {/* Title, Description, Status & Priority */}
          <Stack direction="row" justifyContent="space-between" spacing={2}>
            {/* Title + Description */}
            <Box flex={1} minWidth={0}>
              <Typography variant="h6" fontWeight={600} gutterBottom noWrap>
                {request.title}
              </Typography>
              <Typography
                variant="body2"
                color="text.secondary"
                sx={{
                  display: "-webkit-box",
                  WebkitLineClamp: 2,
                  WebkitBoxOrient: "vertical",
                  overflow: "hidden",
                }}
              >
                {request.description}
              </Typography>
            </Box>

            {/* Status & Priority */}
            <Stack direction="row" spacing={1} flexShrink={0}>
              <Chip label={statusInfo.label} color={statusInfo.color} size="small" />
              <Chip label={priorityInfo.label} color={priorityInfo.color} size="small" />
            </Stack>
          </Stack>

          {/* Metadata row */}
          <Stack
            direction="row"
            spacing={3}
            flexWrap="wrap"
            sx={{ color: "text.secondary", fontSize: 14 }}
          >
            {/* Category */}
            <Box display="flex" alignItems="center" gap={1}>
              <DescriptionIcon fontSize="small" />
              <span>{request.category}</span>
            </Box>

            {/* Project Code */}
            {request.projectCode && (
              <Box display="flex" alignItems="center" gap={1}>
                <DescriptionIcon fontSize="small" />
                <Typography fontFamily="monospace">
                  {request.projectCode}
                </Typography>
              </Box>
            )}

            {/* Created By */}
            <Box display="flex" alignItems="center" gap={1}>
              <PersonIcon fontSize="small" />
              <span>{request.createdByName}</span>
            </Box>

            {/* Created At */}
            <Box display="flex" alignItems="center" gap={1}>
              <CalendarMonthIcon fontSize="small" />
              <span>{new Date(request.createdAt).toLocaleDateString()}</span>
            </Box>

            {/* Estimated Cost */}
            {request.estimatedCost && (
              <Box display="flex" alignItems="center" gap={1}>
                <MonetizationOnIcon fontSize="small" />
                <span>${request.estimatedCost.toLocaleString()}</span>
              </Box>
            )}
          </Stack>
        </Stack>
      </CardContent>
    </Card>

  );
}
