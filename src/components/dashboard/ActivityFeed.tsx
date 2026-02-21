import React from 'react';

const activities = [
  { id: 1, user: 'KLOR', action: 'Deployed Bridge Dashboard V1', time: '5m ago' },
  { id: 2, user: 'KLOR', action: 'Patched Next.js RCE Security Flaw', time: '20m ago' },
  { id: 3, user: 'KLOR', action: 'Mapped 3 Google Calendars (Shane/Lori)', time: '45m ago' },
  { id: 4, user: 'KLOR', action: 'Completed Brisbane Council Data Pull', time: '2h ago' },
  { id: 5, user: 'Captain', action: 'Defined Bridge Vision & Pipeline', time: '3h ago' },
];

export default function ActivityFeed() {
  return (
    <aside className="w-80 bg-slate-950/50 border-l border-slate-900 p-6 flex flex-col h-screen overflow-y-auto">
      <h2 className="text-xs font-semibold text-slate-500 uppercase tracking-widest mb-6">Live Activity</h2>
      <div className="space-y-6">
        {activities.map((activity) => (
          <div key={activity.id} className="relative pl-4 border-l border-slate-800 pb-1">
            <div className="absolute -left-1 top-0 w-2 h-2 rounded-full bg-blue-500/50 shadow-[0_0_8px_rgba(59,130,246,0.5)]"></div>
            <div className="flex justify-between items-start mb-1">
              <span className="text-[10px] font-bold text-blue-400">@{activity.user.toLowerCase()}</span>
              <span className="text-[10px] text-slate-600">{activity.time}</span>
            </div>
            <p className="text-xs text-slate-300 leading-relaxed">{activity.action}</p>
          </div>
        ))}
      </div>
    </aside>
  );
}
