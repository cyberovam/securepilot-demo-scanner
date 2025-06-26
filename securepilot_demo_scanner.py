# securepilot-demo-scanner

This repo contains a full-stack, AI-powered Secure Code Scanner using GPT-4.

## 📁 Structure
```
securepilot-demo-scanner/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── github_client.py
│   │   ├── scanner.py
│   │   └── utils.py
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env.example
├── frontend/
│   ├── public/
│   ├── src/
│   │   └── App.js
│   ├── index.html
│   ├── tailwind.config.js
│   └── package.json
├── docker-compose.yml
└── README.md
```

---

## ✅ Features
- GitHub PR integration
- GPT-4 code chunk scanning (SAST)
- Custom scan manifest
- React frontend dashboard
- Dockerized & deployable

---

## 🚀 Quick Start (Local)
```bash
# Clone and enter repo
$ git clone https://github.com/YOUR_USERNAME/securepilot-demo-scanner.git
$ cd securepilot-demo-scanner

# Add secrets
$ cp backend/.env.example backend/.env
# Fill in OPENAI_API_KEY and GITHUB_TOKEN

# Start app
$ docker-compose up --build

# Visit frontend
http://localhost:3000
```

---

## 🔐 Environment Variables (`backend/.env.example`)
```
OPENAI_API_KEY=sk-...
GITHUB_TOKEN=ghp-...
```

---

## 🖥️ Live Deployment (Render.com)
1. Fork this repo
2. Deploy `backend/` as Web Service
3. Deploy `frontend/` as Static Site
4. Add environment variables to backend
5. You’re done 🎉

---

## 🧠 Backend: `main.py`
```python
from fastapi import FastAPI, HTTPException
from app.github_client import fetch_pr_files
from app.scanner import scan_with_openai

app = FastAPI()

@app.get("/scan-pr")
def scan_pr(repo: str, pr_number: int):
    try:
        files = fetch_pr_files(repo, pr_number)
        results = []
        for f in files:
            if f['filename'].endswith(('.py', '.js', '.ts', '.go', '.java')):
                result = scan_with_openai(f['patch'], f['filename'])
                results.append(result)
        return {"results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

---

## 🧠 Frontend: `App.js`
```jsx
import React, { useState } from "react";
function App() {
  const [repo, setRepo] = useState("");
  const [pr, setPr] = useState("");
  const [results, setResults] = useState(null);

  const scan = async () => {
    const res = await fetch(`/scan-pr?repo=${repo}&pr_number=${pr}`);
    const json = await res.json();
    setResults(json.results);
  };

  return (
    <div className="max-w-xl mx-auto p-4">
      <h1 className="text-2xl font-bold">SecurePilot Scanner</h1>
      <input value={repo} onChange={e => setRepo(e.target.value)} placeholder="owner/repo" className="border p-2 w-full rounded mt-4" />
      <input type="number" value={pr} onChange={e => setPr(e.target.value)} placeholder="PR #" className="border p-2 w-full rounded mt-2" />
      <button onClick={scan} className="bg-blue-600 text-white px-4 py-2 rounded mt-2">Run Scan</button>
      {results && results.map((r, i) => (
        <div key={i} className="border-b py-2">
          <strong>{r.file}</strong>
          <pre className="bg-gray-100 p-2 whitespace-pre-wrap">{r.issues}</pre>
        </div>
      ))}
    </div>
  );
}
export default App;
```

---

## 🧾 License
MIT — Feel free to fork, build, and ship your own SecurePilot SaaS 💪
