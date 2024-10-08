import React, { useState } from 'react';

const Message: React.FC = () => {
  const [message, setMessage] = useState('');
  const [result, setResult] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const userId = 1; // Replace with the actual logged-in user's ID

  const handlePredict = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setResult(null);
    
    try {
      // Call your FastAPI backend here
      const response = await fetch('http://localhost:8000/predict', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text: message, user_id: userId }),
      });
      
      if (!response.ok) {
        throw new Error('Failed to predict');
      }

      const data = await response.json();
      setResult(data.prediction); // Assuming FastAPI returns { prediction: 'spam' or 'ham' }
    } catch (error) {
      console.error('Error:', error);
      setResult('Error predicting message');
    }
    
    setLoading(false);
  };

  return (
    <div className="flex justify-center items-center min-h-screen bg-orange-50">
      <div className="bg-orange-200 p-6 rounded-lg shadow-md w-96">
        <h2 className="text-center text-2xl font-bold text-orange-600 mb-6">Message Spam Detector</h2>
        <form onSubmit={handlePredict}>
          <div className="mb-4">
            <label htmlFor="message" className="block text-orange-600 mb-2">Enter your message</label>
            <textarea
              id="message"
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              required
              rows={4}
              className="w-full px-3 py-2 border border-orange-400 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500"
              placeholder="Type your message here..."
            />
          </div>
          <button
            type="submit"
            className="w-full bg-orange-600 text-white py-2 rounded-lg hover:bg-orange-700 transition duration-300"
            disabled={loading}
          >
            {loading ? 'Checking...' : 'Check Message'}
          </button>
        </form>

        {result && (
          <div className="mt-6 text-center">
            <p className={`text-xl font-bold ${result === 'spam' ? 'text-red-600' : 'text-green-600'}`}>
              The message is: {result === 'spam' ? 'Spam' : 'Ham'}
            </p>
          </div>
        )}
      </div>
    </div>
  );
};

export default Message;
