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

  return (
    <div className="flex h-screen bg-slate-950 text-slate-50 overflow-hidden">
      <Sidebar />
      <main className="flex-1 flex flex-col min-w-0 bg-slate-950 overflow-y-auto">
        <header className="h-16 border-b border-slate-900 px-4 md:px-8 flex items-center justify-between bg-slate-950/50 backdrop-blur-sm sticky top-0 z-10">
          <div className="pl-12 lg:pl-0">
            <h1 className="text-lg font-semibold text-slate-200">Calendar</h1>
            <p className="text-[10px] text-slate-500 uppercase tracking-widest font-bold">Unified Triangle Schedule</p>
          </div>
        </header>

        <div className="p-4 md:p-8 space-y-6">
          {loading ? (
            <div className="text-center py-20 space-y-4">
              <div className="w-12 h-12 bg-blue-500/10 rounded-full flex items-center justify-center mx-auto border border-blue-500/20 text-blue-500">
                <span className="animate-pulse">📅</span>
              </div>
              <h2 className="text-slate-200 font-medium">Syncing Google Workspace...</h2>
            </div>
          ) : (
            <div className="grid gap-4">
              {events.map((event) => (
                <div key={event.id} className="bg-slate-900/40 border border-slate-800 p-5 rounded-xl flex flex-col md:flex-row md:items-center justify-between gap-4">
                  <div className="space-y-1">
                    <span className="text-[10px] font-bold text-blue-500 uppercase tracking-tighter bg-blue-500/10 px-2 py-0.5 rounded">
                      {event.calendar}
                    </span>
                    <h3 className="text-sm font-medium text-slate-200">{event.summary}</h3>
                  </div>
                  <div className="text-right">
                    <p className="text-xs text-slate-400 font-mono">
                      {new Date(event.start).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })} - {new Date(event.end).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                    </p>
                    <p className="text-[10px] text-slate-600 uppercase tracking-tighter">
                      {new Date(event.start).toLocaleDateString('en-AU', { weekday: 'short', day: 'numeric', month: 'short' })}
                    </p>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </main>
      <div className="hidden xl:block">
        <ActivityFeed />
      </div>
    </div>
  );
}
