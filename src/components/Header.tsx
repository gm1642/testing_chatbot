"use client"
import React from 'react';
import { useRouter } from 'next/navigation';

const Header: React.FC = () => {
  const router = useRouter();
  const handleLogout = () => {
    localStorage.removeItem('authToken'); 

    // Redirect to login page
    router.push('/login');

  }
  return (
    <div className="bg-customblue h-16 flex items-center justify-end p-4">
      <button  onClick={handleLogout} className="bg-white20 hover:bg-opacity-80  text-customwhite py-2 px-6 mt-4 mr-3 rounded-lg font-montserrat font-semibold">Logout</button>
    </div>
  );
}

export default Header;
