import React from 'react'

export default function LiveScoreboard({ data }: { data: any }) {
  const s = data?.live_data?.score || {}
  return (
    <div className="pixel-border p-4 bg-black/60 text-white">
      <h3 className="text-neonGreen">8-Bit Live Scoreboard</h3>
      <div className="mt-2 text-sm">
        <div>Runs: <strong className="text-neonYellow">{s.runs}</strong></div>
        <div>Wickets: <strong className="text-hotPink">{s.wickets}</strong></div>
        <div>Overs: <strong>{s.overs}</strong></div>
        <div>RR: <strong>{s.run_rate}</strong></div>
        <div className="mt-2">Batter: <strong>{data?.live_data?.current_batter}</strong></div>
        <div>Bowler: <strong>{data?.live_data?.current_bowler}</strong></div>
      </div>
    </div>
  )
}
