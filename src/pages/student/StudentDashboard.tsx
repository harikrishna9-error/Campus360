import { useEffect, useState } from 'react'
import { supabase } from '../../lib/supabase'
import { useAuth } from '../../context/AuthContext'

interface StudentStats {
  attendancePct: number
  presentPeriods: number
  totalPeriods: number
  avgMarks: number
  feeStatus: string
  notifications: number
}

export default function StudentDashboard() {
  const { profile } = useAuth()
  const [stats, setStats] = useState<StudentStats>({
    attendancePct: 0,
    presentPeriods: 0,
    totalPeriods: 0,
    avgMarks: 0,
    feeStatus: 'N/A',
    notifications: 0,
  })
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    async function loadStats() {
      if (!profile?.rollno) {
        setLoading(false)
        return
      }
      const rollno = profile.rollno

      const { data: attRows } = await supabase
        .from('attendance')
        .select('status')
        .eq('rollno', rollno)

      const totalPeriods = attRows?.length || 0
      const presentPeriods = attRows?.filter((r) => r.status === 'Present').length || 0
      const attendancePct = totalPeriods > 0 ? Math.round((presentPeriods / totalPeriods) * 100 * 100) / 100 : 0

      const { data: marksRows } = await supabase
        .from('marks')
        .select('percentage')
        .eq('rollno', rollno)

      const avgMarks = marksRows && marksRows.length > 0
        ? Math.round((marksRows.reduce((sum, m) => sum + (m.percentage || 0), 0) / marksRows.length) * 100) / 100
        : 0

      const { data: feeRow } = await supabase
        .from('fees')
        .select('status')
        .eq('rollno', rollno)
        .maybeSingle()

      const { count: notifCount } = await supabase
        .from('notifications')
        .select('*', { count: 'exact', head: true })

      setStats({
        attendancePct,
        presentPeriods,
        totalPeriods,
        avgMarks,
        feeStatus: feeRow?.status || 'N/A',
        notifications: notifCount || 0,
      })
      setLoading(false)
    }
    loadStats()
  }, [profile])

  const cards = [
    { label: 'Attendance', value: `${stats.attendancePct}%`, icon: '✅' },
    { label: 'Average Marks', value: `${stats.avgMarks}%`, icon: '📊' },
    { label: 'Fee Status', value: stats.feeStatus, icon: '💳' },
    { label: 'Notifications', value: stats.notifications, icon: '🔔' },
  ]

  return (
    <div>
      <div className="welcome-banner">
        <h1>Welcome, {profile?.name}</h1>
        <p>{profile?.rollno} — {profile?.branch} {profile?.year} Year, Section {profile?.section}</p>
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
