"use client"
import React, { useEffect, useState, useRef } from 'react'
import Hero from '../components/Hero'
import LiveScoreboard from '../components/LiveScoreboard'
import TerminalConsole from '../components/TerminalConsole'
import SuspicionMeter from '../components/SuspicionMeter'
import StartButton from '../components/StartButton'
import { fetchLiveData } from '../lib/fetchLiveData'

export default function Page() {
  const [live, setLive] = useState<any>(null)
  const [script, setScript] = useState('')
  const [enabled, setEnabled] = useState(false)
  const [odds, setOdds] = useState<string[]>([])
  const [trends, setTrends] = useState<string[]>([])
  const intervalRef = useRef<number | null>(null)

  useEffect(() => {
    async function load() {
      const d = await fetchLiveData()
      setLive(d)
    }
    load()
  }, [])

  useEffect(() => {
    if (!enabled) return
    // immediate trigger then interval
    callGenerate()
    intervalRef.current = window.setInterval(callGenerate, 20000)
    return () => { if (intervalRef.current) clearInterval(intervalRef.current) }
  }, [enabled])

  async function callGenerate() {
    // fake odds and trends
    const o = [`Odds on Team A crashed ${Math.floor(Math.random()*500)+50}%`, `Betting bot detected shifting lines`]
    const t = [`#UmpirePaidOff trending`, `#ScriptedIPL spikes`]
    setOdds(o)
    setTrends(t)
    try {
      const res = await fetch('/api/generate-script')
      const json = await res.json()
      setScript(json.script)
      // TTS
      if (enabled && typeof window !== 'undefined' && window.speechSynthesis) {
        const utter = new SpeechSynthesisUtterance(json.script)
        // pick a deep-ish voice if available
        const voices = window.speechSynthesis.getVoices()
        const candidate = voices.find(v => /deep|Alex|Daniel|Google UK|Microsoft/i.test(v.name))
        if (candidate) utter.voice = candidate
        utter.rate = 0.95
        window.speechSynthesis.cancel()
        window.speechSynthesis.speak(utter)
      }
    } catch (err) {
      setScript('Error generating script')
    }
  }

  return (
    <main className="grid grid-cols-12 gap-4">
      <div className="col-span-12">
        <Hero />
      </div>

      <div className="col-span-3">
        <LiveScoreboard data={live} />
        <div className="mt-4">
          <StartButton enabled={enabled} onClick={() => setEnabled(e => !e)} />
        </div>
      </div>

      <div className="col-span-6">
        <TerminalConsole text={script || 'Awaiting conspiracy…'} />
      </div>

      <div className="col-span-3">
        <SuspicionMeter odds={odds} trends={trends} />
      </div>
    </main>
  )
}
