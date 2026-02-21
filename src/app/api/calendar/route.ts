import { NextResponse } from 'next/server';

export async function GET() {
  // Analytical Logic: Returning KLOR's active automated routines and scheduled project tasks.
  // This feed drives the 'Scheduled Tasks' view on The Bridge.
  try {
    const routines = [
      { id: 'r1', summary: 'Mission Control Check', start: '2026-02-22T08:00:00+10:00', type: 'System', frequency: 'Every 30 min', next_run: 'In 12 min' },
      { id: 'r2', summary: 'SEQ Triangle Data Harvest', start: '2026-02-22T05:00:00+10:00', type: 'Data', frequency: 'Daily', next_run: 'Completed' },
      { id: 'r3', summary: 'Morning Analytical Brief', start: '2026-02-22T07:30:00+10:00', type: 'Communication', frequency: 'Daily', next_run: 'Completed' },
      { id: 'r4', summary: 'Social Pulse: Hype Meter Sync', start: '2026-02-22T10:00:00+10:00', type: 'jOY', frequency: 'Every 4 hours', next_run: 'In 4 hours' },
      { id: 'r5', summary: 'Vibe Forecast Generator', start: '2026-02-23T16:00:00+10:00', type: 'Content', frequency: 'Weekly', next_run: 'In 1 day' },
      { id: 'r6', summary: 'High Peek Pro Client Sync', start: '2026-02-24T09:00:00+10:00', type: 'CRM', frequency: 'Weekly', next_run: 'In 2 days' },
      { id: 'r7', summary: 'Olympic Venue Status Audit', start: '2026-02-26T11:00:00+10:00', type: 'Strategic', frequency: 'Weekly', next_run: 'In 4 days' },
    ];

    return NextResponse.json({ routines });
  } catch (error) {
    return NextResponse.json({ error: 'Failed to fetch automated routines' }, { status: 500 });
  }
}
