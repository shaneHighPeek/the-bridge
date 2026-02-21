import React from 'react';

export default function Home() {
  const projects = [
    { name: 'jOY Events', status: 'Phase 1 (Ingestion)', lead: 'Klor', notes: 'SEQ Discovery Triangle active.' },
    { name: 'The Bridge', status: 'Phase 2 (Interface)', lead: 'Klor', notes: 'Command Centre is now live.' },
    { name: 'Spectrum Dental', status: 'Discovery', lead: 'Klor', notes: 'B2B Strategy in development.' },
    { name: 'BeeSold Engine', status: 'In Progress', lead: 'Shane', notes: 'Automated outreach engine.' },
  ];

  return (
    <main className="min-h-screen bg-slate-950 text-slate-50 p-8 font-sans">
      <div className="max-w-4xl mx-auto space-y-12">
        {/* Header */}
        <header className="border-b border-slate-800 pb-8">
          <h1 className="text-4xl font-bold tracking-tight text-blue-400">THE BRIDGE</h1>
          <p className="mt-2 text-slate-400">Command Centre for Shane & Lori</p>
        </header>

        {/* Project Registry */}
        <section className="space-y-6">
          <h2 className="text-xl font-semibold border-l-4 border-blue-500 pl-4">Active Projects</h2>
          <div className="grid gap-4 md:grid-cols-2">
            {projects.map((p) => (
              <div key={p.name} className="bg-slate-900 border border-slate-800 p-5 rounded-lg hover:border-slate-700 transition-colors">
                <div className="flex justify-between items-start">
                  <h3 className="text-lg font-bold text-slate-200">{p.name}</h3>
                  <span className="text-xs font-medium bg-blue-900/30 text-blue-300 px-2 py-1 rounded">{p.status}</span>
                </div>
                <p className="text-sm text-slate-400 mt-3">{p.notes}</p>
                <div className="mt-4 flex items-center text-xs text-slate-500">
                  <span className="mr-2">Lead:</span>
                  <span className="text-slate-300 font-medium">{p.lead}</span>
                </div>
              </div>
            ))}
          </div>
        </section>

        {/* Analytical Feed */}
        <section className="space-y-6">
          <h2 className="text-xl font-semibold border-l-4 border-orange-500 pl-4">What's Happened (Last 24h)</h2>
          <div className="bg-slate-900/50 border border-slate-800 rounded-lg p-6 space-y-4">
            <ul className="space-y-3 list-disc list-inside text-slate-300 text-sm">
              <li>Initialized <strong>The Bridge</strong> infrastructure on Vercel & GitHub.</li>
              <li>Rebuilt jOY Events architecture for <strong>SEQ Olympic Triangle</strong> (BNE-GC-SC).</li>
              <li>Integrated <strong>Ticketmaster Discovery API</strong> for real-time local events.</li>
              <li>Defined <strong>Morphic UI</strong> and <strong>Heat Meter</strong> logic for immersive discovery.</li>
            </ul>
          </div>
        </section>

        {/* Next Moves */}
        <section className="space-y-6">
          <h2 className="text-xl font-semibold border-l-4 border-green-500 pl-4">What's Next</h2>
          <div className="grid gap-4">
            <div className="flex items-center space-x-3 bg-slate-900 border border-slate-800 p-4 rounded-lg">
              <div className="h-5 w-5 border-2 border-slate-700 rounded flex-shrink-0"></div>
              <span className="text-sm text-slate-300">Connect <strong>Google Calendar API</strong> to sync schedules.</span>
            </div>
            <div className="flex items-center space-x-3 bg-slate-900 border border-slate-800 p-4 rounded-lg">
              <div className="h-5 w-5 border-2 border-slate-700 rounded flex-shrink-0"></div>
              <span className="text-sm text-slate-300">Run <strong>SEQ Triangle Harvest</strong> for Sunshine Coast data.</span>
            </div>
            <div className="flex items-center space-x-3 bg-slate-900 border border-slate-800 p-4 rounded-lg">
              <div className="h-5 w-5 border-2 border-slate-700 rounded flex-shrink-0"></div>
              <span className="text-sm text-slate-300">Map <strong>HighPeak Pro</strong> integration for client updates.</span>
            </div>
          </div>
        </section>

        <footer className="text-center text-slate-600 text-xs py-12">
          Sync active: {new Date().toLocaleDateString('en-AU')} | Secure Bridge Connection
        </footer>
      </div>
    </main>
  );
}
