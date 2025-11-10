import { RequestForm } from "../components/request-form/request-form";
import { ClipboardList } from "lucide-react";

const Index = () => {
  return (
    <div className="min-h-screen bg-background">
      <div className="container mx-auto px-4 py-12">
        <div className="flex flex-col items-center mb-12 text-center">
          <div className="inline-flex items-center justify-center w-16 h-16 rounded-2xl bg-[var(--gradient-primary)] mb-4 shadow-[var(--shadow-soft)]">
            <ClipboardList className="w-8 h-8 text-white" />
          </div>
          <h1 className="text-4xl md:text-5xl font-bold mb-3 bg-[var(--gradient-primary)] bg-clip-text text-transparent">
            Work Request System
          </h1>
          <p className="text-lg text-muted-foreground max-w-2xl">
            Streamline your contracting workflow with our efficient approval process
          </p>
        </div>
        
        <div className="flex justify-center">
          <RequestForm />
        </div>
      </div>
    </div>
  );
};

export default Index;
