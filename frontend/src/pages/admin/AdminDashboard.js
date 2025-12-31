import { useState } from 'react';
import { Card } from '../../components/common/Card';
import { Button } from '../../components/common/Button';
import { FormField } from '../../components/forms/FormField';
import { Toast } from '../../components/notifications/Toast';
import apiClient from '../../services/api/axiosConfig'; // Direct access for admin-specific endpoints

export const AdminDashboard = () => {
  const [message, setMessage] = useState('');
  const [toast, setToast] = useState(null);

  const handleBroadcast = async (e) => {
    e.preventDefault();
    try {
      // Assuming endpoint exists: POST /notifications/admin/broadcast
      await apiClient.post('/notifications/admin/broadcast', { message });
      setToast({ message: 'Broadcast sent successfully!', type: 'success' });
      setMessage('');
    } catch (error) {
      setToast({ message: 'Broadcast failed.', type: 'error' });
    }
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <h1 className="text-3xl font-bold text-gray-900 mb-8">
        System Administration
      </h1>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        <Card>
          <h2 className="text-xl font-semibold mb-4">System Broadcast</h2>
          <p className="text-gray-600 mb-4">
            Send a system-wide notification to all registered users.
          </p>
          <form onSubmit={handleBroadcast}>
            <FormField label="Message">
              <textarea
                className="w-full border rounded p-2"
                rows="4"
                value={message}
                onChange={(e) => setMessage(e.target.value)}
                required
              />
            </FormField>
            <Button type="submit" variant="primary">
              Send Broadcast
            </Button>
          </form>
        </Card>

        <Card>
          <h2 className="text-xl font-semibold mb-4">System Health</h2>
          <div className="space-y-2">
            <div className="flex justify-between p-2 bg-green-50 rounded">
              <span>Auth Service</span>
              <span className="text-green-600 font-bold">Online</span>
            </div>
            <div className="flex justify-between p-2 bg-green-50 rounded">
              <span>Job Service</span>
              <span className="text-green-600 font-bold">Online</span>
            </div>
            <div className="flex justify-between p-2 bg-green-50 rounded">
              <span>App Service</span>
              <span className="text-green-600 font-bold">Online</span>
            </div>
          </div>
        </Card>
      </div>
      {toast && <Toast {...toast} onClose={() => setToast(null)} />}
    </div>
  );
};
