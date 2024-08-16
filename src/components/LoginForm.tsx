'use client';

import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import axios from 'axios';
import Image from 'next/image';
import Email from 'next-auth/providers/email';

const LoginForm: React.FC = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const router = useRouter();

  const togglePasswordVisibilty = () =>{
    setShowPassword(!showPassword);
  };



  

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    try {
      const response = await axios.post('/api/login', { email, password });
      const { token } = response.data;
      localStorage.setItem('token', token);
      router.push('/dashboard');
    } catch (error) {
      // TypeScript type guard for AxiosError
      if (axios.isAxiosError(error)) {
        if (error.response) {
          const { status } = error.response;
          
         
          if (status === 400) {
            alert('You don\'t have an account. Please sign up.');
            router.push('/signup');
          } else {
            alert('Login failed: ' + (error.response.data?.message || 'An unknown error occurred'));
          }
        } else {
          alert('Login failed: No response from server');
        }
      } else {
        alert('Login failed: An unexpected error occurred');
      }
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-customblue">
      <div className="w-full max-w-md">
      <div className="text-center mb-8">
        <div className="flex justify-center items-center mb-2 space-x-5">
          <Image src="/bot 1.svg" alt="ExamBot Logo" width={50} height={50} />
          <h1 className="text-3xl font-bold text-customwhite font-cabin">ExamBot</h1>
        </div>
      </div>
        <form onSubmit={handleSubmit} className="bg-customblue px-8 pt-6 pb-8 mb-4">
          <div className="mb-4">
            <div className="relative">
            <div className="absolute inset-y-0 left-0 flex items-center pl-5 pointer-events-none">
        <img src="/Vector (1).svg" alt="Icon" className="h-4 w-5" />
      </div>
              <input
                type="text"
                id="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-[330px] h-[50px] pl-14 bg-white25 text-fieldwhite px-3 py-2 rounded-lg focus:outline-none focus:ring-2 focus:ring-customlightblue font-montserrat"
                placeholder="Email"
                required
              />
            </div>
          </div>
          <div className="mb-6">
            <div className="relative">
            <div className="absolute inset-y-0 left-0 flex items-center pl-5 pointer-events-none">
        <img src="/Vector.svg" alt="Icon" className="h-4 w-5" />
      </div>
              <input
                type={showPassword ? 'text' : 'password'}
                id="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-[330px] h-[50px] pl-14 bg-white25 text-fieldwhite px-3 py-2 rounded-lg focus:outline-none focus:ring-2 focus:ring-customlightblue font-montserrat"
                placeholder="Password"
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
          <div className="flex items-center justify-between ">
            <button
              type="submit"
              className="w-full mt-2 bg-customlightblue hover:bg-opacity-80 text-customwhite  py-2.5 px-4 rounded focus:outline-none focus:shadow-outline font-semibold font-montserrat rounded-lg"
            >
              LOGIN
            </button>
          </div>
        </form>
        <p className="text-center text-customwhite text-sm font-montserrat">
          Don't have an account? <a href="/signup" className="text-customlightblue hover:underline font-montserrat">Sign up</a>
        </p>
      </div>
    </div>
  );
};

export default LoginForm;