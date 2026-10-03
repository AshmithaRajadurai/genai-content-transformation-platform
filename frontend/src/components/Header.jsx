import { SparklesIcon } from './Icons';

export default function Header() {
  return (
    <header className="header-container">
      <div className="header-badge-row">
        <span className="platform-tag">
          <SparklesIcon className="icon-tiny" />
          <span>GenAI Platform v0.1</span>
        </span>
        <div className="system-status-pills">
          <span className="status-pill status-ready" title="Backend: FastAPI (Port 8000)">
            <span className="dot dot-green"></span>
            FastAPI Backend
          </span>
          <span className="status-pill status-ready" title="Database: MongoDB 8 (Docker container: genai-mongodb)">
            <span className="dot dot-green"></span>
            MongoDB 8
          </span>
          <span className="status-pill status-ready" title="Frontend: React 19 + Vite">
            <span className="dot dot-green"></span>
            React + Vite
          </span>
        </div>
      </div>

      <div className="header-title-block">
        <h1 className="header-title">GenAI Content Transformation Platform</h1>
        <p className="header-description">
          Synthesize and transform any source information — articles, research reports, security advisories, or raw prompts — into high-impact multi-channel formats powered by Generative AI.
        </p>
      </div>
    </header>
  );
}
