import { useState, useEffect } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import { supabase } from '../../lib/supabase'
import type { Student } from '../../types'

const BRANCHES = ['CSE', 'ECE', 'EEE', 'MECH', 'CIVIL']
const YEARS = ['1', '2', '3', '4']
const SECTIONS = ['A', 'B', 'C']

interface FormData {
  rollno: string
  name: string
  branch: string
  year: string
  section: string
  phone: string
  email: string
  address: string
  dob: string
  bloodgroup: string
}

const emptyForm: FormData = {
  rollno: '',
  name: '',
  branch: '',
  year: '',
  section: '',
  phone: '',
  email: '',
  address: '',
  dob: '',
  bloodgroup: '',
}

export default function StudentForm() {
  const { rollno } = useParams<{ rollno: string }>()
  const navigate = useNavigate()
  const isEdit = Boolean(rollno)

  const [form, setForm] = useState<FormData>(emptyForm)
  const [errors, setErrors] = useState<Partial<Record<keyof FormData, string>>>({})
  const [submitting, setSubmitting] = useState(false)
  const [serverError, setServerError] = useState('')

  useEffect(() => {
    if (!isEdit || !rollno) return
    async function loadStudent() {
      const { data, error: queryError } = await supabase
        .from('students')
        .select('*')
        .eq('rollno', rollno!)
        .maybeSingle()

      if (queryError || !data) {
        setServerError('Student not found')
        return
      }

      const s = data as Student
      setForm({
        rollno: s.rollno,
        name: s.name,
        branch: s.branch || '',
        year: s.year || '',
        section: s.section || '',
        phone: s.phone || '',
        email: s.email || '',
        address: s.address || '',
        dob: s.dob || '',
        bloodgroup: s.bloodgroup || '',
      })
    }
    loadStudent()
  }, [isEdit, rollno])

  function validate(): boolean {
    const e: Partial<Record<keyof FormData, string>> = {}

    if (!form.rollno.trim()) e.rollno = 'Roll number is required'
    if (!form.name.trim()) e.name = 'Name is required'
    if (!form.branch.trim()) e.branch = 'Branch is required'
    if (!form.year.trim()) e.year = 'Year is required'
    if (!form.section.trim()) e.section = 'Section is required'
    if (!form.email.trim()) {
      e.email = 'Email is required'
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.email)) {
      e.email = 'Invalid email format'
    }

    setErrors(e)
    return Object.keys(e).length === 0
  }

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    setServerError('')

    if (!validate()) return

    setSubmitting(true)

    if (isEdit && rollno) {
      const { error: updateError } = await supabase
        .from('students')
        .update({
          name: form.name,
          branch: form.branch,
          year: form.year,
          section: form.section,
          phone: form.phone || null,
          email: form.email,
          address: form.address || null,
          dob: form.dob || null,
          bloodgroup: form.bloodgroup || null,
        })
        .eq('rollno', rollno)

      setSubmitting(false)
      if (updateError) {
        setServerError(updateError.message)
      } else {
        navigate(`/students/${rollno}`)
      }
    } else {
      // Check for duplicate roll number
      const { data: existing } = await supabase
        .from('students')
        .select('rollno')
        .eq('rollno', form.rollno)
        .maybeSingle()

      if (existing) {
        setErrors({ rollno: 'This roll number already exists' })
        setSubmitting(false)
        return
      }

      const { error: insertError } = await supabase.from('students').insert({
        rollno: form.rollno,
        name: form.name,
        branch: form.branch,
        year: form.year,
        section: form.section,
        phone: form.phone || null,
        email: form.email,
        address: form.address || null,
        dob: form.dob || null,
        bloodgroup: form.bloodgroup || null,
      })

      setSubmitting(false)
      if (insertError) {
        setServerError(insertError.message)
      } else {
        navigate('/students')
      }
    }
  }

  function updateField(field: keyof FormData, value: string) {
    setForm({ ...form, [field]: value })
    if (errors[field]) setErrors({ ...errors, [field]: undefined })
  }

  return (
    <div>
      <div className="page-header">
        <h2>{isEdit ? 'Edit Student' : 'Add Student'}</h2>
        <button className="btn btn-outline" onClick={() => navigate('/students')}>
          ← Back
        </button>
      </div>

      {serverError && <div className="alert alert-danger">{serverError}</div>}

      <div className="form-card">
        <form onSubmit={handleSubmit}>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px' }}>
            <div className="form-group">
              <label>Roll Number *</label>
              <input
                type="text"
                value={form.rollno}
                onChange={(e) => updateField('rollno', e.target.value)}
                disabled={isEdit}
                style={isEdit ? { opacity: 0.6, cursor: 'not-allowed' } : {}}
              />
              {errors.rollno && <span style={{ color: 'var(--danger)', fontSize: '13px' }}>{errors.rollno}</span>}
            </div>

            <div className="form-group">
              <label>Full Name *</label>
              <input
                type="text"
                value={form.name}
                onChange={(e) => updateField('name', e.target.value)}
              />
              {errors.name && <span style={{ color: 'var(--danger)', fontSize: '13px' }}>{errors.name}</span>}
            </div>

            <div className="form-group">
              <label>Branch *</label>
              <select value={form.branch} onChange={(e) => updateField('branch', e.target.value)}>
                <option value="">Select Branch</option>
                {BRANCHES.map((b) => (
                  <option key={b} value={b}>{b}</option>
                ))}
              </select>
              {errors.branch && <span style={{ color: 'var(--danger)', fontSize: '13px' }}>{errors.branch}</span>}
            </div>

            <div className="form-group">
              <label>Year *</label>
              <select value={form.year} onChange={(e) => updateField('year', e.target.value)}>
                <option value="">Select Year</option>
                {YEARS.map((y) => (
                  <option key={y} value={y}>{y}</option>
                ))}
              </select>
              {errors.year && <span style={{ color: 'var(--danger)', fontSize: '13px' }}>{errors.year}</span>}
            </div>

            <div className="form-group">
              <label>Section *</label>
              <select value={form.section} onChange={(e) => updateField('section', e.target.value)}>
                <option value="">Select Section</option>
                {SECTIONS.map((s) => (
                  <option key={s} value={s}>{s}</option>
                ))}
              </select>
              {errors.section && <span style={{ color: 'var(--danger)', fontSize: '13px' }}>{errors.section}</span>}
            </div>

            <div className="form-group">
              <label>Phone</label>
              <input
                type="text"
                value={form.phone}
                onChange={(e) => updateField('phone', e.target.value)}
              />
            </div>

            <div className="form-group">
              <label>Email *</label>
              <input
                type="email"
                value={form.email}
                onChange={(e) => updateField('email', e.target.value)}
              />
              {errors.email && <span style={{ color: 'var(--danger)', fontSize: '13px' }}>{errors.email}</span>}
            </div>

            <div className="form-group">
              <label>Date of Birth</label>
              <input
                type="date"
                value={form.dob}
                onChange={(e) => updateField('dob', e.target.value)}
              />
            </div>

            <div className="form-group">
              <label>Blood Group</label>
              <input
                type="text"
                value={form.bloodgroup}
                onChange={(e) => updateField('bloodgroup', e.target.value)}
                placeholder="e.g. O+"
              />
            </div>

            <div className="form-group" style={{ gridColumn: '1 / -1' }}>
              <label>Address</label>
              <textarea
                value={form.address}
                onChange={(e) => updateField('address', e.target.value)}
                style={{ minHeight: '80px' }}
              />
            </div>
          </div>

          <div style={{ display: 'flex', gap: '12px', marginTop: '24px' }}>
            <button type="submit" className="btn btn-success" disabled={submitting}>
              {submitting ? 'Saving...' : isEdit ? 'Update Student' : 'Add Student'}
            </button>
            <button type="button" className="btn btn-outline" onClick={() => navigate('/students')}>
              Cancel
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}
