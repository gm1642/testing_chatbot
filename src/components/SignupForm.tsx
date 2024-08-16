'use client';
import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import axios from 'axios';

const SignupForm: React.FC = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [showPassword, setShowPassword]= useState(false);
  const [error, setError] = useState('');
  const router = useRouter();

  const togglePasswordVisibilty = () =>{
    setShowPassword(!showPassword);
  };

  const handleSignup = async (event: React.FormEvent) => {
    event.preventDefault();
    setError('');

    if (password !== confirmPassword) {
      setError('Passwords do not match');
      return;
    }

    if (!validatePassword(password)) {
      return;
    }

    try {
      await axios.post('/api/signup', { email, password });
      router.push('/dashboard');
    } catch (error) {
      if (axios.isAxiosError(error) && error.response?.status === 409) {
        alert('User already exists');
        router.push('/login');
      } else {
        alert('Signup failed');
      }
    }
  };

  const validatePassword = (password: string) => {
    if (password.length < 8) {
      setError('Password must be at least 8 characters long.');
      return false;
    } else if (!/[A-Z]/.test(password)) {
      setError('Password must contain at least one uppercase letter.');
      return false;
    } else if (!/[a-z]/.test(password)) {
      setError('Password must contain at least one lowercase letter.');
      return false;
    } else if (!/[0-9]/.test(password)) {
      setError('Password must contain at least one number.');
      return false;
    } else if (!/[!@#$%^&*]/.test(password)) {
      setError('Password must contain at least one special character.');
      return false;
    }
    return true;
  };

  return (
    <form onSubmit={handleSignup} className="max-w-md mx-auto p-4 bg-customblue text-customwhite">
      <h2 className="text-center mb-4 text-2xl text-bold">Create your account</h2>
      <div className="mb-4">
        <div className="relative">
          <div className="absolute inset-y-0 left-0 flex items-center pl-5 pointer-events-none">
            <img src="/Vector (1).svg" alt="Icon" className="h-4 w-5" />
          </div>
          <input
            type="email"
            id="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="w-[330px] h-[50px] pl-14 bg-white25 text-fieldwhite px-3 py-2 rounded-lg focus:outline-none focus:ring-2 focus:ring-customlightblue font-montserrat"
            placeholder="Email"
            required
          />
        </div>
      </div>
      <div className="mb-4">
        <div className="relative">
          <div className="absolute inset-y-0 left-0 flex items-center pl-5 pointer-events-none">
            <img src="/Vector.svg" alt="Icon" className="h-4 w-5" />
          </div>
          <input
            type={showPassword ? 'text' : 'password'}
            id="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className={`w-[330px] h-[50px] pl-14 bg-white25 text-fieldwhite px-3 py-2 rounded-lg focus:outline-none focus:ring-2 ${error ? 'focus:ring-red-500' : 'focus:ring-customlightblue'} font-montserrat`}
            placeholder="Create your password"
            required
          />
                <div className="absolute inset-y-0 right-0 flex items-center pr-5">
        <button
          type="button"
          onClick={togglePasswordVisibilty}
          className="focus:outline-none"
        >
          {showPassword ? (
            <img src="/eye-open.svg" alt="Show Password" className="h-4 w-5 " />
          ) : (
            <img src="/eye-closed.svg" alt="Hide Password" className="h-4 w-5 " />
          )}
        </button>
        
      </div>
        </div>
      </div>
      <div className="mb-6">
        <div className="relative">
          <div className="absolute inset-y-0 left-0 flex items-center pl-5 pointer-events-none">
            <img src="/Vector.svg" alt="Icon" className="h-4 w-5" />
          </div>
          <input
            type={showPassword ? 'text' : 'password'}
            id="confirm-password"
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
            className={`w-[330px] h-[50px] pl-14 bg-white25 text-fieldwhite px-3 py-2 rounded-lg focus:outline-none focus:ring-2 ${error ? 'focus:ring-red-500' : 'focus:ring-customlightblue'} font-montserrat`}
            placeholder="Confirm Password"
            required
          />
           <div className="absolute inset-y-0 right-0 flex items-center pr-5">
           <button
          type="button"
          onClick={togglePasswordVisibilty}
          className="focus:outline-none"
        >
          {showPassword ? (
            <img src="/eye-open.svg" alt="Show Password" className="h-4 w-5 " />
          ) : (
            <img src="/eye-closed.svg" alt="Hide Password" className="h-4 w-5 " />
          )}
        </button>
        </div>
        </div>
      </div>
      {error && <p className="text-red-500 text-sm mb-4">{error}</p>}
      <button
        type="submit"
        className="w-full mt-2 bg-customlightblue hover:bg-opacity-80 text-customwhite py-2.5 px-4 rounded focus:outline-none focus:shadow-outline font-semibold font-montserrat rounded-lg"
      >
        Signup
      </button>
      
    </form>
  );
};

export default SignupForm;

