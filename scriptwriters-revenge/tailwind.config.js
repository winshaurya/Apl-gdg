/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './app/**/*.{js,ts,jsx,tsx}',
    './components/**/*.{js,ts,jsx,tsx}',
  ],
  theme: {
    extend: {
      colors: {
        arcadeBg: '#0b0f0a',
        neonGreen: '#7CFC00',
        hotPink: '#FF5DA2',
        neonYellow: '#FFF200',
        crtTint: 'rgba(0,0,0,0.35)'
      },
      boxShadow: {
        'glow-green': '0 0 12px rgba(124,252,0,0.35)',
        'glow-pink': '0 0 12px rgba(255,93,162,0.35)'
      }
    }
  },
  plugins: []
}
