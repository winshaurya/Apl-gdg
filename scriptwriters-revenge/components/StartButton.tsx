"use client"
import React from 'react'

export default function StartButton({ enabled, onClick }: { enabled: boolean, onClick: () => void }) {
  return (
    <button onClick={onClick} className={`arcade-button pixel-border text-white font-bold text-sm px-6 py-3 ${!enabled? 'pulse':''}`}>
      {enabled ? 'SYSTEM READY (UNMUTE)' : 'START SYSTEM (UNMUTE)'}
    </button>
  )
}
