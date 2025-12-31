import React, { useState } from 'react';
import { useJobs } from '../../hooks/useJobs';
import { AppService } from '../../services/api/app.service';
import { Card } from '../../components/common/Card';
import { Button } from '../../components/common/Button';
import { Input } from '../../components/common/Input';
import { Badge } from '../../components/common/Badge';
import { Spinner } from '../../components/common/Spinner';
import { FileUpload } from '../../components/forms/FileUpload';
import { Toast } from '../../components/notifications/Toast';

export const JobSearchPage = () => {
  const { jobs, loading, searchJobs } = useJobs();
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedJob, setSelectedJob] = useState(null); // For Apply Modal
  const [toast, setToast] = useState(null);

  const handleSearch = (e) => {
    e.preventDefault();
    searchJobs(searchTerm);
  };

  const handleApply = async (file) => {
    try {
      await AppService.submit(selectedJob.id, file);
      setToast({
        message: 'Application submitted successfully!',
        type: 'success',
      });
      setSelectedJob(null);
    } catch (error) {
      setToast({ message: 'Failed to submit application.', type: 'error' });
    }
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-4">
          Find your next job
        </h1>
        <form onSubmit={handleSearch} className="flex gap-4">
          <Input
            placeholder="Search by title or description..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="flex-1"
          />
          <Button type="submit">Search</Button>
        </form>
      </div>

      {loading ? (
        <div className="flex justify-center py-12">
          <Spinner size="lg" />
        </div>
      ) : (
        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
          {jobs.map((job) => (
            <Card
              key={job.id}
              className="flex flex-col justify-between h-full hover:shadow-lg transition-shadow"
            >
              <div>
                <div className="flex justify-between items-start">
                  <h3 className="text-xl font-semibold text-gray-900">
                    {job.title}
                  </h3>
                  <Badge type="info">{job.location}</Badge>
                </div>
                <p className="mt-2 text-gray-600 line-clamp-3">
                  {job.description}
                </p>
                {job.salary_range && (
                  <p className="mt-2 text-sm font-medium text-gray-500">
                    Salary: {job.salary_range}
                  </p>
                )}
              </div>
              <div className="mt-4 pt-4 border-t border-gray-100">
                <Button
                  variant="primary"
                  className="w-full"
                  onClick={() => setSelectedJob(job)}
                >
                  Apply Now
                </Button>
              </div>
            </Card>
          ))}
        </div>
      )}

      {/* Simple Apply Modal Overlay */}
      {selectedJob && (
        <div className="fixed inset-0 bg-gray-600 bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-lg max-w-md w-full p-6">
            <h2 className="text-xl font-bold mb-4">
              Apply for {selectedJob.title}
            </h2>
            <p className="text-gray-600 mb-4">
              Please upload your resume (PDF) to proceed.
            </p>

            <FileUpload onFileSelect={handleApply} />

            <div className="mt-4 flex justify-end">
              <Button variant="secondary" onClick={() => setSelectedJob(null)}>
                Cancel
              </Button>
            </div>
          </div>
        </div>
      )}

      {toast && <Toast {...toast} onClose={() => setToast(null)} />}
    </div>
  );
};
