import React from 'react';
import Sidebar from '@/components/layout/Sidebar';
import TaskBoard from '@/components/dashboard/TaskBoard';
import ActivityFeed from '@/components/dashboard/ActivityFeed';

export default function TasksPage() {
  return (
    <div className="flex h-screen bg-slate-950 text-slate-50 overflow-hidden">
      <Sidebar />
      <main className="flex-1 flex flex-col min-w-0 bg-slate-950">
        <header className="h-16 border-b border-slate-900 px-4 md:px-8 flex items-center justify-between bg-slate-950/50 backdrop-blur-sm sticky top-0 z-10">
          <div>
            <h1 className="text-lg font-semibold text-slate-200">Tasks</h1>
            <p className="text-[10px] text-slate-500 uppercase tracking-widest font-bold">Mission Control / Active Sprints</p>
          </div>
          <div className="hidden md:flex items-center gap-4 text-xs font-medium">
            <span className="flex items-center gap-1.5 text-green-400 bg-green-400/5 px-2 py-1 rounded border border-green-500/10">
              <span className="w-1.5 h-1.5 rounded-full bg-green-500"></span>
              3 Completed
            </span>
          </div>
        </header>
        <TaskBoard />
      </main>
      <div className="hidden xl:block">
        <ActivityFeed />
      </div>
    </div>
  );
}
