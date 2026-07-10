import { Outlet } from "react-router-dom";

import ChatbotButton from "../../features/chatbot/components/ChatbotButton.jsx";
import Header from "./Header.jsx";
import Sidebar from "./Sidebar.jsx";

export default function AppLayout() {
  return (
    <div className="surface-line min-h-screen bg-forge-bg text-forge-text">
      <div className="flex min-h-screen">
        <Sidebar />
        <div className="flex min-w-0 flex-1 flex-col">
          <Header />
          <main className="flex-1 px-4 py-5 md:px-6 lg:px-8">
            <Outlet />
          </main>
        </div>
      </div>
      <ChatbotButton />
    </div>
  );
}
