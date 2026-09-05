import { useEffect, useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { supabase } from '../../lib/supabase'
import { useAuth } from '../../context/AuthContext'
import type { Student } from '../../types'

export default function StudentDetails() {
  const { rollno } = useParams<{ rollno: string }>()
  const navigate = useNavigate()
  const { profile } = useAuth()
  const isAdmin = profile?.role === 'admin'

  const [student, setStudent] = useState<Student | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    async function loadStudent() {
      if (!rollno) return
      const { data, error: queryError } = await supabase
        .from('students')
        .select('*')
        .eq('rollno', rollno)
        .maybeSingle()

      if (queryError) {
        setError(queryError.message)
      } else if (!data) {
        setError('Student not found')
      } else {
        setStudent(data)
      }
      setLoading(false)
    }
    loadStudent()
  }, [rollno])

  if (loading) {
    return (
      <div style={{ textAlign: 'center', padding: '60px' }}>
        <div className="spinner" style={{ margin: '0 auto' }} />
      </div>
    )
  }

  if (error || !student) {
    return (
      <div>
        <div className="alert alert-danger">{error || 'Student not found'}</div>
        <button className="btn" onClick={() => navigate('/students')}>Back to Students</button>
      </div>
    )
  }

  const infoRows: { label: string; value: string | null }[] = [
    { label: 'Roll Number', value: student.rollno },
    { label: 'Name', value: student.name },
    { label: 'Branch', value: student.branch },
    { label: 'Year', value: student.year },
    { label: 'Section', value: student.section },
    { label: 'Phone', value: student.phone },
    { label: 'Email', value: student.email },
    { label: 'Address', value: student.address },
    { label: 'Date of Birth', value: student.dob },
    { label: 'Blood Group', value: student.bloodgroup },
  ]

  return (
    <div>
      <div className="page-header">
        <h2>Student Details</h2>
        <button className="btn btn-outline" onClick={() => navigate('/students')}>
          ← Back to Students
        </button>
      </div>

      <div className="profile-card">
        <h2>{student.name}</h2>
        {infoRows.map((row) => (
          <div className="info-row" key={row.label}>
            <div className="info-label">{row.label}</div>
            <div className="info-value">{row.value || '-'}</div>
          </div>
        ))}

        {isAdmin && (
          <div style={{ marginTop: '28px', display: 'flex', gap: '12px' }}>
            <button
              className="btn btn-warning"
              onClick={() => navigate(`/students/${student.rollno}/edit`)}
            >
              Edit Student
            </button>
            <button className="btn" onClick={() => navigate('/students')}>
              Back
            </button>
          </div>
        )}
      </div>
    </div>
  )
}
