import React from 'react';
import Sidebar from '@/components/layout/Sidebar';
import ActivityFeed from '@/components/dashboard/ActivityFeed';

export default function MemoriesPage() {
  return (
    <div className="flex h-screen bg-slate-950 text-slate-50 overflow-hidden">
      <Sidebar />
      <main className="flex-1 flex flex-col min-w-0 bg-slate-950">
        <header className="h-16 border-b border-slate-900 px-8 flex items-center justify-between">
          <div>
            <h1 className="text-lg font-semibold text-slate-200">Memories</h1>
            <p className="text-[10px] text-slate-500 uppercase tracking-widest font-bold">Semantic Search / Strategy Engine</p>
          </div>
        </header>
        <div className="p-8 space-y-6">
          <div className="bg-slate-900/30 border border-slate-800 p-6 rounded-xl space-y-4">
             <input 
              type="text" 
              placeholder="Search jOY Events ideas, strategy pivots..." 
              className="w-full bg-slate-950 border border-slate-800 rounded-lg p-3 text-sm focus:outline-none focus:border-blue-500 transition-colors"
            />
            <p className="text-[10px] text-slate-600 uppercase tracking-widest">Powering by OpenClaw Memory Engine</p>
          </div>
          <div className="flex items-center justify-center h-64 border-2 border-dashed border-slate-900 rounded-2xl">
            <p className="text-slate-600 text-sm italic text-center px-12">Search into your memories to retrieve project breakthroughs and decisions instantly.</p>
          </div>
        </div>
      </main>
      <ActivityFeed />
    </div>
  );
}
