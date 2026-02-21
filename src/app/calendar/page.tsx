import React from 'react';
import Sidebar from '@/components/layout/Sidebar';
import ActivityFeed from '@/components/dashboard/ActivityFeed';

export default function CalendarPage() {
  return (
    <div className="flex h-screen bg-slate-950 text-slate-50 overflow-hidden">
      <Sidebar />
      <main className="flex-1 flex flex-col min-w-0 bg-slate-950">
        <header className="h-16 border-b border-slate-900 px-8 flex items-center justify-between">
          <div>
            <h1 className="text-lg font-semibold text-slate-200">Calendar</h1>
            <p className="text-[10px] text-slate-500 uppercase tracking-widest font-bold">Unified Triangle Schedule</p>
          </div>
        </header>
        <div className="p-8 flex-1 flex items-center justify-center border-b border-slate-900/50">
          <div className="text-center space-y-4 max-w-md">
            <div className="w-12 h-12 bg-blue-500/10 rounded-full flex items-center justify-center mx-auto border border-blue-500/20 text-blue-500">
               <span className="animate-pulse">📅</span>
            </div>
            <h2 className="text-slate-200 font-medium">Syncing Google Workspace...</h2>
            <p className="text-sm text-slate-500 leading-relaxed">
              Fetching events from Shane (x2), Lori, and jOY Regional Pulse. 
              Live schedule grid will appear here shortly.
            </p>
          </div>
        </div>
      </main>
      <ActivityFeed />
    </div>
  );
}
