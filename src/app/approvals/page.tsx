import React from 'react';
import Sidebar from '@/components/layout/Sidebar';
import ActivityFeed from '@/components/dashboard/ActivityFeed';

const approvalitems = [
  { id: 1, title: 'Weekly Vibe Forecast Script', project: 'jOY Events', status: 'Pending Approval' },
  { id: 2, title: 'Spectrum Dental Outreach Template', project: 'Spectrum', status: 'Pending Approval' },
];

export default function ApprovalsPage() {
  return (
    <div className="flex h-screen bg-slate-950 text-slate-50 overflow-hidden">
      <Sidebar />
      <main className="flex-1 flex flex-col min-w-0 bg-slate-950">
        <header className="h-16 border-b border-slate-900 px-8 flex items-center justify-between">
          <div>
            <h1 className="text-lg font-semibold text-slate-200">Approvals</h1>
            <p className="text-[10px] text-slate-500 uppercase tracking-widest font-bold">Pipeline / Content Guardrails</p>
          </div>
        </header>
        <div className="p-8 space-y-6">
          <div className="grid gap-4">
            {approvalitems.map(item => (
              <div key={item.id} className="bg-slate-900/50 border border-slate-800 p-5 rounded-xl flex items-center justify-between hover:border-slate-700 transition-all">
                <div className="space-y-1">
                  <span className="text-[10px] font-bold text-orange-500 uppercase tracking-tighter bg-orange-500/10 px-2 py-0.5 rounded">{item.project}</span>
                  <h3 className="text-sm font-medium text-slate-200">{item.title}</h3>
                </div>
                <div className="flex gap-2">
                  <button className="px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-xs font-semibold rounded-lg transition-colors border border-slate-700">Review</button>
                  <button className="px-3 py-1.5 bg-green-600/20 hover:bg-green-600/30 text-green-400 text-xs font-semibold rounded-lg transition-colors border border-green-500/20">Approve</button>
                </div>
              </div>
            ))}
          </div>
        </div>
      </main>
      <ActivityFeed />
    </div>
  );
}
