import React from 'react';
import Sidebar from '@/components/layout/Sidebar';
import ActivityFeed from '@/components/dashboard/ActivityFeed';

const googleDocs = [
  { id: 1, title: 'Easall: Founder Manifesto', type: 'Strategy', url: '#' },
  { id: 2, title: 'jOY Events: Architecture Blueprint', type: 'Technical', url: '#' },
  { id: 3, title: 'Spectrum Dental: B2B Strategy', type: 'Marketing', url: '#' },
];

export default function DocsPage() {
  return (
    <div className="flex h-screen bg-slate-950 text-slate-50 overflow-hidden">
      <Sidebar />
      <main className="flex-1 flex flex-col min-w-0 bg-slate-950">
        <header className="h-16 border-b border-slate-900 px-8 flex items-center justify-between">
          <div>
            <h1 className="text-lg font-semibold text-slate-200">Docs</h1>
            <p className="text-[10px] text-slate-500 uppercase tracking-widest font-bold">Central Vault / Knowledge Base</p>
          </div>
        </header>
        <div className="p-8 space-y-4">
          <div className="bg-slate-900/30 border border-slate-800 p-4 rounded-lg flex items-center justify-between">
            <input type="text" placeholder="Search the vault..." className="bg-transparent text-sm focus:outline-none w-full" />
            <span className="text-slate-600">🔍</span>
          </div>
          <div className="grid gap-4">
            {googleDocs.map(doc => (
              <div key={doc.id} className="bg-slate-900/50 border border-slate-800 p-4 rounded-xl flex items-center gap-4 hover:border-slate-700 transition-colors cursor-pointer group">
                <div className="w-10 h-10 bg-slate-800 rounded flex items-center justify-center text-blue-400 group-hover:bg-blue-500/10 transition-colors">
                  📄
                </div>
                <div className="flex-1">
                  <h3 className="text-sm font-medium text-slate-200">{doc.title}</h3>
                  <p className="text-[10px] text-slate-500 uppercase tracking-tighter">{doc.type}</p>
                </div>
                <button className="text-[10px] font-bold text-slate-600 group-hover:text-blue-400 uppercase tracking-widest">Open →</button>
              </div>
            ))}
          </div>
        </div>
      </main>
      <ActivityFeed />
    </div>
  );
}
