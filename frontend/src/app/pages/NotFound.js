import { Button } from "../components/ui/button";
import { useNavigate } from "react-router-dom";
import { Home, Search } from "lucide-react";

export default function NotFound() {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen w-full flex items-center justify-center bg-gradient-to-b from-gray-50 to-gray-100 dark:from-gray-900 dark:to-gray-800 px-4">
      <div className="max-w-md w-full space-y-8 text-center">
        <div className="space-y-4">
          <div className="relative">
            <h1 className="text-9xl font-bold text-gray-200 dark:text-gray-700">404</h1>
            <div className="absolute inset-0 flex items-center justify-center">
              <Search className="w-24 h-24 text-gray-400 dark:text-gray-600 animate-pulse" />
            </div>
          </div>
          
          <h2 className="text-3xl font-bold text-gray-900 dark:text-gray-100">
            Page Not Found
          </h2>
          
          <p className="text-gray-600 dark:text-gray-400 text-lg">
            Oops! The page you`&apos;`re looking for doesn`&apos;`t exist or has been moved.
          </p>
        </div>

        <div className="flex flex-col sm:flex-row gap-4 justify-center pt-4">
          <Button
            onClick={() => navigate("/")}
            className="gap-2"
            size="lg"
          >
            <Home className="w-4 h-4" />
            Back to Home
          </Button>
          
          <Button
            onClick={() => navigate(-1)}
            variant="outline"
            size="lg"
          >
            Go Back
          </Button>
        </div>
      </div>
    </div>
  );
}
