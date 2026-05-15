# The Scriptwriter's Revenge — UI scaffold

This folder contains a Next.js 14 (App Router) scaffold with Tailwind styling and components for the "Scriptwriter's Revenge" retro UI.

Quick start (from this folder):

```bash
npm install
npm run dev
```

Environment:
- Set `GENERATIVE_AI_API_KEY` to use the @google/generative-ai SDK; otherwise the API route returns a mock script.

Copy `.env.example` to `.env.local` and set `GENERATIVE_AI_API_KEY` with your Gemini API key. Do NOT commit `.env.local` — it's ignored by `.gitignore`.

Example:

```bash
cp .env.example .env.local
# edit .env.local and paste your key
```

Firebase deployment (summary)
----------------------------

This project can be deployed to Firebase Hosting + Cloud Functions. The repository includes a `next.config.js` that builds into `functions/.next` and a small Firebase Functions adapter at `functions/index.js`.

Quick steps (run from `scriptwriters-revenge`):

1. Install dependencies:

```bash
npm install
```

2. Install Firebase CLI and log in:

```bash
npm install -g firebase-tools
firebase login
```

3. Initialize or point to your Firebase project (if you haven't):

```bash
firebase use --add
# or set project id in .firebaserc
```

4. Build and deploy (predeploy hook will run `npm run build` from the repo root):

```bash
# from scriptwriters-revenge/
npm run build
firebase deploy --only functions,hosting
```

Notes:
- Replace `<YOUR_FIREBASE_PROJECT_ID>` in `.firebaserc` and `<YOUR_FIREBASE_SITE_ID>` in `firebase.json` with your project/site ids.
- The `firebase.json` rewrites all requests to the `nextServer` Cloud Function so SSR and API routes work.
- If you'd rather run a static export (no server/API routes), use `next export` and host the output in `hosting.public`.

If you want, I can run the local `npm run build` and validate the `functions/.next` output, then help you run `firebase deploy` (you'll need to run `firebase login` locally and provide the project id). 
