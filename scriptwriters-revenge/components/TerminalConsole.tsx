"use client"
import React, { useEffect, useState } from 'react'

export default function TerminalConsole({ text }: { text: string }) {
  const [display, setDisplay] = useState('')

  useEffect(() => {
    let i = 0
    setDisplay('')
    const t = setInterval(() => {
      i++
      setDisplay(text.slice(0, i))
      if (i >= text.length) clearInterval(t)
    }, 18)
    return () => clearInterval(t)
  }, [text])

  return (
    <div className="pixel-border p-4 bg-black/95 text-neonGreen font-mono h-64 overflow-auto crt-frame">
      <pre className="whitespace-pre-wrap text-sm">{display}<span className="tty-cursor" /></pre>
    </div>
  )
}
