import { useState } from 'react'
import { Outlet, useLocation } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

interface NavItem {
  label: string
  path: string
  icon: string
}

const adminNav: NavItem[] = [
  { label: 'Dashboard', path: '/admin', icon: '🏠' },
  { label: 'Students', path: '/admin/students', icon: '🎓' },
  { label: 'Faculty', path: '/admin/faculty', icon: '👨‍🏫' },
  { label: 'Attendance', path: '/admin/attendance', icon: '✅' },
  { label: 'Marks', path: '/admin/marks', icon: '📊' },
  { label: 'Timetable', path: '/admin/timetable', icon: '📅' },
  { label: 'Library', path: '/admin/library', icon: '📚' },
  { label: 'Fees', path: '/admin/fees', icon: '💳' },
  { label: 'Notifications', path: '/admin/notifications', icon: '🔔' },
  { label: 'Exams', path: '/admin/exams', icon: '📝' },
  { label: 'Results', path: '/admin/results', icon: '📈' },
  { label: 'Backlogs', path: '/admin/backlogs', icon: '⚠️' },
  { label: 'Hall Tickets', path: '/admin/halltickets', icon: '🎫' },
  { label: 'Payments', path: '/admin/payments', icon: '💰' },
  { label: 'Receipts', path: '/admin/receipts', icon: '🧾' },
  { label: 'Reports', path: '/admin/reports', icon: '📋' },
  { label: 'Profile', path: '/admin/profile', icon: '👤' },
  { label: 'Settings', path: '/admin/settings', icon: '⚙️' },
]

const facultyNav: NavItem[] = [
  { label: 'Dashboard', path: '/faculty', icon: '🏠' },
  { label: 'Students', path: '/faculty/students', icon: '🎓' },
  { label: 'Attendance', path: '/faculty/attendance', icon: '✅' },
  { label: 'Marks', path: '/faculty/marks', icon: '📊' },
  { label: 'Timetable', path: '/faculty/timetable', icon: '📅' },
  { label: 'Notifications', path: '/faculty/notifications', icon: '🔔' },
  { label: 'Profile', path: '/faculty/profile', icon: '👤' },
]

const studentNav: NavItem[] = [
  { label: 'Dashboard', path: '/student', icon: '🏠' },
  { label: 'Profile', path: '/student/profile', icon: '👤' },
  { label: 'Attendance', path: '/student/attendance', icon: '✅' },
  { label: 'Marks', path: '/student/marks', icon: '📊' },
  { label: 'Results', path: '/student/results', icon: '📈' },
  { label: 'Backlogs', path: '/student/backlogs', icon: '⚠️' },
  { label: 'Hall Ticket', path: '/student/hallticket', icon: '🎫' },
  { label: 'Timetable', path: '/student/timetable', icon: '📅' },
  { label: 'Exams', path: '/student/exams', icon: '📝' },
  { label: 'Fees', path: '/student/fees', icon: '💳' },
  { label: 'Library', path: '/student/library', icon: '📚' },
  { label: 'Book Search', path: '/student/book-search', icon: '🔍' },
  { label: 'Payments', path: '/student/payments', icon: '💰' },
  { label: 'Receipts', path: '/student/receipts', icon: '🧾' },
  { label: 'Notifications', path: '/student/notifications', icon: '🔔' },
  { label: 'Change Password', path: '/student/change-password', icon: '🔑' },
]

function getNavItems(role: string): NavItem[] {
  if (role === 'admin') return adminNav
  if (role === 'faculty') return facultyNav
  return studentNav
}

function getPageTitle(pathname: string, navItems: NavItem[]): string {
  const match = navItems.find((item) => pathname === item.path || (item.path !== `/${pathname.split('/')[1]}` && pathname.startsWith(item.path) && item.path !== '/admin' && item.path !== '/faculty' && item.path !== '/student'))
  return match?.label || 'Dashboard'
}

export default function Layout() {
  const { profile, signOut } = useAuth()
  const location = useLocation()
  const [sidebarOpen, setSidebarOpen] = useState(false)

  if (!profile) return null

  const navItems = getNavItems(profile.role)
  const title = getPageTitle(location.pathname, navItems)
  const initials = profile.name.charAt(0).toUpperCase()

  return (
    <div className="layout">
      <button className="mobile-toggle" onClick={() => setSidebarOpen(!sidebarOpen)}>
        ☰
      </button>

      <aside className={`sidebar ${sidebarOpen ? 'open' : ''}`}>
        <div className="sidebar-header">
          <h2>Campus360</h2>
          <span className="role-badge">{profile.role}</span>
        </div>
        <ul className="sidebar-nav">
          {navItems.map((item) => (
            <li key={item.path}>
              <a
                href={item.path}
                className={location.pathname === item.path ? 'active' : ''}
                onClick={() => setSidebarOpen(false)}
              >
                <span className="icon">{item.icon}</span>
                {item.label}
              </a>
            </li>
          ))}
          <li>
            <a
              href="/login"
              onClick={(e) => {
                e.preventDefault()
                signOut()
              }}
            >
              <span className="icon">🚪</span>
              Logout
            </a>
          </li>
        </ul>
      </aside>

      <div className="main-area">
        <div className="topbar">
          <h1>{title}</h1>
          <div className="user-info">
            <div>
              <div className="user-name">{profile.name}</div>
              <div className="user-role">{profile.role}</div>
            </div>
            <div className="user-avatar">{initials}</div>
          </div>
        </div>
        <div className="fade-in">
          <Outlet />
        </div>
      </div>
    </div>
  )
}
