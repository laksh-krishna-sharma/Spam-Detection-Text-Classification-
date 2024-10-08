import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const Signup: React.FC = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();

  const handleSignup = async (e: React.FormEvent) => {
    e.preventDefault();

    try {
        const response = await fetch('http://localhost:8000/signup/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username, password }),
        });

        if (response.ok) {
            alert('Signup successful! Please sign in.');
            navigate('/signin'); // Redirect to sign-in page after signup
        } else {
            const errorData = await response.json();
            alert(`Signup failed: ${errorData.detail || 'An unknown error occurred'}`);
        }
    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred during signup');
    }
};


  return (
    <div className="flex justify-center items-center min-h-screen bg-orange-50">
      <div className="bg-orange-200 p-6 rounded-lg shadow-md w-96">
        <h2 className="text-center text-2xl font-bold text-orange-600 mb-6">Sign Up</h2>
        <form onSubmit={handleSignup}>
          <div className="mb-4">
            <label htmlFor="username" className="block text-orange-600 mb-2">Username</label>
            <input
              type="text"
              id="username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
              className="w-full px-3 py-2 border border-orange-400 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500"
            />
          </div>
          <div className="mb-6">
            <label htmlFor="password" className="block text-orange-600 mb-2">Password</label>
            <input
              type="password"
              id="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              className="w-full px-3 py-2 border border-orange-400 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500"
            />
          </div>
          <button
            type="submit"
            className="w-full bg-orange-600 text-white py-2 rounded-lg hover:bg-orange-700 transition duration-300"
          >
            Sign Up
          </button>
        </form>
      </div>
    </div>
  );
};

export default Signup;
