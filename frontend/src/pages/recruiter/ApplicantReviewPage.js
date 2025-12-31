import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { AppService } from '../../services/api/app.service';
import { JobService } from '../../services/api/job.service';
import { Card } from '../../components/common/Card';
import { Button } from '../../components/common/Button';
import { Badge } from '../../components/common/Badge';
import { Spinner } from '../../components/common/Spinner';
import { Toast } from '../../components/notifications/Toast';
import { APP_STATUS } from '../../core/constants';
import apiClient from '../../services/api/axiosConfig'; // Direct access for specific queries

export const ApplicantReviewPage = () => {
  const { jobId } = useParams();
  const navigate = useNavigate();

  const [job, setJob] = useState(null);
  const [applications, setApplications] = useState([]);
  const [loading, setLoading] = useState(true);
  const [downloadingId, setDownloadingId] = useState(null); // Track which resume is downloading
  const [toast, setToast] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        // 1. Fetch Job Details for context
        const jobData = await JobService.getById(jobId);
        setJob(jobData);

        // 2. Fetch Applications for this job
        // Note: Assuming backend endpoint GET /applications?job_id={id} exists
        // If not, this would need to be added to the App Service backend
        const appsResponse = await apiClient.get(`/applications`, {
          params: { job_id: jobId },
        });
        setApplications(appsResponse.data);
      } catch (error) {
        console.error('Failed to load data', error);
        setToast({ message: 'Failed to load applicants.', type: 'error' });
      } finally {
        setLoading(false);
      }
    };

    if (jobId) fetchData();
  }, [jobId]);

  const handleStatusChange = async (appId, newStatus) => {
    try {
      // Optimistic Update
      setApplications((prev) =>
        prev.map((app) =>
          app.id === appId ? { ...app, status: newStatus } : app
        )
      );

      // API Call: PATCH /applications/{id}
      await apiClient.patch(`/applications/${appId}`, { status: newStatus });

      setToast({ message: `Status updated to ${newStatus}`, type: 'success' });
    } catch (error) {
      // Revert on failure
      setToast({ message: 'Failed to update status.', type: 'error' });
      // In a real app, you'd re-fetch data here to revert UI
    }
  };

  const handleDownloadResume = async (appId, candidateId) => {
    setDownloadingId(appId);
    try {
      // Fetch the blob
      const blob = await AppService.getResume(appId);

      // Create a temporary link to trigger download
      const url = window.URL.createObjectURL(new Blob([blob]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `resume_${candidateId}.pdf`); // Filename
      document.body.appendChild(link);
      link.click();
      link.parentNode.removeChild(link);
    } catch (error) {
      setToast({ message: 'Failed to download resume.', type: 'error' });
    } finally {
      setDownloadingId(null);
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case APP_STATUS.ACCEPTED:
        return 'success';
      case APP_STATUS.REJECTED:
        return 'danger';
      case APP_STATUS.SHORTLISTED:
        return 'info';
      case APP_STATUS.PENDING:
        return 'warning';
      default:
        return 'gray';
    }
  };

  if (loading)
    return (
      <div className="flex justify-center py-12">
        <Spinner size="lg" />
      </div>
    );

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="flex items-center justify-between mb-6">
        <div>
          <Button
            variant="outline"
            onClick={() => navigate('/recruiter/dashboard')}
            className="mb-2 text-sm"
          >
            ← Back to Dashboard
          </Button>
          <h1 className="text-2xl font-bold text-gray-900">
            Applicants for: <span className="text-blue-600">{job?.title}</span>
          </h1>
        </div>
        <div className="text-gray-500">
          Total Applicants:{' '}
          <span className="font-bold text-gray-900">{applications.length}</span>
        </div>
      </div>

      <Card className="overflow-hidden">
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Candidate ID
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Applied Date
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Resume
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Current Status
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Actions
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {applications.map((app) => (
                <tr key={app.id}>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900 font-mono">
                    {app.candidate_id.substring(0, 8)}...
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {new Date(app.applied_at).toLocaleDateString()}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <Button
                      variant="outline"
                      size="sm"
                      className="text-xs py-1"
                      onClick={() =>
                        handleDownloadResume(app.id, app.candidate_id)
                      }
                      isLoading={downloadingId === app.id}
                    >
                      Download PDF
                    </Button>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <Badge type={getStatusColor(app.status)}>
                      {app.status}
                    </Badge>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm">
                    <select
                      value={app.status}
                      onChange={(e) =>
                        handleStatusChange(app.id, e.target.value)
                      }
                      className="block w-full pl-3 pr-10 py-1 text-base border-gray-300 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm rounded-md border"
                    >
                      {Object.values(APP_STATUS).map((status) => (
                        <option key={status} value={status}>
                          {status}
                        </option>
                      ))}
                    </select>
                  </td>
                </tr>
              ))}
              {applications.length === 0 && (
                <tr>
                  <td
                    colSpan="5"
                    className="px-6 py-12 text-center text-gray-500"
                  >
                    No applications received yet.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </Card>

      {toast && <Toast {...toast} onClose={() => setToast(null)} />}
    </div>
  );
};
