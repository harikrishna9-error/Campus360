import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { AuthProvider, useAuth } from './context/AuthContext'
import Login from './pages/Login'
import AdminDashboard from './pages/admin/AdminDashboard'
import FacultyDashboard from './pages/faculty/FacultyDashboard'
import StudentDashboard from './pages/student/StudentDashboard'
import Layout from './components/Layout'
import './index.css'

function ProtectedRoute({ children, roles }: { children: React.ReactNode; roles: string[] }) {
  const { session, profile, loading } = useAuth()

  if (loading) {
    return (
      <div className="auth-loading">
        <div className="spinner" />
        <p>Loading Campus360...</p>
      </div>
    )
  }

  if (!session || !profile) return <Navigate to="/login" replace />
  if (!roles.includes(profile.role)) return <Navigate to={`/${profile.role}`} replace />

  return <>{children}</>
}

function DashboardRouter() {
  const { profile } = useAuth()
  if (!profile) return <Navigate to="/login" replace />

  if (profile.role === 'admin') return <Navigate to="/admin" replace />
  if (profile.role === 'faculty') return <Navigate to="/faculty" replace />
  return <Navigate to="/student" replace />
}

function AppRoutes() {
  const { session, profile, loading } = useAuth()

  if (loading) {
    return (
      <div className="auth-loading">
        <div className="spinner" />
        <p>Loading Campus360...</p>
      </div>
    )
  }

  if (!session || !profile) {
    return (
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="*" element={<Navigate to="/login" replace />} />
      </Routes>
    )
  }

  return (
    <Routes>
      <Route path="/login" element={<Navigate to={`/${profile.role}`} replace />} />
      <Route path="/" element={<DashboardRouter />} />
      <Route
        path="/admin"
        element={
          <ProtectedRoute roles={['admin']}>
            <Layout />
          </ProtectedRoute>
        }
      >
        <Route index element={<AdminDashboard />} />
      </Route>
      <Route
        path="/faculty"
        element={
          <ProtectedRoute roles={['faculty']}>
            <Layout />
          </ProtectedRoute>
        }
      >
        <Route index element={<FacultyDashboard />} />
      </Route>
      <Route
        path="/student"
        element={
          <ProtectedRoute roles={['student']}>
            <Layout />
          </ProtectedRoute>
        }
      >
        <Route index element={<StudentDashboard />} />
      </Route>
      <Route path="*" element={<Navigate to={`/${profile.role}`} replace />} />
    </Routes>
  )
}

export default function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <AppRoutes />
      </BrowserRouter>
    </AuthProvider>
  )
}
