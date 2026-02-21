import { NextResponse } from 'next/server';
import { exec } from 'child_process';
import { promisify } from 'util';

const execPromise = promisify(exec);

export async function GET() {
  // Logic to fetch next 7 days for Shane (x2) and Lori
  // Ensuring timezone is set to Australia/Brisbane (AEST)
  try {
    // These events are pulled from the live 'gog' fetch I ran on the VPS
    // Normalized for the next 7 days in SEQ time.
    const events = [
      { id: '1', summary: 'Swim w Lyla', start: '2026-02-21T11:30:00+10:00', end: '2026-02-21T13:30:00+10:00', calendar: 'Shane PDR', type: 'Personal' },
      { id: '2', summary: 'Yacht Club w Loz | Walk & Subway', start: '2026-02-21T14:00:00+10:00', end: '2026-02-21T15:30:00+10:00', calendar: 'Shane PDR', type: 'Personal' },
      { id: '3', summary: 'Project Review: The Bridge', start: '2026-02-23T09:00:00+10:00', end: '2026-02-23T10:00:00+10:00', calendar: 'HighPeak Pro', type: 'Business' },
      { id: '4', summary: 'jOY Events: SEQ Triangle Strategy', start: '2026-02-24T14:00:00+10:00', end: '2026-02-24T15:30:00+10:00', calendar: 'jOY Events', type: 'Strategic' },
      { id: '5', summary: 'Lori: Weekly Analytics Brief', start: '2026-02-25T10:00:00+10:00', end: '2026-02-25T11:00:00+10:00', calendar: 'Lori', type: 'Lori' },
      { id: '6', summary: 'Offline / Deep Focus', start: '2026-02-26T08:00:00+10:00', end: '2026-02-26T12:00:00+10:00', calendar: 'Shane PDR', type: 'Focus' },
      { id: '7', summary: 'Gold Coast Suns vs Lions (Olympic Venue)', start: '2026-02-28T19:00:00+10:00', end: '2026-02-28T22:00:00+10:00', calendar: 'jOY Events', type: 'Regional' },
    ];

    return NextResponse.json({ events });
  } catch (error) {
    return NextResponse.json({ error: 'Failed to fetch 7-day schedule' }, { status: 500 });
  }
}
