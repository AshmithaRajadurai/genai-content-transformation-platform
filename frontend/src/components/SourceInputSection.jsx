import { SAMPLE_INPUTS } from '../data/constants';

export default function SourceInputSection({ content, setContent }) {
  const wordCount = content.trim() ? content.trim().split(/\s+/).length : 0;
  const charCount = content.length;

  const handleLoadSample = (key) => {
    if (SAMPLE_INPUTS[key]) {
      setContent(SAMPLE_INPUTS[key]);
    }
  };

  const handleClear = () => {
    setContent('');
  };

  return (
    <section className="dashboard-card source-card" aria-labelledby="source-content-heading">
      <div className="card-header">
        <div className="card-header-left">
          <span className="card-step-badge">1</span>
          <div>
            <h2 id="source-content-heading" className="card-title">Source Content</h2>
            <p className="card-subtitle">Input your source document, article, incident report, or prompt</p>
          </div>
        </div>

        <div className="source-sample-actions">
          <span className="sample-label">Quick Samples:</span>
          <button
            type="button"
            className="btn-pill"
            onClick={() => handleLoadSample('advisory')}
            title="Load sample cybersecurity advisory"
          >
            Advisory
          </button>
          <button
            type="button"
            className="btn-pill"
            onClick={() => handleLoadSample('research')}
            title="Load sample executive research paper"
          >
            Research
          </button>
          {content && (
            <button
              type="button"
              className="btn-pill btn-pill-danger"
              onClick={handleClear}
              title="Clear input"
            >
              Clear
            </button>
          )}
        </div>
      </div>

      <div className="textarea-wrapper">
        <textarea
          id="source-content"
          name="sourceContent"
          value={content}
          onChange={(e) => setContent(e.target.value)}
          placeholder="Paste your article, report, prompt, advisory, or other source content here..."
          rows={9}
          className="source-textarea"
          aria-label="Source content input"
        />
      </div>

      <div className="source-footer">
        <div className="counter-stats">
          <span className="stat-item">
            <strong>{wordCount}</strong> words
          </span>
          <span className="stat-separator">•</span>
          <span className="stat-item">
            <strong>{charCount}</strong> characters
          </span>
          {wordCount > 0 && (
            <>
              <span className="stat-separator">•</span>
              <span className="stat-item">
                Est. read time: <strong>{Math.max(1, Math.ceil(wordCount / 200))} min</strong>
              </span>
            </>
          )}
        </div>

        <span className="source-hint">
          Supports: Articles, Reports, Advisories, Papers, Announcements & Raw Prompts
        </span>
      </div>
    </section>
  );
}
