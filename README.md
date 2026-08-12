# 🎙️ المساعد الصوتي العربي (Arabic Voice Chatbot)

A voice-based chatbot that listens to Arabic speech, sends it to Cohere's
`command-a-03-2025` model for a response, and speaks the reply back out loud.

**Stack:**
- **Backend:** Python + Flask — talks to the Cohere API, keeps conversation history
- **Frontend:** HTML + JavaScript — captures your mic input and speaks replies using
  the browser's built-in Web Speech API (no audio libraries needed)

---

## Requirements

- Python 3.9–3.11 recommended
- Google Chrome (for speech recognition — other browsers have limited/no support)
- A [Cohere API key](https://dashboard.cohere.com/api-keys)

---

## Project structure

```
rootFolder/
├── app.py
├── .env
└── templates/
    └── index.html
```

---

## Setup

1. **Create and activate a virtual environment**
   ```bash
   python -m venv venv
   ```
   - Windows: `venv\Scripts\activate`
   - Mac/Linux: `source venv/bin/activate`

2. **Install dependencies**
   ```bash
   pip install flask cohere python-dotenv
   ```

3. **Add your Cohere API key**

   Create a `.env` file in the project root:
   ```
   COHERE_API_KEY=your_key_here
   ```

4. **Run the server**
   ```bash
   python app.py
   ```

5. **Open the app**

   Go to [http://127.0.0.1:5000](http://127.0.0.1:5000) in Chrome.

---

## How to use it

1. Click the 🎤 microphone button.
2. Speak in Arabic.
3. The app transcribes your speech, sends it to Cohere, and shows + speaks the reply.
4. Click **مسح المحادثة** (Clear conversation) to reset the chat history.

---

## Notes

- **Conversation history is in-memory** — it resets every time you restart `app.py`.
- **Arabic TTS voice quality** depends on the voices installed on your OS.
  If replies sound off or use an English-accented voice, install an Arabic voice pack:
  - Windows: Settings → Time & Language → Speech → Add a voice
  - Mac: System Settings → Accessibility → Spoken Content → System Voice
- **Your Cohere API key stays server-side** — the browser never sees it, since all
  API calls go through the Flask backend.

---

## Troubleshooting

| Symptom | Likely cause |
|---|---|
| "Failed to fetch" in browser | Flask isn't running, wrong URL, or a browser extension/antivirus blocking local requests. Try Incognito mode. |
| `WinError 10054` in terminal | Antivirus/firewall (e.g. McAfee) resetting outbound HTTPS connections. The app auto-retries a few times to work around this. |
| Garbled `<PAD>` text in replies | Was caused by an unstable model — fixed by switching to `command-a-03-2025`. |
| No Arabic voice / robotic English accent | Install an Arabic voice pack on your OS (see Notes above). |
