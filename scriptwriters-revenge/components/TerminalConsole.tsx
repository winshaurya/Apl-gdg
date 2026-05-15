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
    }, 20)
    return () => clearInterval(t)
  }, [text])

  return (
    <div className="pixel-border p-4 bg-black/80 text-white font-mono h-64 overflow-auto">
      <pre className="whitespace-pre-wrap">{display}</pre>
    </div>
  )
}
