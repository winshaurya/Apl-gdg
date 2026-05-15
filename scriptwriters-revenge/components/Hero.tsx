import React from 'react'

export default function Hero() {
  return (
    <section className="pixel-border p-6 rounded-md bg-black/60 mb-6 relative overflow-hidden">
      <div className="badge inline-block bg-hotPink text-white px-3 py-1 rounded shadow-glow-pink mb-2 text-xs uppercase tracking-wider">LIVE CONSPIRACY GENERATOR</div>
      <h1 className="text-5xl text-neonGreen drop-shadow-glow-green mt-2">THE SCRIPTWRITER'S REVENGE</h1>
      <p className="text-sm text-white/80 mt-2 max-w-2xl">Fans joke that IPL matches are scripted. This generator blends live match data, fake odds shifts, and Twitter drama to produce an over-the-top conspiracy script — read aloud in a warped, retro-arcade announcer voice.</p>

      <div className="grid grid-cols-3 gap-4 mt-6">
        <div className="p-3 bg-black/40 pixel-border crt-frame"> <strong className="text-neonGreen">Live Data Ingestion</strong><div className="text-xs text-white/70">Simulated match feed & live hooks</div></div>
        <div className="p-3 bg-black/40 pixel-border crt-frame"> <strong className="text-hotPink">Gemini AI Scripting</strong><div className="text-xs text-white/70">Engineered prompts for punchy drama</div></div>
        <div className="p-3 bg-black/40 pixel-border crt-frame"> <strong className="text-neonYellow">TTS Broadcasting</strong><div className="text-xs text-white/70">Browser speech synthesis with deep voices</div></div>
      </div>
    </section>
  )
}
