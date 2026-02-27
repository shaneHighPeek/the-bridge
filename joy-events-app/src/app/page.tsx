"use client";

import React, { useState, useEffect } from 'react';
import { Menu, Loader2 } from 'lucide-react';

type Vibe = 'DEFAULT' | 'SPORTS' | 'MUSIC' | 'CHILL';
type Location = 'BRISBANE' | 'GC' | 'SC';

interface Event {
  id: string;
  title: string;
  date: string;
  venue: string;
  hero: string;
  link: string;
}

export default function Home() {
  const [vibe, setVibe] = useState<Vibe>('DEFAULT');
  const [location, setLocation] = useState<Location | null>(null);
  const [showEvents, setShowEvents] = useState(false);
  const [events, setEvents] = useState<Event[]>([]);
  const [loading, setLoading] = useState(false);

  const themes = {
    DEFAULT: {
      outsideBg: 'bg-slate-950',
      accent: 'text-blue-500',
      glow: 'shadow-blue-500/30',
      visual: 'url("https://images.unsplash.com/photo-1518173946687-a4c8a9ba332f?auto=format&fit=crop&q=80&w=2000")',
      description: 'The SEQ Discovery Engine. Discover the soul of South East Queensland.'
    },
    SPORTS: {
      outsideBg: 'bg-[#2D0012]',
      accent: 'text-[#FFB81C]',
      glow: 'shadow-[#FFB81C]/30',
      visual: 'url("https://images.unsplash.com/photo-1540747913346-19e32dc3e97e?auto=format&fit=crop&q=80&w=2000")',
      description: 'The Game is Calling. Your home for Brisbane and Gold Coast sport.'
    },
    MUSIC: {
      outsideBg: 'bg-[#0a0a0a]',
      accent: 'text-fuchsia-500',
      glow: 'shadow-fuchsia-500/30',
      visual: 'url("https://images.unsplash.com/photo-1470225620780-dba8ba36b745?auto=format&fit=crop&q=80&w=2000")',
      description: 'The Valley After Dark. Find the hidden gems and main stages.'
    },
    CHILL: {
      outsideBg: 'bg-[#431407]',
      accent: 'text-[#FF7E5F]',
      glow: 'shadow-[#FF7E5F]/30',
      visual: 'url("https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&q=80&w=2000")',
      description: 'Sunset Sessions. Coastal vibes and laid-back SEQ events.'
    }
  };

  const current = themes[vibe];

  const fetchEvents = async (selectedVibe: Vibe, selectedLocation: Location) => {
    setLoading(true);
    try {
      const res = await fetch(`/api/events?vibe=${selectedVibe}&location=${selectedLocation}`);
      const data = await res.json();
      setEvents(data.events || []);
    } catch (error) {
      console.error('Failed to fetch events', error);
    } finally {
      setLoading(false);
    }
  };

  const handleLocationSelect = (loc: Location) => {
    setLocation(loc);
    fetchEvents(vibe, loc);
    setTimeout(() => setShowEvents(true), 300);
  };

  return (
    <main className={`min-h-[200vh] transition-all duration-1000 ease-in-out flex flex-col items-center justify-start font-sans relative ${current.outsideBg}`}>
      
      {/* Atmosphere Layer */}
      <div 
        className="fixed inset-0 z-0 transition-all duration-1000 opacity-60"
        style={{ 
          backgroundImage: current.visual,
          backgroundSize: 'cover',
          backgroundPosition: 'center',
          filter: 'brightness(0.3) contrast(1.1)'
        }}
      />

      {/* Handset Frame */}
      <div className="relative z-10 w-full md:max-w-[1200px] mt-8 flex flex-col items-center">
        
        {/* Physical Bezel */}
        <div className={`absolute -inset-x-2 -top-2 h-full hidden md:block border-[16px] border-slate-100 rounded-t-[6rem] pointer-events-none shadow-[0_0_80px_rgba(0,0,0,0.5)] ${current.glow} z-50`}>
          <div className="absolute top-48 -left-5 w-1.5 h-20 bg-slate-200 rounded-l-md" />
          <div className="absolute top-72 -left-5 w-1.5 h-20 bg-slate-200 rounded-l-md" />
          <div className="absolute top-60 -right-5 w-1.5 h-32 bg-slate-200 rounded-r-md" />
        </div>

        {/* Digital Screen */}
        <div className="relative w-full bg-black/95 min-h-screen rounded-t-[5rem] border-t border-x border-white/10 flex flex-col overflow-hidden shadow-2xl text-xs md:text-sm">
          
          {/* NAVIGATION HUD */}
          <div className="h-24 px-6 md:px-10 flex items-center justify-center border-b border-white/5 bg-black/40 backdrop-blur-xl relative z-[60]">
             <div className="flex gap-4 md:gap-10">
                {(['DEFAULT', 'SPORTS', 'MUSIC', 'CHILL'] as Vibe[]).map((v) => (
                  <button key={v} onClick={() => setVibe(v)} className={`text-[10px] md:text-[12px] font-black uppercase tracking-widest transition-all ${vibe === v ? 'text-white underline underline-offset-[12px] decoration-2' : 'text-white/20 hover:text-white'}`}>
                    {v}
                  </button>
                ))}
             </div>
             <div className="absolute right-6 md:right-12 text-white/40 hover:text-white cursor-pointer transition-colors p-2 md:p-2.5 bg-white/5 rounded-xl border border-white/10">
                <Menu className="w-6 h-6 md:w-8 md:h-8" />
             </div>
          </div>

          <div className="flex-1 relative">
            
            {/* SELECTION LANDING */}
            <div className={`h-[85vh] flex flex-col items-center justify-between p-6 md:p-16 transition-all duration-700 ${showEvents ? 'opacity-0 -translate-y-full absolute inset-x-0' : 'opacity-100'}`}>
              <div className="flex flex-col items-center w-full mt-10">
                <div className={`inline-block px-4 py-1 rounded-full border mb-8 bg-white/5 ${current.accent.replace('text', 'border')}`}>
                  <span className={`text-[10px] font-black uppercase tracking-widest ${current.accent}`}>Vibe: {vibe}</span>
                </div>
                <h1 className="text-[14vw] md:text-[10rem] font-black tracking-tighter italic uppercase text-center leading-[0.8] mb-10 select-none whitespace-nowrap">
                  jOY <span className={`transition-colors duration-1000 ${current.accent}`}>EVENTS</span>
                </h1>
                <p className="text-base md:text-2xl font-bold tracking-tight opacity-70 max-w-lg mx-auto leading-tight text-center text-slate-300">{current.description}</p>
              </div>

              <div className="w-full grid grid-cols-3 gap-2 md:gap-4 mb-10">
                {[{ id: 'BRISBANE', label: 'Brisbane' }, { id: 'GC', label: 'Gold Coast' }, { id: 'SC', label: 'Sunshine' }].map(loc => (
                  <button key={loc.id} onClick={() => handleLocationSelect(loc.id as Location)} className="bg-slate-900/60 border border-white/5 p-4 md:p-8 rounded-2xl md:rounded-[2.5rem] flex flex-col items-center gap-4 transition-all duration-300 hover:bg-slate-800 hover:border-white/10 active:scale-[0.98] group">
                    <div className="text-xl md:text-3xl opacity-60 group-hover:scale-110 transition-all">📍</div>
                    <span className="font-black text-[9px] md:text-[10px] uppercase tracking-[0.2em] text-slate-400 group-hover:text-white transition-colors text-center">{loc.label}</span>
                  </button>
                ))}
              </div>
            </div>

            {/* EVENT FEED */}
            <div className={`transition-all duration-1000 ${showEvents ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-20 h-0 overflow-hidden'}`}>
               
               {/* Hero Banner (Real event based) */}
               {events.length > 0 && (
                 <div className="relative h-[300px] md:h-[450px] w-full overflow-hidden border-b border-white/10">
                   <div 
                    className="absolute inset-0 bg-cover bg-center transition-transform duration-1000 scale-105" 
                    style={{ backgroundImage: `url(${events[0].hero})` }}
                   />
                   <div className="absolute inset-0 bg-gradient-to-r from-black via-black/50 to-transparent" />
                   <div className="relative h-full flex flex-col justify-center p-8 md:p-20 max-w-3xl">
                      <div className="bg-red-600 text-[9px] md:text-[10px] font-black uppercase px-2 py-1 inline-block w-fit mb-4 tracking-widest animate-pulse">Featured Event</div>
                      <h2 className="text-4xl md:text-7xl font-black italic uppercase tracking-tighter leading-[0.85] mb-6">{events[0].title}</h2>
                      <p className={`text-xs md:text-base font-bold uppercase tracking-widest ${current.accent}`}>{events[0].date} • {events[0].venue}</p>
                   </div>
                 </div>
               )}

               {/* Poster Feed */}
               <div className="p-6 md:p-12 space-y-12">
                  <div className="flex items-center justify-between border-b border-white/10 pb-6">
                    <h2 className="text-xl md:text-3xl font-black italic uppercase tracking-tighter">
                      Live Pulse: {location} <span className={current.accent}>{vibe}</span>
                    </h2>
                    <button onClick={() => setShowEvents(false)} className="text-[10px] uppercase font-black text-slate-500 hover:text-white underline underline-offset-4 transition-colors">Reset</button>
                  </div>

                  {loading ? (
                    <div className="h-64 flex flex-col items-center justify-center gap-4 text-slate-500 font-bold uppercase tracking-[0.3em] text-[10px]">
                      <Loader2 className="w-8 h-8 animate-spin text-blue-500" />
                      Harvesting live events...
                    </div>
                  ) : (
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6 md:gap-10 pb-40">
                      {events.slice(1).map(event => (
                        <div key={event.id} className="bg-white rounded-3xl overflow-hidden flex flex-col group cursor-pointer border border-white/5 shadow-2xl transition-all duration-300 hover:translate-y-[-6px]">
                          <div className="h-48 md:h-72 bg-slate-800 relative overflow-hidden">
                             <div 
                              className="absolute inset-0 bg-cover bg-center transition-transform duration-700 group-hover:scale-110" 
                              style={{ backgroundImage: `url(${event.hero})` }}
                             />
                             <div className="absolute top-4 left-4 bg-black/90 p-2 text-[8px] font-black text-white uppercase tracking-widest border border-white/10">jOY Verified</div>
                          </div>
                          <div className="p-6 md:p-10 bg-white flex flex-col gap-5">
                             <h3 className="text-black text-xl md:text-3xl font-black leading-[0.9] uppercase italic tracking-tighter">{event.title}</h3>
                             <div className="text-slate-500 text-[10px] md:text-xs font-bold space-y-1 uppercase tracking-tight md:tracking-tighter">
                                <p>{event.date}</p>
                                <p className="truncate">{event.venue}</p>
                             </div>
                             <a 
                              href={event.link} 
                              target="_blank" 
                              rel="noopener noreferrer"
                              className="bg-[#2a4d2e] hover:bg-black text-white py-3 md:py-4 rounded-xl text-[9px] md:text-[10px] font-black uppercase tracking-[0.2em] transition-all text-center"
                             >
                              Find Tickets
                             </a>
                          </div>
                        </div>
                      ))}
                    </div>
                  )}
               </div>
            </div>

          </div>
        </div>
      </div>
    </main>
  );
}
