import React from 'react';
import DashboardSidebar from '../../components/DashboardSidebar';
import Header from '../../components/Header';
import ChatBox from '../../components/Chatbox';

const DashboardPage: React.FC = () => {
  return (
    <div className="h-screen flex bg-customblue text-customwhite">
      <DashboardSidebar />
      <div className="flex flex-col flex-grow">
        <Header />
        <div className="flex-grow p-4">
          <ChatBox />
        </div>
      </div>
    </div>
  );
}

export default DashboardPage;
