export const ROLES = {
  ADMIN: 'Admin',
  RECRUITER: 'Recruiter',
  CANDIDATE: 'Candidate',
};

export const APP_STATUS = {
  PENDING: 'Pending',
  REVIEWED: 'Reviewed',
  SHORTLISTED: 'Shortlisted',
  ACCEPTED: 'Accepted',
  REJECTED: 'Rejected',
  WITHDRAWN: 'Withdrawn',
};

export const JOB_STATUS = {
  ACTIVE: 'Active',
  ARCHIVED: 'Archived',
  CLOSED: 'Closed',
};

// Matches Nginx Gateway Routes
export const API_ROUTES = {
  AUTH: '/auth',
  USERS: '/users',
  JOBS: '/jobs',
  APPLICATIONS: '/applications',
  NOTIFICATIONS: '/notifications',
  SYSTEM: '/system', // <--- Add this for the failed events API
};
