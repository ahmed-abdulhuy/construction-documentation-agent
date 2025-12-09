"use client";


// Detail view component with approval workflow
import { useState } from "react";
import { useRouter } from "next/navigation";
import { RequestDocument, RequestStatus } from "@/lib/types";
import { requestService } from "@/lib/requestService";
import { currentUser } from "@/lib/mockData";
// import { toast } from "sonner";
import Grid from '@mui/material/Grid'



import {
  Card,
  CardContent,
  Button,
  Chip,
  Typography,
  Box,
  TextField,
  Divider,
  Paper,
} from "@mui/material";

import {
  ArrowBack,
  Edit,
  CalendarMonth,
  Person,
  Description,
  MonetizationOn,
  CheckCircle,
  Cancel,
  AccessTime,
} from "@mui/icons-material";


interface RequestDetailProps {
  request: RequestDocument;
}

export default function RequestDetail({ request: initialRequest }: RequestDetailProps) {
  const router = useRouter();
  
  const [request, setRequest] = useState(initialRequest);
  const [reviewNotes, setReviewNotes] = useState("");
  const [isReviewing, setIsReviewing] = useState(false);

  const canEdit = currentUser.role === 'engineer' && 
    (request.status === 'draft' || request.status === 'rejected');
  
  const canReview = currentUser.role === 'approver' && request.status === 'pending';

  const statusConfig = {
    draft: { 
      label: 'Draft', 
      className: 'bg-muted text-muted-foreground',
      icon: <Description fontSize="small" /> 
    },
    pending: { 
      label: 'Pending Review', 
      className: 'bg-warning text-warning-foreground',
      icon: <AccessTime fontSize="small" /> 
    },
    approved: { 
      label: 'Approved', 
      className: 'bg-success text-success-foreground',
      icon: <CheckCircle fontSize="small" /> 
    },
    rejected: { 
      label: 'Rejected', 
      className: 'bg-destructive text-destructive-foreground',
      icon: <Cancel fontSize="small" /> 
    },
  };

  //! Disabled until configuring Update 
  // const handleStatusUpdate = (newStatus: RequestStatus) => {
  //   const updated = requestService.updateRequestStatus(
  //     request.id,
  //     newStatus,
  //     newStatus !== 'draft' && newStatus !== 'pending' ? {
  //       reviewedBy: currentUser.id,
  //       reviewerName: currentUser.name,
  //       reviewNotes: reviewNotes || undefined,
  //     } : undefined
  //   );

  //   if (updated) {
  //     setRequest(updated);
  //     setReviewNotes('');
  //     setIsReviewing(false);
  //   //   toast.success(`Request ${newStatus === 'approved' ? 'approved' : 'rejected'}`);
  //   }
  // };

  const statusMeta = statusConfig[request.status];

  return (
    <Box sx={{ display: "flex", flexDirection: "column", gap: 3 }}>
      {/* Header Actions */}
      <Box
        sx={{
          display: "flex",
          flexWrap: "wrap",
          alignItems: "center",
          justifyContent: "space-between",
          gap: 2,
        }}
      >
        <Box sx={{ display: "flex", gap: 2, alignItems: "center" }}>
          <Button
            variant="outlined"
            size="small"
            onClick={() => router.push("/Dashboard")}
            startIcon={<ArrowBack />}
          >
            Back to List
          </Button>

          <Chip
            label={
              <Box sx={{ display: "flex", alignItems: "center", gap: 0.5 }}>
                {statusMeta.icon}
                {statusMeta.label}
              </Box>
            }
            // color={statusMeta.color as any}
            variant="filled"
            sx={{ fontSize: "0.875rem", px: 1.5 }}
          />
        </Box>

        {/* {canEdit && (
          <Button
            variant="contained"
            startIcon={<Edit />}
            onClick={() => router.push(`/RequestDetails/${request.id}/edit`)}
          >
            Edit Request
          </Button>
        )} */}
      </Box>

      {/* Main Card */}
      <Card elevation={3}>
        <CardContent sx={{ display: "flex", flexDirection: "column", gap: 4 }}>
          {/* Title Section */}
          <Box>
            <Typography variant="h4" fontWeight="bold" gutterBottom>
              {request.title}
            </Typography>

            <Box
              sx={{
                display: "flex",
                flexWrap: "wrap",
                gap: 2,
                color: "text.secondary",
                fontSize: "0.875rem",
              }}
            >
              <Box sx={{ display: "flex", alignItems: "center", gap: 0.5 }}>
                <Description fontSize="small" />
                {request.category}
              </Box>

              <Chip label={request.priority} variant="outlined" size="small" />

              {request.projectCode && (
                <Box sx={{ display: "flex", alignItems: "center", gap: 0.5 }}>
                  <Description fontSize="small" />
                  <Typography
                    component="span"
                    sx={{ fontFamily: "monospace", fontSize: "0.875rem" }}
                  >
                    {request.projectCode}
                  </Typography>
                </Box>
              )}
            </Box>
          </Box>

          <Divider />

          {/* Description */}
          <Box>
            <Typography variant="h6" gutterBottom>
              Description
            </Typography>
            <Typography
              sx={{
                whiteSpace: "pre-wrap",
                color: "text.secondary",
                fontSize: "0.95rem",
              }}
            >
              {request.description}
            </Typography>
          </Box>

          <Divider />

          {/* Details Grid */}
          <Grid container spacing={3} >
            {/* Left column */}
            <Grid size={{ xs: 12, md: 6 }}>
              <Typography
                variant="subtitle2"
                sx={{ color: "text.secondary", mb: 1 }}
              >
                Request Details
              </Typography>

              <Box sx={{ display: "flex", flexDirection: "column", gap: 1 }}>
                <DetailRow
                  icon={<Person fontSize="small" />}
                  label="Created by:"
                  value={request.createdByName}
                />

                <DetailRow
                  icon={<CalendarMonth fontSize="small" />}
                  label="Created:"
                  value={new Date(request.createdAt).toLocaleString()}
                />

                {request.submittedAt && (
                  <DetailRow
                    icon={<CalendarMonth fontSize="small" />}
                    label="Submitted:"
                    value={new Date(request.submittedAt).toLocaleString()}
                  />
                )}

                {request.estimatedCost && (
                  <DetailRow
                    icon={<MonetizationOn fontSize="small" />}
                    label="Estimated Cost:"
                    value={`$${request.estimatedCost.toLocaleString()}`}
                  />
                )}
              </Box>
            </Grid>

            {/* Right column */}
            {(request.reviewedAt || request.reviewNotes) && (
              <Grid size={{ xs: 12, md: 6 }}>
                <Typography
                  variant="subtitle2"
                  sx={{ color: "text.secondary", mb: 1 }}
                >
                  Review Information
                </Typography>

                <Box sx={{ display: "flex", flexDirection: "column", gap: 1 }}>
                  {request.reviewerName && (
                    <DetailRow
                      icon={<Person fontSize="small" />}
                      label="Reviewed by:"
                      value={request.reviewerName}
                    />
                  )}

                  {request.reviewedAt && (
                    <DetailRow
                      icon={<CalendarMonth fontSize="small" />}
                      label="Reviewed:"
                      value={new Date(request.reviewedAt).toLocaleString()}
                    />
                  )}

                  {request.reviewNotes && (
                    <Paper
                      sx={{
                        p: 2,
                        mt: 1,
                        backgroundColor: "action.hover",
                      }}
                    >
                      <Typography variant="subtitle2" gutterBottom>
                        Review Notes:
                      </Typography>
                      <Typography variant="body2" color="text.secondary">
                        {request.reviewNotes}
                      </Typography>
                    </Paper>
                  )}
                </Box>
              </Grid>
            )}
          </Grid>

          {/* Review Section */}
          {canReview && (
            <Box>
              <Typography variant="h6" gutterBottom>
                Review Request
              </Typography>

              {!isReviewing ? (
                <Box sx={{ display: "flex", gap: 2 }}>
                  <Button
                    variant="contained"
                    color="success"
                    startIcon={<CheckCircle />}
                    onClick={() => setIsReviewing(true)}
                  >
                    Approve
                  </Button>

                  <Button
                    variant="contained"
                    color="error"
                    startIcon={<Cancel />}
                    onClick={() => setIsReviewing(true)}
                  >
                    Reject
                  </Button>
                </Box>
              ) : (
                <Box sx={{ display: "flex", flexDirection: "column", gap: 3 }}>
                  <TextField
                    label="Review Notes (Optional)"
                    multiline
                    minRows={4}
                    fullWidth
                    value={reviewNotes}
                    onChange={(e) => setReviewNotes(e.target.value)}
                  />

                  {/*! Disabled until configuring update */}
                  {/* <Box sx={{ display: "flex", gap: 2 }}>
                    <Button
                      variant="contained"
                      color="success"
                      startIcon={<CheckCircle />}
                      onClick={() => handleStatusUpdate("approved")}
                    >
                      Confirm Approval
                    </Button>

                    <Button
                      variant="contained"
                      color="error"
                      startIcon={<Cancel />}
                      onClick={() => handleStatusUpdate("rejected")}
                    >
                      Confirm Rejection
                    </Button>

                    <Button
                      variant="outlined"
                      onClick={() => {
                        setIsReviewing(false);
                        setReviewNotes("");
                      }}
                    >
                      Cancel
                    </Button>
                  </Box> */}
                </Box>
              )}
            </Box>
          )}
        </CardContent>
      </Card>
    </Box>
  );
}


function DetailRow({
  icon,
  label,
  value,
}: {
  icon: React.ReactNode;
  label: string;
  value: string | number;
}) {
  return (
    <Box sx={{ display: "flex", alignItems: "center", gap: 1 }}>
      {icon}
      <Typography variant="body2">
        <strong>{label}</strong> {value}
      </Typography>
    </Box>
  );
}
