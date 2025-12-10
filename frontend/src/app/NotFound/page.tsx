"use client";

import { useEffect } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";


const NotFound = () => {

const pathName = usePathname();

  useEffect(() => {
    console.error("404 Error: User attempted to access non-existent route:", location.pathname);
  }, [pathName]);

  return (
    <div>
      <div>
        <h1>404</h1>
        <p>Oops! Page not found</p>
        <Link href="/">
          Return to Home
        </Link>
      </div>
    </div>
  );
};

export default NotFound;
