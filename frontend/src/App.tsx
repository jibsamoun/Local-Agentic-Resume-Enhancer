import { useState } from "react";
import { BulletInput } from "./components/BulletInput";
import { RewriteResults } from "./components/RewriteResults";
import { rewriteBullets } from "./services/api";
import type { BulletRewrite } from "./types";
import "./App.css";

function App() {
  const [results, setResults] = useState<BulletRewrite[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function handleSubmit(bullets: string[], jobDescription?: string) {
    setIsLoading(true);
    setError(null);

    try {
      const response = await rewriteBullets({
        bullets,
        job_description: jobDescription,
      });
      setResults(response.results);
    } catch (err) {
      setError("Failed to rewrite bullets. Is the backend running?");
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <div className="app">
      <header className="app-header">
        <div className="header-ornament"></div>
        <h1>Resume Bullet Enhancer</h1>
        <p className="subtitle">Transform your experience into compelling narratives</p>
      </header>

      <main className="app-main">
        <BulletInput onSubmit={handleSubmit} isLoading={isLoading} />

        {error && (
          <div className="error-banner">
            <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
              <circle cx="10" cy="10" r="9" stroke="currentColor" strokeWidth="2"/>
              <path d="M10 6v5M10 14v.5" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
            </svg>
            {error}
          </div>
        )}

        <RewriteResults results={results} />
      </main>

      <footer className="app-footer">
        <div className="footer-line"></div>
        <p>Powered by AI · Crafted for professionals</p>
      </footer>
    </div>
  );
}

export default App;