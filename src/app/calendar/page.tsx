"use client";

import React, { useEffect, useState } from 'react';
import Sidebar from '@/components/layout/Sidebar';
import ActivityFeed from '@/components/dashboard/ActivityFeed';

export default function CalendarPage() {
  const [events, setEvents] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchCalendar() {
      try {
        const res = await fetch('/api/calendar');
        const data = await res.json();
        setEvents(data.events || []);
      } catch (err) {
        console.error("Calendar fetch failed");
      } finally {
        setLoading(false);
      }
    }
    fetchCalendar();
  }, []);

  // Group events by day for the 7-day view
  const groupEventsByDay = () => {
    const days: { [key: string]: any[] } = {};
    events.forEach(event => {
      const dateKey = new Date(event.start).toLocaleDateString('en-AU', { weekday: 'long', day: 'numeric', month: 'short' });
      if (!days[dateKey]) days[dateKey] = [];
      days[dateKey].push(event);
    });
    return days;
  };

  const groupedEvents = groupEventsByDay();

  return (
    <div className="flex h-screen bg-slate-950 text-slate-50 overflow-hidden text-xs">
      <Sidebar />
      <main className="flex-1 flex flex-col min-w-0 bg-slate-950 overflow-y-auto pt-16 lg:pt-0">
        <header className="h-16 border-b border-slate-900 px-4 md:px-8 flex items-center justify-between bg-slate-950/50 backdrop-blur-sm sticky top-0 z-10">
          <div className="pl-12 lg:pl-0">
            <h1 className="text-lg font-semibold text-slate-200">Calendar</h1>
            <p className="text-[10px] text-slate-500 uppercase tracking-widest font-bold">7-Day SEQ Schedule / AEST Timezone</p>
          </div>
        </header>

        <div className="p-4 md:p-8 space-y-10 max-w-5xl">
          {loading ? (
            <div className="text-center py-20 space-y-4">
              <div className="w-12 h-12 bg-blue-500/10 rounded-full flex items-center justify-center mx-auto border border-blue-500/20 text-blue-500">
                <span className="animate-pulse text-2xl">📅</span>
              </div>
              <h2 className="text-slate-200 font-medium">Syncing Triangle Schedule...</h2>
            </div>
          ) : (
            Object.keys(groupedEvents).map(day => (
              <section key={day} className="space-y-4">
                <h2 className="text-sm font-bold border-l-4 border-blue-500 pl-4 uppercase tracking-widest text-slate-400">{day}</h2>
                <div className="grid gap-3">
                  {groupedEvents[day].map(event => (
                    <div key={event.id} className="bg-slate-900/40 border border-slate-800/60 p-4 rounded-xl flex items-center justify-between hover:border-slate-700 transition-colors group">
                      <div className="space-y-1">
                        <div className="flex items-center gap-2">
                          <span className="text-[9px] font-bold text-blue-400 uppercase tracking-tighter bg-blue-900/20 px-1.5 py-0.5 rounded">
                            {event.calendar}
                          </span>
                          <span className="text-[9px] font-medium text-slate-500 uppercase tracking-widest">{event.type}</span>
                        </div>
                        <h3 className="text-sm font-medium text-slate-200 group-hover:text-blue-400 transition-colors">{event.summary}</h3>
                      </div>
                      <div className="text-right flex-shrink-0">
                        <p className="text-[11px] text-slate-300 font-mono">
                          {new Date(event.start).toLocaleTimeString('en-AU', { hour: '2-digit', minute: '2-digit', hour12: true })}
                        </p>
                        <p className="text-[9px] text-slate-500 uppercase tracking-tighter italic">AEST</p>
                      </div>
                    </div>
                  ))}
                </div>
              </section>
            ))
          )}
        </div>
      </main>
      <div className="hidden xl:block">
        <ActivityFeed />
      </div>
    </div>
  );
}
