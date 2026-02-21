"use client";

import React, { useEffect, useState } from 'react';
import Sidebar from '@/components/layout/Sidebar';

export default function CalendarPage() {
  const [routines, setRoutines] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  const daysOfWeek = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];

  useEffect(() => {
    async function fetchRoutines() {
      try {
        const res = await fetch('/api/calendar');
        const data = await res.json();
        setRoutines(data.routines || []);
      } catch (err) {
        console.error("Routine fetch failed");
      } finally {
        setLoading(false);
      }
    }
    fetchRoutines();
  }, []);

  const getDayRoutines = (dayIndex: number) => {
    return routines.filter(routine => {
      const routineDate = new Date(routine.start);
      return routineDate.getDay() === dayIndex;
    });
  };

  const getVibeColor = (type: string) => {
    switch (type?.toLowerCase()) {
      case 'system': return 'bg-blue-500/20 border-blue-500/40 text-blue-300';
      case 'data': return 'bg-green-500/20 border-green-500/40 text-green-300';
      case 'joy': return 'bg-orange-500/20 border-orange-500/40 text-orange-300';
      case 'content': return 'bg-purple-500/20 border-purple-500/40 text-purple-300';
      case 'crm': return 'bg-indigo-500/20 border-indigo-500/40 text-indigo-300';
      default: return 'bg-slate-800/40 border-slate-700/60 text-slate-300';
    }
  };

  return (
    <div className="flex h-screen bg-slate-950 text-slate-50 overflow-hidden text-xs">
      <Sidebar />
      <main className="flex-1 flex flex-col min-w-0 bg-slate-950 overflow-y-auto pt-16 lg:pt-0">
        <header className="h-16 border-b border-slate-900 px-4 md:px-8 flex items-center justify-between bg-slate-950/50 backdrop-blur-sm sticky top-0 z-10">
          <div className="pl-12 lg:pl-0">
            <h1 className="text-lg font-semibold text-slate-200">Scheduled Tasks</h1>
            <p className="text-[10px] text-slate-500 uppercase tracking-widest font-bold">KLOR's Automated Routines / AEST</p>
          </div>
          <div className="flex gap-2">
            <button className="px-3 py-1 bg-slate-900 border border-slate-800 rounded text-[10px] font-bold uppercase tracking-tighter">Week</button>
            <button className="px-3 py-1 text-slate-500 text-[10px] font-bold uppercase tracking-tighter hover:text-slate-300">Today</button>
          </div>
        </header>

        <div className="p-4 md:p-8 space-y-10 max-w-[1600px] mx-auto w-full">
          {/* Always Running Section */}
          <section className="space-y-4">
             <div className="flex items-center gap-2 text-slate-400">
               <span className="text-blue-500 text-xs">⚡</span>
               <h2 className="text-[10px] font-bold uppercase tracking-widest text-slate-500">Always Running</h2>
             </div>
             <div className="flex flex-wrap gap-3">
               {routines.filter(r => r.frequency.includes('Every')).map(r => (
                 <div key={r.id} className="bg-blue-500/5 border border-blue-500/20 p-3 rounded-lg flex items-center gap-3">
                    <span className="text-blue-400 font-medium">{r.summary.toLowerCase()}</span>
                    <span className="text-blue-500/40">•</span>
                    <span className="text-slate-500">{r.frequency.toLowerCase()}</span>
                 </div>
               ))}
             </div>
          </section>

          {/* 7-Day Grid of Routines */}
          <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-7 gap-3">
            {daysOfWeek.map((day, idx) => (
              <div key={day} className="flex flex-col gap-3">
                <h3 className="text-[10px] font-bold text-slate-600 uppercase tracking-widest mb-1 px-1">{day}</h3>
                <div className="flex-1 space-y-2">
                  {getDayRoutines(idx).map((r: any) => (
                    <div key={r.id} className={`p-3 rounded-lg border flex flex-col gap-1 transition-all hover:scale-[1.02] ${getVibeColor(r.type)}`}>
                      <span className="font-bold truncate leading-tight">{r.summary.toLowerCase()}</span>
                      <span className="text-[9px] opacity-60 font-mono">
                        {new Date(r.start).toLocaleTimeString('en-AU', { hour: 'numeric', minute: '2-digit', hour12: true }).toLowerCase()}
                      </span>
                    </div>
                  ))}
                  {getDayRoutines(idx).length === 0 && (
                    <div className="h-24 border border-slate-900 border-dashed rounded-xl bg-slate-900/10"></div>
                  )}
                </div>
              </div>
            ))}
          </div>

          {/* Next Up List with Time Indicators */}
          <section className="space-y-6 pt-12 border-t border-slate-900">
            <div className="flex items-center gap-2 text-slate-400">
               <span className="text-xs">📋</span>
               <h2 className="text-[10px] font-bold uppercase tracking-widest text-slate-500">Next Up</h2>
             </div>
             <div className="space-y-1">
               {routines.filter(r => r.next_run !== 'Completed').slice(0, 6).map(r => (
                 <div key={r.id} className="flex justify-between items-center group cursor-pointer border-b border-slate-900/50 py-4 hover:bg-slate-900/10 px-2 rounded-lg transition-colors">
                   <span className={`text-sm font-medium transition-colors ${getVibeColor(r.type).split(' ')[2]}`}>
                     {r.summary.toLowerCase()}
                   </span>
                   <span className="text-[10px] text-slate-600 font-mono group-hover:text-slate-400 transition-colors italic uppercase tracking-tighter">
                     {r.next_run.toLowerCase()}
                   </span>
                 </div>
               ))}
             </div>
          </section>
        </div>
      </main>
    </div>
  );
}
