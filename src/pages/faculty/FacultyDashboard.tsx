import { useEffect, useState } from 'react'
import { supabase } from '../../lib/supabase'
import { useAuth } from '../../context/AuthContext'

interface Stats {
  students: number
  attendance: number
  marks: number
  notifications: number
}

export default function FacultyDashboard() {
  const { profile } = useAuth()
  const [stats, setStats] = useState<Stats>({
    students: 0,
    attendance: 0,
    marks: 0,
    notifications: 0,
  })
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    async function loadStats() {
      const [s, a, m, n] = await Promise.all([
        supabase.from('students').select('*', { count: 'exact', head: true }),
        supabase.from('attendance').select('*', { count: 'exact', head: true }),
        supabase.from('marks').select('*', { count: 'exact', head: true }),
        supabase.from('notifications').select('*', { count: 'exact', head: true }),
      ])

      setStats({
        students: s.count || 0,
        attendance: a.count || 0,
        marks: m.count || 0,
        notifications: n.count || 0,
      })
      setLoading(false)
    }
    loadStats()
  }, [])

  const cards = [
    { label: 'Total Students', value: stats.students, icon: '🎓' },
    { label: 'Attendance Records', value: stats.attendance, icon: '✅' },
    { label: 'Marks Records', value: stats.marks, icon: '📊' },
    { label: 'Notifications', value: stats.notifications, icon: '🔔' },
  ]

  return (
    <div>
      <div className="welcome-banner">
        <h1>Welcome, {profile?.name}</h1>
        <p>Faculty Dashboard — {profile?.department} Department</p>
      </div>

      {loading ? (
        <div style={{ textAlign: 'center', padding: '40px' }}>
          <div className="spinner" style={{ margin: '0 auto' }} />
        </div>
      ) : (
        <div className="dashboard-grid">
          {cards.map((card) => (
            <div className="dash-card" key={card.label}>
              <h3>{card.label}</h3>
              <div className="value">{card.value}</div>
              <div className="icon">{card.icon}</div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
