"use client"

// Form component with business logic
import { useState } from "react";
import { useRouter } from "next/navigation";

import {
  TextField,
  MenuItem,
  Card,
  CardContent,
  Typography,
  Box,
  Button,
  Grid,
} from "@mui/material";

import { Save, Send, ArrowBack } from "@mui/icons-material";

import { RequestDocument, RequestPriority } from "@/lib/types";
import { requestService } from "@/lib/requestService";
import { currentUser } from "@/lib/mockData";
import { toast } from "sonner";

interface RequestFormProps {
  initialData?: RequestDocument;
  mode: 'create' | 'edit';
}

export function RequestForm({ initialData, mode }: RequestFormProps) {
  const router = useRouter();

  const [formData, setFormData] = useState({
    title: initialData?.title || "",
    description: initialData?.description || "",
    category: initialData?.category || "",
    priority: (initialData?.priority || "medium") as RequestPriority,
    projectCode: initialData?.projectCode || "",
    estimatedCost: initialData?.estimatedCost?.toString() || "",
  });

  const categories = [
    'Materials',
    'Equipment',
    'Design Change',
    'Documentation',
    'Site Work',
    'Safety',
    'Other'
  ];

  const handleChange =
    (field: string) => (e: React.ChangeEvent<HTMLInputElement>) => {
      setFormData((prev) => ({ ...prev, [field]: e.target.value }));
  };

  const handleSubmit = (status: 'draft' | 'pending') => {
    if (!formData.title.trim()) {
      toast.error('Please enter a title');
      return;
    }
    if (!formData.description.trim()) {
      toast.error('Please enter a description');
      return;
    }
    if (!formData.category) {
      toast.error('Please select a category');
      return;
    }

    try {
      if (mode === 'create') {
        const newRequest = requestService.createRequest({
          ...formData,
          estimatedCost: formData.estimatedCost ? parseFloat(formData.estimatedCost) : undefined,
          status,
          createdBy: currentUser.id,
          createdByName: currentUser.name,
          submittedAt: status === 'pending' ? new Date().toISOString() : undefined,
        });
        toast.success(
          status === 'draft' 
            ? 'Request saved as draft' 
            : 'Request submitted for approval'
        );
        router.push(`/RequestDetails/${newRequest.id}`);
      } else if (initialData) {
        requestService.updateRequest(initialData.id, {
          ...formData,
          estimatedCost: formData.estimatedCost ? parseFloat(formData.estimatedCost) : undefined,
          status,
          submittedAt: status === 'pending' && !initialData.submittedAt 
            ? new Date().toISOString() 
            : initialData.submittedAt,
        });
        toast.success('Request updated successfully');
        router.push(`/RequestDetails/${initialData.id}`);
      }
    } catch (error) {
      toast.error('Failed to save request');
    }
  };

  return (
        <Box sx={{ display: "flex", flexDirection: "column", gap: 3 }}>
      {/* Header */}
      <Box sx={{ display: "flex", alignItems: "center", gap: 2 }}>
        <Button
          variant="outlined"
          size="small"
          onClick={() => router.back()}
          startIcon={<ArrowBack />}
        >
          Back
        </Button>

        <Typography variant="h4" fontWeight="bold">
          {mode === "create" ? "Create New Request" : "Edit Request"}
        </Typography>
      </Box>

      {/* Form Card */}
      <Card elevation={3}>
        <CardContent sx={{ display: "flex", flexDirection: "column", gap: 3 }}>
          {/* Title */}
          <TextField
            label="Request Title *"
            fullWidth
            value={formData.title}
            onChange={handleChange("title")}
            placeholder="Brief description of the request"
          />

          {/* Description */}
          <TextField
            label="Description *"
            fullWidth
            multiline
            minRows={5}
            value={formData.description}
            onChange={handleChange("description")}
            placeholder="Detailed description including justification"
          />

          {/* Category + Priority */}
          <Grid container spacing={3}>
            <Grid size={{ xs: 12, md: 6 }}>
              <TextField
                select
                label="Category *"
                fullWidth
                value={formData.category}
                onChange={(e) =>
                  setFormData((prev) => ({ ...prev, category: e.target.value }))
                }
              >
                {categories.map((cat) => (
                  <MenuItem key={cat} value={cat}>
                    {cat}
                  </MenuItem>
                ))}
              </TextField>
            </Grid>

            <Grid size={{ xs: 12, md: 6 }}>
              <TextField
                select
                label="Priority *"
                fullWidth
                value={formData.priority}
                onChange={(e) =>
                  setFormData((prev) => ({
                    ...prev,
                    priority: e.target.value as RequestPriority,
                  }))
                }
              >
                <MenuItem value="low">Low</MenuItem>
                <MenuItem value="medium">Medium</MenuItem>
                <MenuItem value="high">High</MenuItem>
                <MenuItem value="urgent">Urgent</MenuItem>
              </TextField>
            </Grid>
          </Grid>

          {/* Project Code + Estimated Cost */}
          <Grid container spacing={3}>
            <Grid size={{ xs: 12, md: 6 }}>
              <TextField
                label="Project Code"
                fullWidth
                value={formData.projectCode}
                onChange={handleChange("projectCode")}
              />
            </Grid>

            <Grid size={{ xs: 12, md: 6 }}>
              <TextField
                label="Estimated Cost ($)"
                type="number"
                fullWidth
                value={formData.estimatedCost}
                onChange={handleChange("estimatedCost")}
                placeholder="0.00"
              />
            </Grid>
          </Grid>

          {/* Actions */}
          <Box sx={{ display: "flex", gap: 2, pt: 2 }}>
            <Button
              variant="outlined"
              startIcon={<Save />}
              onClick={() => handleSubmit("draft")}
              sx={{ flex: 1 }}
            >
              Save as Draft
            </Button>

            <Button
              variant="contained"
              startIcon={<Send />}
              onClick={() => handleSubmit("pending")}
              sx={{ flex: 1 }}
            >
              Submit for Approval
            </Button>
          </Box>
        </CardContent>
      </Card>
    </Box>

  );
}
