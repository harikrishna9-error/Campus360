import { useEffect, useState } from 'react'
import { supabase } from '../../lib/supabase'

interface Stats {
  students: number
  faculty: number
  books: number
  notifications: number
  marks: number
  payments: number
}

export default function AdminDashboard() {
  const [stats, setStats] = useState<Stats>({
    students: 0,
    faculty: 0,
    books: 0,
    notifications: 0,
    marks: 0,
    payments: 0,
  })
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    async function loadStats() {
      const [s, f, b, n, m, p] = await Promise.all([
        supabase.from('students').select('*', { count: 'exact', head: true }),
        supabase.from('faculty').select('*', { count: 'exact', head: true }),
        supabase.from('books').select('*', { count: 'exact', head: true }),
        supabase.from('notifications').select('*', { count: 'exact', head: true }),
        supabase.from('marks').select('*', { count: 'exact', head: true }),
        supabase.from('payments').select('*', { count: 'exact', head: true }),
      ])

      setStats({
        students: s.count || 0,
        faculty: f.count || 0,
        books: b.count || 0,
        notifications: n.count || 0,
        marks: m.count || 0,
        payments: p.count || 0,
      })
      setLoading(false)
    }
    loadStats()
  }, [])

  const cards = [
    { label: 'Total Students', value: stats.students, icon: '🎓' },
    { label: 'Total Faculty', value: stats.faculty, icon: '👨‍🏫' },
    { label: 'Library Books', value: stats.books, icon: '📚' },
    { label: 'Notifications', value: stats.notifications, icon: '🔔' },
    { label: 'Marks Records', value: stats.marks, icon: '📊' },
    { label: 'Payments', value: stats.payments, icon: '💰' },
  ]

  return (
    <div>
      <div className="welcome-banner">
        <h1>Admin Dashboard</h1>
        <p>Manage students, faculty, academics, and campus operations</p>
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
