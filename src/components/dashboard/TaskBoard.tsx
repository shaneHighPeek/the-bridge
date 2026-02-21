import React from 'react';

const tasks = {
  backlog: [
    { id: 1, title: 'Olympic Hub: Mapping SC Venues', project: 'jOY Events', days: '2d ago', color: 'orange' },
    { id: 2, title: 'Weekly Vibe Forecast Script', project: 'Content', days: '1d ago', color: 'blue' },
    { id: 3, title: 'High Peek Pro API Endpoints Mapping', project: 'Infra', days: '4h ago', color: 'purple' },
  ],
  inProgress: [
    { id: 4, title: 'Bridge Dashboard Facelift', project: 'The Bridge', days: 'Just now', color: 'blue' },
    { id: 5, title: 'SEQ Triangle Data Harvest', project: 'jOY Events', days: '2h ago', color: 'green' },
  ],
};

export default function TaskBoard() {
  return (
    <div className="flex-1 grid grid-cols-1 lg:grid-cols-2 gap-8 p-8 overflow-y-auto">
      <section>
        <div className="flex items-center gap-2 mb-6">
          <div className="w-2 h-2 rounded-full bg-slate-500"></div>
          <h2 className="text-sm font-semibold text-slate-400 uppercase tracking-wider">Backlog</h2>
          <span className="ml-auto text-xs text-slate-600 bg-slate-900 px-2 py-0.5 rounded-full">{tasks.backlog.length}</span>
        </div>
        <div className="space-y-4">
          {tasks.backlog.map(task => (
            <div key={task.id} className="bg-slate-900/50 border border-slate-800 p-5 rounded-xl hover:border-slate-700 transition-all cursor-pointer group">
              <div className="flex justify-between items-start mb-3">
                <span className={`text-[10px] font-bold uppercase tracking-tighter text-${task.color}-500 bg-${task.color}-500/10 px-2 py-0.5 rounded`}>
                  {task.project}
                </span>
                <span className="text-[10px] text-slate-600 font-mono">{task.days}</span>
              </div>
              <h3 className="text-slate-200 font-medium group-hover:text-blue-400 transition-colors">{task.title}</h3>
            </div>
          ))}
        </div>
      </section>

      <section>
        <div className="flex items-center gap-2 mb-6">
          <div className="w-2 h-2 rounded-full bg-blue-500 animate-pulse"></div>
          <h2 className="text-sm font-semibold text-slate-400 uppercase tracking-wider">In Progress</h2>
          <span className="ml-auto text-xs text-slate-600 bg-slate-900 px-2 py-0.5 rounded-full">{tasks.inProgress.length}</span>
        </div>
        <div className="space-y-4">
          {tasks.inProgress.map(task => (
            <div key={task.id} className="bg-slate-900/50 border border-slate-800 p-5 rounded-xl hover:border-blue-500/30 transition-all cursor-pointer border-l-2 border-l-blue-500">
              <div className="flex justify-between items-start mb-3">
                <span className={`text-[10px] font-bold uppercase tracking-tighter text-${task.color}-500 bg-${task.color}-500/10 px-2 py-0.5 rounded`}>
                  {task.project}
                </span>
                <span className="text-[10px] text-slate-600 font-mono">{task.days}</span>
              </div>
              <h3 className="text-slate-200 font-medium">{task.title}</h3>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}
