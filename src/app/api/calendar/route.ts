import { NextResponse } from 'next/server';
import { exec } from 'child_process';
import { promisify } from 'util';

const execPromise = promisify(exec);

export async function GET() {
  // This is a bridge to the 'gog' CLI running on the VPS
  // In a full production build, we would use the Google Calendar SDK directly in Next.js
  // For this high-velocity build, we are bridging the VPS intelligence to the Dashboard
  
  try {
    // For now, returning a structured mock that reflects the actual data I see in the CLI
    // I will wire this to the live CLI fetcher once the UI component is ready
    const events = [
      { id: '1', summary: 'Swim w Lyla', start: '2026-02-21T11:30:00+10:00', end: '2026-02-21T13:30:00+10:00', calendar: 'Shane PDR' },
      { id: '2', summary: 'Yacht Club w Loz | Walk & Subway', start: '2026-02-21T14:00:00+10:00', end: '2026-02-21T15:30:00+10:00', calendar: 'Shane PDR' },
      { id: '3', summary: 'Olympic Venue Site Visit', start: '2026-02-22T09:00:00+10:00', end: '2026-02-22T11:00:00+10:00', calendar: 'jOY Events' },
    ];

    return NextResponse.json({ events });
  } catch (error) {
    return NextResponse.json({ error: 'Failed to fetch calendar data' }, { status: 500 });
  }
}
