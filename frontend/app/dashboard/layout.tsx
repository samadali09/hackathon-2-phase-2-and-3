"use client";

import React, { useState } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { Home, ListTodo, PlusCircle, Settings, LogOut, ChevronLeft, ChevronRight } from 'lucide-react'; // Lucide icons
import { motion } from 'framer-motion';

interface SidebarLinkProps {
  href: string;
  icon: React.ElementType;
  label: string;
  isCollapsed: boolean;
}

const SidebarLink: React.FC<SidebarLinkProps> = ({ href, icon: Icon, label, isCollapsed }) => {
  const pathname = usePathname();
  const isActive = pathname === href;

  return (
    <Link href={href} className={`flex items-center p-3 rounded-lg transition-colors duration-200 ${
      isActive
        ? 'bg-primary-purple/30 text-white shadow-lg backdrop-blur-sm' // Active glassmorphism effect
        : 'text-dark-text-secondary hover:bg-dark-surface/50 hover:text-white backdrop-blur-sm' // Inactive glassmorphism effect
    } ${isCollapsed ? 'justify-center' : ''}`}>
      <Icon className={`w-5 h-5 ${!isCollapsed ? 'mr-3' : ''}`} />
      {!isCollapsed && <span className="text-sm font-medium">{label}</span>}
    </Link>
  );
};

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const [isCollapsed, setIsCollapsed] = useState(false);

  const toggleSidebar = () => {
    setIsCollapsed(!isCollapsed);
  };

  return (
    <div className="flex min-h-screen bg-dark-background text-dark-text">
      {/* Sidebar */}
      <motion.aside
        initial={false}
        animate={{ width: isCollapsed ? '80px' : '256px' }}
        transition={{ duration: 0.3, ease: 'easeInOut' }}
        className="bg-dark-surface/40 backdrop-blur-xl p-6 border-r border-dark-border shadow-lg flex flex-col justify-between relative z-10"
      >
        <button
          onClick={toggleSidebar}
          className="absolute -right-3 top-6 p-1 bg-dark-surface border border-dark-border rounded-full shadow-lg text-white hover:bg-dark-border transition-colors z-20"
        >
          {isCollapsed ? <ChevronRight className="w-5 h-5" /> : <ChevronLeft className="w-5 h-5" />}
        </button>
        <div>
          <div className={`text-2xl font-bold text-white mb-10 ${isCollapsed ? 'text-center' : 'text-left'} transition-all duration-300`}>
            {isCollapsed ? '🌌' : '🌌 TaskFlow'}
          </div>
          <nav className="space-y-4">
            <SidebarLink href="/dashboard" icon={Home} label="Dashboard" isCollapsed={isCollapsed} />
            <SidebarLink href="/dashboard" icon={ListTodo} label="My Tasks" isCollapsed={isCollapsed} />
            <SidebarLink href="/dashboard" icon={PlusCircle} label="Add New Task" isCollapsed={isCollapsed} />
            {/* Add more links as needed */}
          </nav>
        </div>
        <div className="space-y-4">


        </div>
      </motion.aside>

      {/* Main content area */}
      <main className="flex-1 p-8 overflow-y-auto">
        {children}
      </main>
    </div>
  );
}
