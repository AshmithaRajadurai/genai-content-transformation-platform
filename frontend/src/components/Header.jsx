import { SparklesIcon, DatabaseIcon } from './Icons';

export default function Header({ onOpenHistory }) {
  return (
    <header className="header-container">
      <div className="header-badge-row">
        <span className="platform-tag">
          <SparklesIcon className="icon-tiny" />
          <span>GenAI Platform v0.3</span>
        </span>
        <div className="system-status-pills">
          <span className="status-pill status-ready" title="Backend: FastAPI (Port 8000)">
            <span className="dot dot-green"></span>
            FastAPI Backend
          </span>
          <button
            type="button"
            className="status-pill status-ready"
            onClick={onOpenHistory}
            style={{ cursor: 'pointer', background: 'none', border: '1px solid rgba(16, 185, 129, 0.3)' }}
            title="Storage: MongoDB Atlas Cloud (Click to view saved history)"
          >
            <span className="dot dot-green"></span>
            MongoDB Atlas Cloud
          </button>
          <span className="status-pill status-ready" title="Frontend: React 19 + Vite">
            <span className="dot dot-green"></span>
            React + Vite
          </span>
          {onOpenHistory && (
            <button
              type="button"
              className="btn-history-trigger"
              onClick={onOpenHistory}
              title="Open Transformation History Archive"
            >
              <DatabaseIcon className="w-3.5 h-3.5" />
              <span>History Archive</span>
            </button>
          )}
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
