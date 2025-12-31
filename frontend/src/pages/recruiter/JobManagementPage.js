import React, { useState } from 'react';
import { useJobs } from '../../hooks/useJobs';
import { JobService } from '../../services/api/job.service';
import { Card } from '../../components/common/Card';
import { Button } from '../../components/common/Button';
import { Badge } from '../../components/common/Badge';
import { Input } from '../../components/common/Input';
import { FormField } from '../../components/forms/FormField';
import { Toast } from '../../components/notifications/Toast';

export const JobManagementPage = () => {
  const { jobs, refresh } = useJobs(); // In real app, filter by recruiter ID
  const [showCreate, setShowCreate] = useState(false);
  const [newJob, setNewJob] = useState({
    title: '',
    description: '',
    location: '',
    salary_range: '',
  });
  const [toast, setToast] = useState(null);

  const handleCreate = async (e) => {
    e.preventDefault();
    try {
      await JobService.create(newJob);
      setToast({ message: 'Job posted successfully!', type: 'success' });
      setShowCreate(false);
      setNewJob({ title: '', description: '', location: '', salary_range: '' });
      refresh();
    } catch (error) {
      setToast({ message: 'Failed to post job.', type: 'error' });
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm('Are you sure?')) return;
    try {
      await JobService.delete(id);
      refresh();
      setToast({ message: 'Job deleted.', type: 'info' });
    } catch (error) {
      setToast({ message: 'Delete failed.', type: 'error' });
    }
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold text-gray-900">Job Management</h1>
        <Button onClick={() => setShowCreate(!showCreate)}>
          {showCreate ? 'Cancel' : 'Post New Job'}
        </Button>
      </div>

      {showCreate && (
        <Card className="mb-8 animate-fade-in">
          <h3 className="text-lg font-medium mb-4">Create Job Posting</h3>
          <form onSubmit={handleCreate} className="space-y-4">
            <FormField label="Job Title">
              <Input
                value={newJob.title}
                onChange={(e) =>
                  setNewJob({ ...newJob, title: e.target.value })
                }
                required
              />
            </FormField>
            <FormField label="Description">
              <textarea
                className="w-full border rounded p-2"
                rows="3"
                value={newJob.description}
                onChange={(e) =>
                  setNewJob({ ...newJob, description: e.target.value })
                }
                required
              />
            </FormField>
            <div className="grid grid-cols-2 gap-4">
              <FormField label="Location">
                <Input
                  value={newJob.location}
                  onChange={(e) =>
                    setNewJob({ ...newJob, location: e.target.value })
                  }
                  required
                />
              </FormField>
              <FormField label="Salary Range">
                <Input
                  value={newJob.salary_range}
                  onChange={(e) =>
                    setNewJob({ ...newJob, salary_range: e.target.value })
                  }
                />
              </FormField>
            </div>
            <Button type="submit">Publish Job</Button>
          </form>
        </Card>
      )}

      <div className="grid gap-4">
        {jobs.map((job) => (
          <Card key={job.id} className="flex justify-between items-center">
            <div>
              <h3 className="font-bold text-lg">{job.title}</h3>
              <div className="flex gap-2 mt-1">
                <Badge>{job.status}</Badge>
                <span className="text-sm text-gray-500">{job.location}</span>
              </div>
            </div>
            <div className="flex gap-2">
              {/* Link to Applicant Review Page (Placeholder route) */}
              <Button
                variant="outline"
                onClick={() =>
                  alert('Navigate to /jobs/' + job.id + '/applications')
                }
              >
                View Applicants
              </Button>
              <Button variant="danger" onClick={() => handleDelete(job.id)}>
                Delete
              </Button>
            </div>
          </Card>
        ))}
      </div>
      {toast && <Toast {...toast} onClose={() => setToast(null)} />}
    </div>
  );
};
