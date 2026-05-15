import '../styles/globals.css'
import { Press_Start_2P } from 'next/font/google'
import React from 'react'

const press = Press_Start_2P({ subsets: ['latin'], weight: '400', display: 'swap' })

export const metadata = {
  title: "The Scriptwriter's Revenge",
  description: 'Retro conspiracy generator for IPL matches.'
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className={`${press.className} bg-arcadeBg text-neonYellow min-h-screen` }>
        <div className="min-h-screen p-6 crt-frame scanlines">
          <header className="flex items-center gap-4 mb-6">
            <div className="text-4xl text-neonGreen drop-shadow-glow-green">▣</div>
            <div>
              <div className="text-3xl text-white drop-shadow-glow-pink">THE SCRIPTWRITER'S</div>
              <div className="text-2xl text-neonGreen">REVENGE</div>
            </div>
            <div className="ml-auto text-sm text-white/60">Retro GBA • Live Conspiracy</div>
          </header>
          {children}
        </div>
      </body>
    </html>
  )
}
