import { GoogleGenerativeAI } from '@google/generative-ai'
import { NextResponse } from 'next/server'
import fs from 'fs'
import path from 'path'
import { fetchLiveData } from '../../../lib/fetchLiveData'

const CONTEXT_PATH = path.resolve(process.cwd(), './scriptwriters-revenge/lib/context.json')
const TW_PATH = path.resolve(process.cwd(), './scriptwriters-revenge/tw.json')

function pickRandom(arr:any[]) { return arr[Math.floor(Math.random()*arr.length)] }

async function generateMockScript(tropes:any[], live:any, odds:string[], trends:string[], reactions:string[]) {
  const trope = pickRandom(tropes || ["Unknown script"])
  const style = pickRandom(["tabloid-screamer","conspiratorial-whisper","breathless-breakdown"])
  return `SYSTEM BULLETIN: ${trope}. Score ${live.live_data.score.runs}/${live.live_data.score.wickets} at ${live.live_data.score.overs} overs. ${odds[0]}. Trend: ${trends[0]}.\n\nPredicted 3-over script:\n1) Ball 1-6: Fielders act strangely; baited no-balls and boundaries timed.\n2) Ball 7-12: Wicket falls as planned; commentator gasps but cut feed.\n3) Ball 13-18: Final over, mysterious run-out; scoreboard flashes and odds correct the lie.\n\nFan reactions sample: ${reactions.join(' / ')}\n\nTone: ${style}. Keep it punchy, dramatic, and read-ready.`
}

function sampleArray<T>(arr:T[], n=3){
  const copy = Array.from(arr||[])
  const out:T[] = []
  while(out.length < n && copy.length) {
    const i = Math.floor(Math.random()*copy.length)
    out.push(copy.splice(i,1)[0])
  }
  return out
}

function buildPrompt(tropes:string[], live:any, odds:string[], trends:string[], reactions:string[]) {
  const system = `You are a deranged, dramatic sports conspiracy theorist. Based on the current score and these suspicious betting/Twitter trends, generate a highly dramatic, brutal, and 'heinous' 3-over script predicting exactly how the next 18 balls are rigged to play out. Make it sound like an absolute madman uncovering a massive scandal. Keep it concise, punchy, and formatted for a text-to-speech engine. Avoid actual threats or physical violence; focus on sports-rigging, manipulation, and broadcast tampering. Keep each ball prediction short (1-2 sentences). Include a 1-line headline and a 2-3 sentence closing hook describing how odds and trends will react. Use simple sentences for TTS clarity.`

  const user = `Tropes: ${tropes.join('; ')}\nLive Score: ${live.live_data.score.runs}/${live.live_data.score.wickets} at ${live.live_data.score.overs} overs. Recent: ${live.live_data.recent_overs.join(', ')}. Batter: ${live.live_data.current_batter}. Bowler: ${live.live_data.current_bowler}.\nOdds samples: ${odds.join(' | ')}\nTwitter samples: ${trends.join(' | ')}\nFan reactions sample: ${reactions.join(' | ')}\n\nProduce: 3-over, 18-ball sequence with a 1-line headline, numbered ball outcomes (1-18), and a 2-3 sentence closing hook. Output plain text, TTS-friendly.`

  return { system, user }
}

export async function GET() {
  // read tropes and twitter reactions
  let tropes: string[] = []
  let reactions: string[] = []
  try {
    const raw = fs.readFileSync(CONTEXT_PATH, 'utf8')
    const ctx = JSON.parse(raw)
    tropes = ctx.conspiracy_tropes || []
  } catch (e) {
    tropes = ["Unknown script"]
  }

  try {
    const rawTw = fs.readFileSync(TW_PATH, 'utf8')
    const tw = JSON.parse(rawTw)
    reactions = tw.fan_reactions || []
  } catch (e) {
    reactions = []
  }

  const live = await fetchLiveData()
  const odds = [`Odds on Team A crashed ${Math.floor(Math.random()*400)+50}% in dark markets`, `Insider bot flipped lines`]
  const trends = sampleArray(reactions.map(r => r.match(/#\w+/)?.[0]).filter(Boolean) as string[], 2)
  const sampleReactions = sampleArray(reactions, 4)

  const { system, user } = buildPrompt(tropes, live, odds, trends.length ? trends : ['#ScriptedIPL'], sampleReactions)

  // Attempt to call Gemini (if key provided) otherwise fallback to mock
  if (process.env.GENERATIVE_AI_API_KEY) {
    try {
      const genAI = new GoogleGenerativeAI(process.env.GENERATIVE_AI_API_KEY);
      const model = genAI.getGenerativeModel({ model: "gemini-2.5-flash" });
      const prompt = `${system}\n\n${user}`;
      const result = await model.generateContent(prompt);
      const responseText = result.response.text();

      if (responseText && responseText.length > 10) {
        return NextResponse.json({ script: responseText })
      }
    } catch (err) {
      console.error("Gemini API Error:", err);
      // continue to mock
    }
  }

  const mock = await generateMockScript(tropes, live, odds, trends.length ? trends : ['#ScriptedIPL'], sampleReactions)
  return NextResponse.json({ script: mock })
}
