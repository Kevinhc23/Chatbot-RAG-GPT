"use client";
import { useAuth } from "@/contexts/AuthContext";
import { useRouter } from "next/navigation";
import { ReactNode, useEffect } from "react";

interface ProtectedRouteProps {
  children: ReactNode;
  requireAuth?: boolean;
}

export default function ProtectedRoute({
  children,
  requireAuth = true,
}: ProtectedRouteProps) {
  const { user, isLoading } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!isLoading) {
      if (requireAuth && !user) {
        router.push("/login");
      } else if (!requireAuth && user) {
        router.push("/chat");
      }
    }
  }, [user, isLoading, router, requireAuth]);

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50 dark:bg-gray-900">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600 dark:text-gray-400">Cargando...</p>
        </div>
      </div>
    );
  }

  // Si requiere autenticación pero no hay usuario, no mostrar nada (redirecciona)
  if (requireAuth && !user) {
    return null;
  }

  // Si no requiere autenticación pero hay usuario, no mostrar nada (redirecciona)
  if (!requireAuth && user) {
    return null;
  }

  return <>{children}</>;
}
