import React from 'react';
import Sidebar from '@/components/layout/Sidebar';
import ActivityFeed from '@/components/dashboard/ActivityFeed';

export default function Home() {
  const projects = [
    { name: 'jOY Events', status: 'Phase 1 (Ingestion)', lead: 'Klor', notes: 'SEQ Discovery Triangle active.' },
    { name: 'The Bridge', status: 'Phase 2 (Interface)', lead: 'Klor', notes: 'Command Centre is now live.' },
    { name: 'Spectrum Dental', status: 'Discovery', lead: 'Klor', notes: 'B2B Strategy in development.' },
    { name: 'BeeSold Engine', status: 'In Progress', lead: 'Shane', notes: 'Automated outreach engine.' },
  ];

  return (
    <div className="flex h-screen bg-slate-950 text-slate-50 overflow-hidden">
      <Sidebar />
      
      <main className="flex-1 flex flex-col min-w-0 bg-slate-950 overflow-y-auto">
        <header className="h-16 border-b border-slate-900 px-8 flex items-center justify-between bg-slate-950/50 backdrop-blur-sm sticky top-0 z-10">
          <div>
            <h1 className="text-lg font-semibold text-slate-200 uppercase tracking-widest text-xs">The Bridge</h1>
            <p className="text-[10px] text-slate-500 uppercase tracking-widest font-bold">Command Centre for Shane & Lori</p>
          </div>
        </header>

        <div className="p-8 space-y-12 max-w-5xl">
          {/* Active Projects */}
          <section className="space-y-6">
            <h2 className="text-sm font-bold border-l-4 border-blue-500 pl-4 uppercase tracking-widest text-slate-400">Active Projects</h2>
            <div className="grid gap-4 md:grid-cols-2">
              {projects.map((p) => (
                <div key={p.name} className="bg-slate-900/40 border border-slate-800/60 p-5 rounded-xl hover:border-slate-700 transition-colors group">
                  <div className="flex justify-between items-start">
                    <h3 className="text-md font-bold text-slate-200 group-hover:text-blue-400 transition-colors">{p.name}</h3>
                    <span className="text-[10px] font-bold bg-blue-900/20 text-blue-400 px-2 py-1 rounded border border-blue-500/10 uppercase tracking-tighter">{p.status}</span>
                  </div>
                  <p className="text-xs text-slate-400 mt-3 leading-relaxed">{p.notes}</p>
                  <div className="mt-4 flex items-center text-[10px] text-slate-500 uppercase tracking-widest">
                    <span className="mr-2 italic">Lead:</span>
                    <span className="text-slate-300 font-bold">{p.lead}</span>
                  </div>
                </div>
              ))}
            </div>
          </section>

          {/* Analytical Feed */}
          <section className="space-y-6">
            <h2 className="text-sm font-bold border-l-4 border-orange-500 pl-4 uppercase tracking-widest text-slate-400">What's Happened (Last 24h)</h2>
            <div className="bg-slate-900/30 border border-slate-800/60 rounded-xl p-6">
              <ul className="space-y-4">
                {[
                  'Initialized **The Bridge** infrastructure on Vercel & GitHub.',
                  'Rebuilt jOY Events architecture for **SEQ Olympic Triangle** (BNE-GC-SC).',
                  'Integrated **Ticketmaster Discovery API** for real-time local events.',
                  'Defined **Morphic UI** and **Heat Meter** logic for immersive discovery.'
                ].map((item, i) => (
                  <li key={i} className="flex items-start gap-3 text-xs text-slate-300 leading-relaxed">
                    <span className="text-orange-500 mt-1.5">•</span>
                    <span>{item.split('**').map((part, index) => index % 2 === 1 ? <strong key={index} className="text-slate-100 font-semibold">{part}</strong> : part)}</span>
                  </li>
                ))}
              </ul>
            </div>
          </section>

          {/* Next Moves */}
          <section className="space-y-6">
            <h2 className="text-sm font-bold border-l-4 border-green-500 pl-4 uppercase tracking-widest text-slate-400">What's Next</h2>
            <div className="grid gap-3">
              {[
                'Connect **Google Calendar API** to sync schedules.',
                'Run **SEQ Triangle Harvest** for Sunshine Coast data.',
                'Map **HighPeak Pro** integration for client updates.'
              ].map((item, i) => (
                <div key={i} className="flex items-center space-x-4 bg-slate-900/20 border border-slate-800/40 p-4 rounded-xl hover:bg-slate-900/40 transition-colors">
                  <div className="h-4 w-4 border-2 border-slate-700 rounded-sm flex-shrink-0"></div>
                  <span className="text-xs text-slate-400 font-medium">
                    {item.split('**').map((part, index) => index % 2 === 1 ? <strong key={index} className="text-slate-200 font-semibold">{part}</strong> : part)}
                  </span>
                </div>
              ))}
            </div>
          </section>
        </div>
      </main>

      <ActivityFeed />
    </div>
  );
}
