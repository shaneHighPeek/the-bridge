import { NextResponse } from 'next/server';
import fs from 'fs';
import path from 'path';

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const vibe = searchParams.get('vibe') || 'DEFAULT';
  const locationParam = searchParams.get('location') || 'BRISBANE';

  try {
    // 1. Resolve path to the harvested data from "The Vacuum"
    // Using process.cwd() as /data/.openclaw/workspace/joy-events-app
    const dataPath = path.join(process.cwd(), '..', 'joy-events', 'data', 'events.json');
    
    if (fs.existsSync(dataPath)) {
      const fileData = fs.readFileSync(dataPath, 'utf8');
      const harvestedEvents = JSON.parse(fileData);

      // 2. Map harvested data to the frontend schema
      const mappedEvents = harvestedEvents
        .filter((e: any) => {
          // Normalise location strings for filtering
          const venue = (e.venue || '').toUpperCase();
          const source = (e.source || '').toUpperCase();
          
          if (locationParam === 'BRISBANE') {
            return venue.includes('BRISBANE') || source.includes('BCC') || venue.includes('MOUNT GRAVATT');
          }
          if (locationParam === 'GC') {
            return venue.includes('GOLD COAST') || venue.includes('HOTA') || venue.includes('SURFERS PARADISE') || source.includes('GCCC');
          }
          return true;
        })
        .map((e: any, index: number) => ({
          id: `h-${index}`,
          title: e.title,
          date: e.date || 'Live Now',
          venue: e.venue,
          hero: e.hero || getPlaceholderImage(vibe),
          link: e.link || '#'
        }));

      if (mappedEvents.length > 0) {
        return NextResponse.json({ events: mappedEvents });
      }
    }
  } catch (error) {
    console.error('Error reading harvested events:', error);
  }

  return NextResponse.json({ events: getFallbackData(vibe) });
}

function getPlaceholderImage(vibe: string) {
  const images: any = {
    SPORTS: 'https://images.unsplash.com/photo-1540747913346-19e32dc3e97e?auto=format&fit=crop&q=80&w=2000',
    MUSIC: 'https://images.unsplash.com/photo-1470225620780-dba8ba36b745?auto=format&fit=crop&q=80&w=2000',
    CHILL: 'https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&q=80&w=2000',
    DEFAULT: 'https://images.unsplash.com/photo-1518173946687-a4c8a9ba332f?auto=format&fit=crop&q=80&w=2000'
  };
  return images[vibe] || images.DEFAULT;
}

function getFallbackData(vibe: string) {
  const fallbacks: any = {
    SPORTS: [{ id: 's1', title: 'Brisbane Broncos vs Sydney Roosters', date: 'Fri 14 Mar 2026', venue: 'Suncorp Stadium', hero: getPlaceholderImage('SPORTS'), link: '#' }],
    MUSIC: [{ id: 'm1', title: 'RÜFÜS DU SOL: World Tour', date: 'Thu 20 Mar 2026', venue: 'Riverstage', hero: getPlaceholderImage('MUSIC'), link: '#' }],
    CHILL: [{ id: 'c1', title: 'Burleigh Pavilion Sunday Session', date: 'Sun Every Week', venue: 'Burleigh Pavilion', hero: getPlaceholderImage('CHILL'), link: '#' }],
    DEFAULT: [{ id: 'd1', title: 'Brisbane City Markets', date: 'Wed Every Week', venue: 'Reddacliff Place', hero: getPlaceholderImage('DEFAULT'), link: '#' }]
  };
  return fallbacks[vibe] || fallbacks.DEFAULT;
}
