import React from 'react'

export default function SuspicionMeter({ odds, trends }: { odds: string[], trends: string[] }) {
  return (
    <div className="pixel-border p-4 bg-black/60 text-white">
      <h3 className="text-hotPink">Suspicion Meter</h3>
      <div className="mt-2">
        <div className="text-sm">Odds Shifts</div>
        <ul className="text-xs list-disc ml-4 text-neonYellow">
          {odds.map((o, i) => <li key={i}>{o}</li>)}
        </ul>
        <div className="mt-2 text-sm">Twitter Trends</div>
        <ul className="text-xs list-disc ml-4 text-white/80">
          {trends.map((t, i) => <li key={i}>{t}</li>)}
        </ul>
      </div>
    </div>
  )
}
