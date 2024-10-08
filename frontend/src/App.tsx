import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from './components/Home';
import Signin from './components/Signin';
import Signup from './components/Signup';
import Message from './components/Message';

const App: React.FC = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/signup" element={<Signup />} />
        <Route path="/signin" element={<Signin />} />
        <Route path="/message" element={<Message />} />
      </Routes>
    </Router>
  );
};

export default App;

