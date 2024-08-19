'use client'
import React from 'react';
import { useState } from 'react';

const DashboardSidebar: React.FC = () => {

  const [isExamTypeOpen, setIsExamTypeOpen] = useState(false);
  const [isYearOpen, setIsYearOpen] = useState(false);

  const toggleExamType = () => setIsExamTypeOpen(!isExamTypeOpen);
  const toggleYear = () => setIsYearOpen(!isYearOpen);


  return (
    <div className="bg-white20 w-[235px] h-full p-4 flex flex-col justify-between">
      <div>
        <div className="flex items-center mb-10">
          <img src="/bot 1.svg" alt="ExamBot" className="w-8 h-8 mr-2" />
          <h1 className="text-customwhite text-2xl font-bold font-cabin ">ExamBot</h1>
        </div>
        <div>

        <div className="relative inline-block">
  <button
    onClick={toggleExamType}
    className="bg-customlightblue w-[210px] text-customwhite px-6 py-2 mb-4 rounded-lg font-montserrat font-semibold text-base flex items-center justify-between"
  >
    Exam Type
    <span
      className={`transform transition-transform ${
        isExamTypeOpen ? 'rotate-180' : ''
      }`}
    >
      <img src="/arrow-down 1.svg" alt="Arrow" className="ml-2 mr-2" />
    </span>
  </button>
  {isExamTypeOpen && (
    <ul className="absolute left-full top-0 bg-customgrey w-[210px] text-customwhite py-2 rounded-lg mt-2 z-10">
      <li className="px-4 py-2 hover:bg-customlightblue">Gate</li>
    </ul>
  )}
</div>
<div className="relative inline-block">
  <button
    onClick={toggleYear}
    className="bg-customlightblue w-[210px] text-customwhite px-6 py-2 mb-4 rounded-lg font-montserrat font-semibold text-base flex items-center justify-between"
  >
    Year
    <span
      className={`transform transition-transform ${
        isYearOpen ? 'rotate-180' : ''
      }`}
    >
      <img src="/arrow-down 1.svg" alt="Arrow" className="ml-2 mr-2" />
    </span>
  </button>
  {isYearOpen && (
    <ul className="absolute left-full top-0 bg-customgrey w-[210px] text-customwhite py-2 rounded-lg mt-2 z-10">
      <li className="px-4 py-2 hover:bg-customlightblue">2024</li>
              <li className="px-4 py-2 hover:bg-customlightblue">2023</li>
              <li className="px-4 py-2 hover:bg-customlightblue">2022</li>
    </ul>
  )}
</div>

          
        </div>
      </div>
      
    </div>
  );
}

export default DashboardSidebar;
