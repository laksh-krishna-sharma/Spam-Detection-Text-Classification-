import React from 'react';
import { useNavigate } from 'react-router-dom';

const Home: React.FC = () => {
  const navigate = useNavigate();

  return (
    <div className="flex justify-center items-center min-h-screen bg-orange-50">
      <div className="bg-orange-200 p-6 rounded-lg shadow-md w-96">
        <h2 className="text-center text-2xl font-bold text-orange-600 mb-6">Check Your Message</h2>
        <div className="flex flex-col space-y-4">
          <button 
            className="bg-orange-600 text-white py-2 rounded-lg hover:bg-orange-700 transition duration-300"
            onClick={() => navigate('/signup')}
          >
            Sign Up
          </button>
          <button 
            className="bg-orange-600 text-white py-2 rounded-lg hover:bg-orange-700 transition duration-300"
            onClick={() => navigate('/signin')}
          >
            Sign In
          </button>
        </div>
      </div>
    </div>
  );
};

export default Home;
