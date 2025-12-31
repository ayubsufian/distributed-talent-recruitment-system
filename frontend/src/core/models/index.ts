// User & Auth Models
export interface User {
  id: string;
  email: string;
  role: 'Admin' | 'Recruiter' | 'Candidate';
  is_active: boolean;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
  user?: User; // Optional, depending on if backend returns user object on login
}

// Job Models
export interface Job {
  id: string;
  recruiter_id: string;
  title: string;
  description: string;
  location: string;
  salary_range?: string;
  status: 'Active' | 'Archived' | 'Closed' | 'Flagged';
  created_at: string;
}

// Application Models
export interface Application {
  id: string;
  job_id: string;
  candidate_id: string;
  status:
    | 'Pending'
    | 'Reviewed'
    | 'Shortlisted'
    | 'Accepted'
    | 'Rejected'
    | 'Withdrawn';
  resume_file_id: string;
  applied_at: string;
}

// Notification Models
export interface Notification {
  id: string;
  user_id: string;
  message: string;
  type: 'email' | 'system';
  read_status: boolean;
  created_at: string;
}
