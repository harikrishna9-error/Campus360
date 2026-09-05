export type Role = 'admin' | 'faculty' | 'student'

export interface Student {
  id: number
  user_id: string | null
  rollno: string
  password: string | null
  name: string
  branch: string | null
  year: string | null
  section: string | null
  phone: string | null
  email: string | null
  address: string | null
  dob: string | null
  bloodgroup: string | null
}

export interface Admin {
  id: number
  user_id: string | null
  username: string | null
  password: string | null
}

export interface Faculty {
  id: number
  user_id: string | null
  facultyid: string | null
  password: string | null
  name: string
  department: string | null
  phone: string | null
  email: string | null
}

export interface Attendance {
  id: number
  rollno: string
  branch: string
  year: string
  date: string
  period: number
  status: 'Present' | 'Absent'
}

export interface Mark {
  id: number
  rollno: string
  branch: string
  year: string
  semester: string
  exam: string
  python: number
  java: number
  dbms: number
  os: number
  cn: number
  total: number
  percentage: number
  grade: string | null
  result: string | null
}

export interface Fee {
  id: number
  rollno: string
  total_fee: number
  paid: number
  balance: number
  status: string
}

export interface LibraryRecord {
  id: number
  rollno: string
  book_name: string
  issue_date: string
  return_date: string
  status: string
}

export interface Timetable {
  id: number
  branch: string
  year: string
  day: string
  period1: string
  period2: string
  period3: string
  period4: string
  period5: string
  period6: string
}

export interface Result {
  id: number
  rollno: string
  semester: string
  sgpa: number
  cgpa: number
  result: string
}

export interface Backlog {
  id: number
  rollno: string
  subject: string
  status: string
}

export interface Exam {
  id: number
  exam_name: string
  exam_date: string
  branch: string
  year: string
}

export interface Hallticket {
  id: number
  rollno: string
  hallticket_no: string
  semester: string
}

export interface Payment {
  id: number
  rollno: string
  amount: number
  payment_date: string
  payment_mode: string
}

export interface Receipt {
  id: number
  receipt_no: string
  rollno: string
  amount: number
  receipt_date: string
}

export interface Notification {
  id: number
  title: string
  message: string
  date: string
}

export interface Book {
  id: number
  book_name: string
  author: string
  quantity: number
}

export interface UserProfile {
  role: Role
  id: number
  user_id: string
  name: string
  rollno?: string
  facultyid?: string
  username?: string
  branch?: string
  year?: string
  section?: string
  department?: string
  phone?: string
  email?: string
}
