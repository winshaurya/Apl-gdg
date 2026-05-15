import { NextResponse } from 'next/server'
import fs from 'fs'
import path from 'path'
import { fetchLiveData } from '../../../lib/fetchLiveData'

const CONTEXT_PATH = path.resolve(process.cwd(), './scriptwriters-revenge/lib/context.json')

function pickRandom(arr:any[]) { return arr[Math.floor(Math.random()*arr.length)] }

async function generateMockScript(tropes:any[], live:any, odds:string[], trends:string[]) {
  const trope = pickRandom(tropes)
  const style = pickRandom(["tabloid-screamer","conspiratorial-whisper","breathless-breakdown"])
  return `SYSTEM BULLETIN: ${trope}. Score ${live.live_data.score.runs}/${live.live_data.score.wickets} at ${live.live_data.score.overs} overs. ${odds[0]}. Trend: ${trends[0]}.\n\nPredicted 3-over script:\n1) Ball 1-6: Fielders act strangely; baited no-balls and boundaries timed.\n2) Ball 7-12: Wicket falls as planned; commentator gasps but cut feed.\n3) Ball 13-18: Final over, mysterious run-out; scoreboard flashes and odds correct the lie.\n\nTone: ${style}. Keep it punchy, dramatic, and read-ready.`
}

export async function GET() {
  // read tropes
  let tropes = []
  try {
    const raw = fs.readFileSync(CONTEXT_PATH, 'utf8')
    const ctx = JSON.parse(raw)
    tropes = ctx.conspiracy_tropes || []
  } catch (e) {
    tropes = ["Unknown script"]
  }

  const live = await fetchLiveData()
  const odds = [`Odds on Team A crashed ${Math.floor(Math.random()*400)+50}% in dark markets`, `Insider bot flipped lines`]
  const trends = ['#UmpirePaidOff', '#ScriptedIPL']

  // If API key provided, attempt real Gemini call (pseudo-code)
  if (process.env.GENERATIVE_AI_API_KEY) {
    try {
      // NOTE: SDK usage may vary. This is a placeholder for a real call.
      const {TextGenerationModel} = await import('@google/generative-ai')
      const model = new TextGenerationModel({ apiKey: process.env.GENERATIVE_AI_API_KEY })
      const system = `You are a deranged, dramatic sports conspiracy theorist. Based on the current score and these suspicious betting/Twitter trends, generate a highly dramatic, brutal, and 'heinous' 3-over script predicting exactly how the next 18 balls are rigged to play out. Make it sound like an absolute madman uncovering a massive scandal. Keep it concise, punchy, and formatted for a text-to-speech engine. Avoid actual violence, focus entirely on intense sports-rigging drama.`
      const prompt = `${system}\nTropes: ${tropes.join(', ')}\nLive: runs ${live.live_data.score.runs} wickets ${live.live_data.score.wickets} overs ${live.live_data.score.overs}\nOdds: ${odds.join(' | ')}\nTrends: ${trends.join(' | ')}`
      const response = await model.generate({ prompt })
      const script = response?.text || (await generateMockScript(tropes, live, odds, trends))
      return NextResponse.json({ script })
    } catch (err) {
      const script = await generateMockScript(tropes, live, odds, trends)
      return NextResponse.json({ script })
    }
  }

  const script = await generateMockScript(tropes, live, odds, trends)
  return NextResponse.json({ script })
}
