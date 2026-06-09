// Author:      Wajid Ali Chaudhry
// Description: Root component — sets up the router and wraps the
//              app in the AuthProvider.
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { AuthProvider, useAuth } from '@/context/AuthContext'
import LoginPage from '@/pages/LoginPage'
import RegisterPage from '@/pages/RegisterPage'
import AppLayout from '@/pages/AppLayout'
import DashboardPage from '@/pages/DashboardPage'
import ExpensesPage from '@/pages/ExpensesPage'
import AddExpensePage from '@/pages/AddExpensePage'
import EditExpensePage from '@/pages/EditExpensePage'

// Redirects to / if the user has no access token
function PrivateRoute({ children }: { children: React.ReactNode }) {
  const { accessToken } = useAuth()
  return accessToken ? <>{children}</> : <Navigate to="/" replace />
}

export default function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />
          {/* AppLayout wraps all private pages; Outlet renders the child */}
          <Route
            path="/app"
            element={<PrivateRoute><AppLayout /></PrivateRoute>}
          >
            <Route index element={<DashboardPage />} />
            <Route path="expenses" element={<ExpensesPage />} />
            <Route path="expenses/new" element={<AddExpensePage />} />
            <Route path="expenses/:id" element={<EditExpensePage />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  )
}