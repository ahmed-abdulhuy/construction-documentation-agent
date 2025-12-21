"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { NewRequestData } from "@/lib/types";
import {
  Card,
  CardContent,
  TextField,
  Typography,
  Button,
  Box,
  Grid,
  Divider,
  MenuItem,
} from "@mui/material";
import { ArrowBack, Save } from "@mui/icons-material";
import { requestService } from "@/lib/requestService";


export default function CreateRequestPage() {
  const router = useRouter();

  const [form, setForm] = useState<NewRequestData>({
        title: "",
        description: "",
        category: "",
        priority: "medium",
        status: "draft",
  });

  const [submitting, setSubmitting] = useState(false);

  const handleChange = (key: string, value: any) => {
    setForm((prev) => ({ ...prev, [key]: value }));
  };

  async function handleSubmit() {
    setSubmitting(true);
    try {
      if (!form) throw new Error("Form is incomplete");  
      const created = await requestService.createRequest(form);

      router.push(`/RequestDetails/${created.id}`);
    } catch (err) {
      console.error(err);
      alert("Failed to create request");
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <Box sx={{ display: "flex", flexDirection: "column", gap: 3 }}>
      {/* Header */}
      <Box
        sx={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
        }}
      >
        <Button
          variant="outlined"
          startIcon={<ArrowBack />}
          onClick={() => router.push("/Dashboard")}
        >
          Back to List
        </Button>

        <Typography variant="h5" fontWeight="bold">
          Create New Request
        </Typography>
      </Box>

      {/* Card */}
      <Card elevation={3}>
        <CardContent sx={{ display: "flex", flexDirection: "column", gap: 4 }}>
          <Typography variant="h6">Request Information</Typography>

          <Grid container spacing={3}>
            <Grid size={{xs: 12, md: 6}}>
              <TextField
                fullWidth
                label="Title"
                value={form.title}
                onChange={(e) => handleChange("title", e.target.value)}
              />
            </Grid>

            <Grid size={{xs: 12, md: 6}}>
              <TextField
                fullWidth
                select
                label="Category"
                value={form.category}
                onChange={(e) => handleChange("category", e.target.value)}
              >
                <MenuItem value="maintenance">Maintenance</MenuItem>
                <MenuItem value="procurement">Procurement</MenuItem>
                <MenuItem value="planning">Planning</MenuItem>
              </TextField>
            </Grid>

            <Grid size={{xs: 12, md: 6}}>
              <TextField
                fullWidth
                select
                label="Priority"
                value={form.priority}
                onChange={(e) => handleChange("priority", e.target.value)}
              >
                <MenuItem value="low">Low</MenuItem>
                <MenuItem value="medium">Medium</MenuItem>
                <MenuItem value="high">High</MenuItem>
              </TextField>
            </Grid>
          </Grid>

          <Divider />

          <Box>
            <Typography variant="h6">Description</Typography>
            <TextField
              fullWidth
              multiline
              minRows={5}
              value={form.description}
              onChange={(e) => handleChange("description", e.target.value)}
            />
          </Box>

          <Box sx={{ display: "flex", justifyContent: "flex-end", gap: 2 }}>
            <Button
              variant="contained"
              color="primary"
              startIcon={<Save />}
              disabled={submitting}
              onClick={handleSubmit}
            >
              {submitting ? "Submitting..." : "Create Request"}
            </Button>
          </Box>
        </CardContent>
      </Card>
    </Box>
  );
}
