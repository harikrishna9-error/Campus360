import { useEffect, useState, useCallback } from 'react'
import { useNavigate } from 'react-router-dom'
import { supabase } from '../../lib/supabase'
import { useAuth } from '../../context/AuthContext'
import type { Student } from '../../types'

const BRANCHES = ['CSE', 'ECE', 'EEE', 'MECH', 'CIVIL']
const YEARS = ['1', '2', '3', '4']
const SECTIONS = ['A', 'B', 'C']

export default function StudentsList() {
  const { profile } = useAuth()
  const navigate = useNavigate()
  const isAdmin = profile?.role === 'admin'

  const [students, setStudents] = useState<Student[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  const [search, setSearch] = useState('')
  const [branchFilter, setBranchFilter] = useState('')
  const [yearFilter, setYearFilter] = useState('')
  const [sectionFilter, setSectionFilter] = useState('')

  const [deleteTarget, setDeleteTarget] = useState<Student | null>(null)
  const [deleting, setDeleting] = useState(false)
  const [toast, setToast] = useState<{ type: 'success' | 'error'; msg: string } | null>(null)

  const showToast = (type: 'success' | 'error', msg: string) => {
    setToast({ type, msg })
    setTimeout(() => setToast(null), 4000)
  }

  const loadStudents = useCallback(async () => {
    setLoading(true)
    setError('')

    let query = supabase.from('students').select('*').order('rollno')

    if (search) {
      query = query.or(`rollno.ilike.%${search}%,name.ilike.%${search}%`)
    }
    if (branchFilter) query = query.eq('branch', branchFilter)
    if (yearFilter) query = query.eq('year', yearFilter)
    if (sectionFilter) query = query.eq('section', sectionFilter)

    const { data, error: queryError } = await query

    if (queryError) {
      setError(queryError.message)
    } else {
      setStudents(data || [])
    }
    setLoading(false)
  }, [search, branchFilter, yearFilter, sectionFilter])

  useEffect(() => {
    loadStudents()
  }, [loadStudents])

  function clearFilters() {
    setSearch('')
    setBranchFilter('')
    setYearFilter('')
    setSectionFilter('')
  }

  async function confirmDelete() {
    if (!deleteTarget) return
    setDeleting(true)
    const { error: deleteError } = await supabase
      .from('students')
      .delete()
      .eq('rollno', deleteTarget.rollno)

    setDeleting(false)
    if (deleteError) {
      showToast('error', `Failed to delete: ${deleteError.message}`)
    } else {
      showToast('success', `Student ${deleteTarget.rollno} deleted successfully`)
      setDeleteTarget(null)
      loadStudents()
    }
  }

  return (
    <div>
      {toast && (
        <div className={`alert alert-${toast.type === 'success' ? 'success' : 'danger'}`}>
          {toast.msg}
        </div>
      )}

      <div className="page-header">
        <h2>Students Management</h2>
        {isAdmin && (
          <button className="btn btn-success" onClick={() => navigate('/students/add')}>
            ＋ Add Student
          </button>
        )}
      </div>

      {/* Filters */}
      <div className="form-card" style={{ marginBottom: '20px' }}>
        <div style={{ display: 'flex', flexWrap: 'wrap', gap: '16px', alignItems: 'flex-end' }}>
          <div className="form-group" style={{ flex: '1 1 200px', marginBottom: 0 }}>
            <label>Search</label>
            <input
              type="text"
              placeholder="Search by Roll No or Name"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
            />
          </div>
          <div className="form-group" style={{ flex: '1 1 140px', marginBottom: 0 }}>
            <label>Branch</label>
            <select value={branchFilter} onChange={(e) => setBranchFilter(e.target.value)}>
              <option value="">All Branches</option>
              {BRANCHES.map((b) => (
                <option key={b} value={b}>{b}</option>
              ))}
            </select>
          </div>
          <div className="form-group" style={{ flex: '1 1 120px', marginBottom: 0 }}>
            <label>Year</label>
            <select value={yearFilter} onChange={(e) => setYearFilter(e.target.value)}>
              <option value="">All Years</option>
              {YEARS.map((y) => (
                <option key={y} value={y}>{y}</option>
              ))}
            </select>
          </div>
          <div className="form-group" style={{ flex: '1 1 120px', marginBottom: 0 }}>
            <label>Section</label>
            <select value={sectionFilter} onChange={(e) => setSectionFilter(e.target.value)}>
              <option value="">All Sections</option>
              {SECTIONS.map((s) => (
                <option key={s} value={s}>{s}</option>
              ))}
            </select>
          </div>
          <button className="btn btn-outline" onClick={clearFilters}>
            Clear Filters
          </button>
        </div>
      </div>

      {/* Error */}
      {error && <div className="alert alert-danger">{error}</div>}

      {/* Loading */}
      {loading ? (
        <div style={{ textAlign: 'center', padding: '60px' }}>
          <div className="spinner" style={{ margin: '0 auto' }} />
          <p style={{ marginTop: '16px', color: 'var(--gray-500)' }}>Loading students...</p>
        </div>
      ) : students.length === 0 ? (
        /* Empty state */
        <div className="form-card" style={{ textAlign: 'center', padding: '60px' }}>
          <div style={{ fontSize: '48px', marginBottom: '16px' }}>🎓</div>
          <h3 style={{ color: 'var(--gray-600)', marginBottom: '8px' }}>No Students Found</h3>
          <p style={{ color: 'var(--gray-500)' }}>
            No students match the current filters. Try adjusting your search or filters.
          </p>
        </div>
      ) : (
        /* Table */
        <div style={{ overflowX: 'auto' }}>
          <table className="data-table">
            <thead>
              <tr>
                <th>Roll No</th>
                <th>Name</th>
                <th>Branch</th>
                <th>Year</th>
                <th>Section</th>
                <th>Phone</th>
                <th>Email</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {students.map((student) => (
                <tr key={student.id}>
                  <td style={{ fontWeight: 600 }}>{student.rollno}</td>
                  <td>{student.name}</td>
                  <td>{student.branch || '-'}</td>
                  <td>{student.year || '-'}</td>
                  <td>{student.section || '-'}</td>
                  <td>{student.phone || '-'}</td>
                  <td style={{ fontSize: '13px' }}>{student.email || '-'}</td>
                  <td>
                    <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap' }}>
                      <button
                        className="btn btn-outline"
                        style={{ padding: '6px 14px', fontSize: '13px' }}
                        onClick={() => navigate(`/students/${student.rollno}`)}
                      >
                        View
                      </button>
                      {isAdmin && (
                        <>
                          <button
                            className="btn btn-warning"
                            style={{ padding: '6px 14px', fontSize: '13px' }}
                            onClick={() => navigate(`/students/${student.rollno}/edit`)}
                          >
                            Edit
                          </button>
                          <button
                            className="btn btn-danger"
                            style={{ padding: '6px 14px', fontSize: '13px' }}
                            onClick={() => setDeleteTarget(student)}
                          >
                            Delete
                          </button>
                        </>
                      )}
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {/* Delete Confirmation Modal */}
      {deleteTarget && (
        <div
          style={{
            position: 'fixed',
            inset: 0,
            background: 'rgba(0,0,0,0.5)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            zIndex: 200,
          }}
          onClick={() => !deleting && setDeleteTarget(null)}
        >
          <div
            className="form-card"
            style={{ maxWidth: '440px', width: '90%' }}
            onClick={(e) => e.stopPropagation()}
          >
            <h2 style={{ color: 'var(--danger)' }}>Delete Student</h2>
            <p style={{ fontSize: '16px', color: 'var(--gray-600)', marginTop: '12px' }}>
              Are you sure you want to delete{' '}
              <strong style={{ color: 'var(--dark)' }}>
                {deleteTarget.name} ({deleteTarget.rollno})
              </strong>
              ?
            </p>
            <p style={{ fontSize: '14px', color: 'var(--gray-500)', marginTop: '8px' }}>
              This action cannot be undone.
            </p>
            <div style={{ display: 'flex', gap: '12px', marginTop: '28px', justifyContent: 'flex-end' }}>
              <button
                className="btn btn-outline"
                onClick={() => setDeleteTarget(null)}
                disabled={deleting}
              >
                Cancel
              </button>
              <button
                className="btn btn-danger"
                onClick={confirmDelete}
                disabled={deleting}
              >
                {deleting ? 'Deleting...' : 'Delete'}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
