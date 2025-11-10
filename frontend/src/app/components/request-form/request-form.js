import { useState } from "react";
import { Button } from "../ui/button";
import { Input } from "../ui/input";
import { Label } from "../ui/label";
import { Textarea } from "../ui/textarea";

import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "../ui/select";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "../ui/card";
import { toast } from "sonner";
import { Calendar, DollarSign, AlertCircle, User, FileText } from "lucide-react";

// Mock approvers data
// ! In a real application, this would come from an API or global state
const approvers = [
  { id: "1", name: "Sarah Johnson", role: "Project Manager" },
  { id: "2", name: "Michael Chen", role: "Operations Director" },
  { id: "3", name: "Emily Rodriguez", role: "Department Head" },
  { id: "4", name: "David Kim", role: "Site Supervisor" },
];

export const RequestForm = () => {
  const [formData, setFormData] = useState({
    title: "",
    description: "",
    category: "",
    priority: "",
    dateNeeded: "",
    approverId: "",
  });

  const handleSubmit = (e) => {
    e.preventDefault();
    
    // Basic validation
    if (!formData.title || !formData.description || !formData.approverId) {
      toast.error("Please fill in all required fields");
      return;
    }

    const approver = approvers.find(a => a.id === formData.approverId);
    toast.success(`Request submitted to ${approver?.name} for approval!`);
    
    // Reset form
    setFormData({
      title: "",
      description: "",
      category: "",
      priority: "",
      dateNeeded: "",
      budget: "",
      approverId: "",
    });
  };

  return (
    <Card className="w-full max-w-3xl shadow-[var(--shadow-medium)] border-border/50 backdrop-blur-sm">
      <CardHeader className="space-y-1">
        <CardTitle className="text-3xl font-bold bg-[var(--gradient-primary)] bg-clip-text text-transparent">
          New Work Request
        </CardTitle>
        <CardDescription className="text-base">
          Submit a contracting work request for approval
        </CardDescription>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="space-y-2">
            <Label htmlFor="title" className="flex items-center gap-2 text-sm font-medium">
              <FileText className="w-4 h-4 text-primary" />
              Request Title *
            </Label>
            <Input
              id="title"
              placeholder="e.g., Office Renovation - Floor 3"
              value={formData.title}
              onChange={(e) => setFormData({ ...formData, title: e.target.value })}
              className="transition-all focus:shadow-[var(--shadow-soft)]"
              required
            />
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label htmlFor="category" className="text-sm font-medium">Category *</Label>
              <Select
                value={formData.category}
                onValueChange={(value) => setFormData({ ...formData, category: value })}
                required
              >
                <SelectTrigger id="category" className="transition-all focus:shadow-[var(--shadow-soft)]">
                  <SelectValue placeholder="Select category" />
                </SelectTrigger>
                <SelectContent className="bg-popover">
                  <SelectItem value="construction">Construction</SelectItem>
                  <SelectItem value="electrical">Electrical</SelectItem>
                  <SelectItem value="plumbing">Plumbing</SelectItem>
                  <SelectItem value="hvac">HVAC</SelectItem>
                  <SelectItem value="maintenance">Maintenance</SelectItem>
                  <SelectItem value="other">Other</SelectItem>
                </SelectContent>
              </Select>
            </div>

            <div className="space-y-2">
              <Label htmlFor="priority" className="flex items-center gap-2 text-sm font-medium">
                <AlertCircle className="w-4 h-4 text-accent" />
                Priority *
              </Label>
              <Select
                value={formData.priority}
                onValueChange={(value) => setFormData({ ...formData, priority: value })}
                required
              >
                <SelectTrigger id="priority" className="transition-all focus:shadow-[var(--shadow-soft)]">
                  <SelectValue placeholder="Select priority" />
                </SelectTrigger>
                <SelectContent className="bg-popover">
                  <SelectItem value="low">Low</SelectItem>
                  <SelectItem value="medium">Medium</SelectItem>
                  <SelectItem value="high">High</SelectItem>
                  <SelectItem value="urgent">Urgent</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>

          <div className="space-y-2">
            <Label htmlFor="description" className="text-sm font-medium">Description *</Label>
            <Textarea
              id="description"
              placeholder="Provide detailed information about the work request..."
              value={formData.description}
              onChange={(e) => setFormData({ ...formData, description: e.target.value })}
              className="min-h-[120px] transition-all focus:shadow-[var(--shadow-soft)] resize-none"
              required
            />
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label htmlFor="dateNeeded" className="flex items-center gap-2 text-sm font-medium">
                <Calendar className="w-4 h-4 text-primary" />
                Date Needed
              </Label>
              <Input
                id="dateNeeded"
                type="date"
                value={formData.dateNeeded}
                onChange={(e) => setFormData({ ...formData, dateNeeded: e.target.value })}
                className="transition-all focus:shadow-[var(--shadow-soft)]"
              />
            </div>
          </div>

          <div className="space-y-2">
            <Label htmlFor="approver" className="flex items-center gap-2 text-sm font-medium">
              <User className="w-4 h-4 text-primary" />
              Select Approver *
            </Label>
            <Select
              value={formData.approverId}
              onValueChange={(value) => setFormData({ ...formData, approverId: value })}
              required
            >
              <SelectTrigger id="approver" className="transition-all focus:shadow-[var(--shadow-soft)]">
                <SelectValue placeholder="Choose who should approve this request" />
              </SelectTrigger>
              <SelectContent className="bg-popover">
                {approvers.map((approver) => (
                  <SelectItem key={approver.id} value={approver.id}>
                    <div className="flex flex-col">
                      <span className="font-medium">{approver.name}</span>
                      <span className="text-xs text-muted-foreground">{approver.role}</span>
                    </div>
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>

          <Button 
            type="submit" 
            className="w-full bg-[var(--gradient-primary)] hover:opacity-90 transition-all shadow-[var(--shadow-soft)] hover:shadow-[var(--shadow-medium)]"
            size="lg"
          >
            Submit Request
          </Button>
        </form>
      </CardContent>
    </Card>
  );
};
