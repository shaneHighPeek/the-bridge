import React from 'react';
import Sidebar from '@/components/layout/Sidebar';
import ActivityFeed from '@/components/dashboard/ActivityFeed';

const projects = [
  { id: 1, name: 'jOY Events', status: 'Phase 1 (Ingestion)', lead: 'KLOR', health: 'Healthy' },
  { id: 2, name: 'The Bridge', status: 'Phase 2 (Interface)', lead: 'KLOR', health: 'Critical Patch Applied' },
  { id: 3, name: 'Spectrum Dental', status: 'Discovery', lead: 'KLOR', health: 'On Hold' },
];

export default function ProjectsPage() {
  return (
    <div className="flex h-screen bg-slate-950 text-slate-50 overflow-hidden">
      <Sidebar />
      <main className="flex-1 flex flex-col min-w-0 bg-slate-950">
        <header className="h-16 border-b border-slate-900 px-8 flex items-center justify-between">
          <div>
            <h1 className="text-lg font-semibold text-slate-200">Projects</h1>
            <p className="text-[10px] text-slate-500 uppercase tracking-widest font-bold">Deep Dive / Strategic Roadmaps</p>
          </div>
        </header>
        <div className="p-8 space-y-6 overflow-y-auto">
          {projects.map(project => (
            <div key={project.id} className="bg-slate-900/50 border border-slate-800 p-6 rounded-xl space-y-4">
              <div className="flex justify-between items-center">
                <h2 className="text-xl font-bold text-slate-100">{project.name}</h2>
                <span className="text-[10px] font-bold bg-blue-500/10 text-blue-400 px-2 py-1 rounded border border-blue-500/20">{project.status}</span>
              </div>
              <div className="grid grid-cols-3 gap-4 text-xs">
                <div className="p-3 bg-slate-950 rounded-lg border border-slate-800">
                  <p className="text-slate-500 mb-1">Lead</p>
                  <p className="font-medium text-slate-200">{project.lead}</p>
                </div>
                <div className="p-3 bg-slate-950 rounded-lg border border-slate-800">
                  <p className="text-slate-500 mb-1">Health</p>
                  <p className="font-medium text-green-400">{project.health}</p>
                </div>
                <div className="p-3 bg-slate-950 rounded-lg border border-slate-800">
                  <p className="text-slate-500 mb-1">Last Update</p>
                  <p className="font-medium text-slate-200">Today</p>
                </div>
              </div>
              <button className="text-[10px] font-bold text-slate-400 uppercase tracking-widest hover:text-blue-400 transition-colors">View Scorecard →</button>
            </div>
          ))}
        </div>
      </main>
      <ActivityFeed />
    </div>
  );
}
