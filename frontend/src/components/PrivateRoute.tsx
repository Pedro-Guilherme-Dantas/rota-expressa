import { Navigate } from 'react-router-dom';
import type { ReactNode } from 'react';

interface PrivateRouteProps {
  children: ReactNode;
}

export default function PrivateRoute({ children }: PrivateRouteProps) {
  const token = localStorage.getItem('access_token');

  if (!token) {
    return <Navigate to="/" replace />;
  }

  return <>{children}</>;
}
