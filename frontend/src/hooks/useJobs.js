import { useState, useEffect, useCallback } from 'react';
import { JobService } from '../services/api/job.service';

export const useJobs = () => {
  const [jobs, setJobs] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Search & Pagination State
  const [query, setQuery] = useState('');
  const [page, setPage] = useState(1);
  const limit = 10;

  const fetchJobs = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const offset = (page - 1) * limit;
      const params = { limit, offset };
      if (query) params.q = query;

      const data = await JobService.getAll(params);
      setJobs(data);
    } catch (err) {
      setError(err.message || 'Failed to load jobs');
    } finally {
      setLoading(false);
    }
  }, [query, page]);

  // Initial fetch and re-fetch on dependency change
  useEffect(() => {
    fetchJobs();
  }, [fetchJobs]);

  const searchJobs = (searchTerm) => {
    setQuery(searchTerm);
    setPage(1); // Reset to first page on new search
  };

  return {
    jobs,
    loading,
    error,
    page,
    setPage,
    searchJobs,
    refresh: fetchJobs,
  };
};
