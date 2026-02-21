import React from 'react';
import { LayoutGrid, CheckSquare, ClipboardCheck, Calendar, FolderHeart, FileText, BrainCircuit } from 'lucide-react';

const menuItems = [
  { icon: LayoutGrid, label: 'Dashboard', id: 'dashboard' },
  { icon: CheckSquare, label: 'Tasks', id: 'tasks' },
  { icon: ClipboardCheck, label: 'Approvals', id: 'approvals' },
  { icon: Calendar, label: 'Calendar', id: 'calendar' },
  { icon: FolderHeart, label: 'Projects', id: 'projects' },
  { icon: FileText, label: 'Docs', id: 'docs' },
  { icon: BrainCircuit, label: 'Memories', id: 'memories' },
];

export default function Sidebar() {
  return (
    <aside className="w-64 bg-slate-950 border-r border-slate-900 flex flex-col h-screen sticky top-0">
      <div className="p-6">
        <div className="flex items-center gap-3 text-blue-500 mb-8">
          <div className="w-8 h-8 bg-blue-500/10 rounded-lg flex items-center justify-center border border-blue-500/20">
            <span className="font-bold text-lg">B</span>
          </div>
          <span className="font-bold tracking-tight text-slate-200">THE BRIDGE</span>
        </div>
        
        <nav className="space-y-1">
          {menuItems.map((item) => (
            <button
              key={item.id}
              className={`w-full flex items-center gap-3 px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
                item.id === 'tasks' 
                  ? 'bg-slate-900 text-blue-400 border border-slate-800' 
                  : 'text-slate-400 hover:text-slate-200 hover:bg-slate-900/50'
              }`}
            >
              <item.icon className="w-4 h-4" />
              {item.label}
            </button>
          ))}
        </nav>
      </div>

      <div className="mt-auto p-6 border-t border-slate-900">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 rounded-full bg-gradient-to-tr from-blue-600 to-indigo-600 flex items-center justify-center text-[10px] font-bold">
            SA
          </div>
          <div className="flex-1 min-w-0">
            <p className="text-sm font-medium text-slate-200 truncate">Shane Anderson</p>
            <p className="text-xs text-slate-500 truncate">The Captain</p>
          </div>
        </div>
      </div>
    </aside>
  );
}
