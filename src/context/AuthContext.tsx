import { createContext, useContext, useEffect, useState, ReactNode } from 'react'
import { Session, User } from '@supabase/supabase-js'
import { supabase } from '../lib/supabase'
import type { Role, UserProfile } from '../types'

interface AuthContextValue {
  session: Session | null
  user: User | null
  profile: UserProfile | null
  loading: boolean
  signIn: (email: string, password: string) => Promise<{ error: string | null }>
  signOut: () => Promise<void>
}

const AuthContext = createContext<AuthContextValue | undefined>(undefined)

export function AuthProvider({ children }: { children: ReactNode }) {
  const [session, setSession] = useState<Session | null>(null)
  const [profile, setProfile] = useState<UserProfile | null>(null)
  const [loading, setLoading] = useState(true)

  async function loadProfile(uid: string): Promise<UserProfile | null> {
    const { data: adminRow } = await supabase
      .from('admin')
      .select('*')
      .eq('user_id', uid)
      .maybeSingle()

    if (adminRow) {
      return {
        role: 'admin' as Role,
        id: adminRow.id,
        user_id: uid,
        name: adminRow.username || 'Administrator',
        username: adminRow.username,
      }
    }

    const { data: facultyRow } = await supabase
      .from('faculty')
      .select('*')
      .eq('user_id', uid)
      .maybeSingle()

    if (facultyRow) {
      return {
        role: 'faculty' as Role,
        id: facultyRow.id,
        user_id: uid,
        name: facultyRow.name,
        facultyid: facultyRow.facultyid,
        department: facultyRow.department,
        phone: facultyRow.phone,
        email: facultyRow.email,
      }
    }

    const { data: studentRow } = await supabase
      .from('students')
      .select('*')
      .eq('user_id', uid)
      .maybeSingle()

    if (studentRow) {
      return {
        role: 'student' as Role,
        id: studentRow.id,
        user_id: uid,
        name: studentRow.name,
        rollno: studentRow.rollno,
        branch: studentRow.branch,
        year: studentRow.year,
        section: studentRow.section,
        phone: studentRow.phone,
        email: studentRow.email,
      }
    }

    return null
  }

  useEffect(() => {
    supabase.auth.getSession().then(({ data: { session: s } }) => {
      setSession(s)
      if (s?.user) {
        loadProfile(s.user.id).then((p) => {
          setProfile(p)
          setLoading(false)
        })
      } else {
        setLoading(false)
      }
    })

    supabase.auth.onAuthStateChange((_event, s) => {
      setSession(s)
      if (s?.user) {
        (async () => {
          const p = await loadProfile(s.user.id)
          setProfile(p)
          setLoading(false)
        })()
      } else {
        setProfile(null)
        setLoading(false)
      }
    })
  }, [])

  async function signIn(email: string, password: string) {
    const { error } = await supabase.auth.signInWithPassword({ email, password })
    return { error: error?.message || null }
  }

  async function signOut() {
    await supabase.auth.signOut()
    setProfile(null)
    setSession(null)
  }

  return (
    <AuthContext.Provider value={{ session, user: session?.user ?? null, profile, loading, signIn, signOut }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const ctx = useContext(AuthContext)
  if (!ctx) throw new Error('useAuth must be used within AuthProvider')
  return ctx
}
