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

export const API_ROUTES = {
  AUTH: '/auth', // Add trailing slash
  USERS: '/users', // Add trailing slash
  JOBS: '/jobs', // Add trailing slash
  APPLICATIONS: '/applications', // Add trailing slash
  NOTIFICATIONS: '/notifications', // Add trailing slash
  SYSTEM: '/system', // Add trailing slash
};
