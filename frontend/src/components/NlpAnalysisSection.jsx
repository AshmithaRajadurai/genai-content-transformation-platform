import { useState } from 'react';
import { BrainIcon, TagIcon, CopyIcon, CheckCircleIcon } from './Icons';

export default function NlpAnalysisSection({ nlpData, transformedState }) {
  const [copied, setCopied] = useState(false);

  if (!transformedState || !nlpData) {
    return (
      <section className="dashboard-card nlp-card nlp-card-empty" aria-label="NLP Analysis Section">
        <div className="card-header">
          <div className="card-header-left">
            <span className="card-step-badge">5</span>
            <div>
              <h2 className="card-title">NLP Analysis Layer</h2>
              <p className="card-subtitle">
                Extracts topics, keywords, named entities, and key facts prior to LLM generation
              </p>
            </div>
          </div>
          <span className="nlp-pipeline-tag">Pipeline Layer 2</span>
        </div>

        <div className="nlp-idle-prompt">
          <BrainIcon className="nlp-idle-icon" />
          <p className="nlp-idle-text">
            Provide source content and click <strong>&quot;Transform Content&quot;</strong> to inspect the structured NLP extraction (topics, keywords, entities, and facts).
          </p>
        </div>
      </section>
    );
  }

  const handleCopyNlp = () => {
    navigator.clipboard.writeText(JSON.stringify(nlpData, null, 2));
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const topic = nlpData.topic || 'General Domain';
  const contentType = nlpData.contentType || nlpData.content_type || 'Analytical Briefing';
  const detectedTone = nlpData.detectedTone || nlpData.detected_tone || 'Professional & Authoritative';
  const confidenceScore = nlpData.confidenceScore || nlpData.confidence_score || 95.0;
  const keyFacts = nlpData.keyFacts || nlpData.key_facts || [];
  const summaryContext = nlpData.summaryContext || nlpData.summary_context || '';
  const keywords = nlpData.keywords || [];
  const entities = nlpData.entities || [];

  return (
    <section className="dashboard-card nlp-card" id="nlp-analysis-section" aria-label="NLP Analysis Results">
      <div className="card-header">
        <div className="card-header-left">
          <span className="card-step-badge">5</span>
          <div>
            <div className="card-title-row">
              <h2 className="card-title">NLP Analysis Layer</h2>
              <span className="nlp-pipeline-tag">Pipeline Layer 2 • Real NLP Extraction</span>
            </div>
            <p className="card-subtitle">
              Structured semantic extraction fed into the Context Engine to guarantee factual fidelity
            </p>
          </div>
        </div>

        <div className="nlp-header-actions">
          <span className="nlp-confidence-pill" title="NLP Extraction Confidence Score">
            <span className="dot dot-green"></span>
            Factual Confidence: <strong>{confidenceScore}%</strong>
          </span>
          <button
            type="button"
            className="btn-pill"
            onClick={handleCopyNlp}
            title="Copy structured NLP JSON"
          >
            <CopyIcon className="icon-tiny" />
            <span>{copied ? 'Copied JSON!' : 'Copy NLP JSON'}</span>
          </button>
        </div>
      </div>

      <div className="nlp-results-container">
        {/* Row 1: Primary Classification & Tone */}
        <div className="nlp-overview-grid">
          <div className="nlp-stat-box">
            <span className="stat-label">Identified Topic</span>
            <div className="stat-value-group">
              <BrainIcon className="icon-small text-accent" />
              <strong className="stat-value-highlight">{topic}</strong>
            </div>
          </div>

          <div className="nlp-stat-box">
            <span className="stat-label">Content Classification</span>
            <div className="stat-value-group">
              <span className="nlp-badge-type">{contentType}</span>
            </div>
          </div>

          <div className="nlp-stat-box">
            <span className="stat-label">Detected Tone & Sentiment</span>
            <div className="stat-value-group">
              <span className="nlp-badge-tone">{detectedTone}</span>
            </div>
          </div>
        </div>

        {/* Row 2: Keywords & Named Entities */}
        <div className="nlp-split-grid">
          {/* Keywords */}
          <div className="nlp-section-box">
            <div className="box-header">
              <TagIcon className="icon-small text-blue" />
              <h4 className="box-title">Salient Keywords ({keywords.length})</h4>
            </div>
            <div className="keywords-chip-list">
              {keywords.map((kw, i) => (
                <span key={i} className="keyword-chip">
                  <span className="chip-hash">#</span>
                  {kw}
                </span>
              ))}
            </div>
          </div>

          {/* Named Entities */}
          <div className="nlp-section-box">
            <div className="box-header">
              <BrainIcon className="icon-small text-purple" />
              <h4 className="box-title">Named Entities ({entities.length})</h4>
            </div>
            <div className="entities-chip-list">
              {entities.map((ent, i) => (
                <div key={i} className="entity-item-pill">
                  <span className="entity-name">{ent.name}</span>
                  <span className="entity-type-badge">{ent.type}</span>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Row 3: Key Facts Extracted */}
        <div className="nlp-section-box nlp-facts-box">
          <div className="box-header">
            <CheckCircleIcon className="icon-small text-emerald" />
            <h4 className="box-title">Core Key Facts & Semantic Assertions</h4>
          </div>
          <div className="facts-list">
            {keyFacts.map((fact, i) => (
              <div key={i} className="fact-item">
                <span className="fact-index">{i + 1}</span>
                <p className="fact-text">{fact}</p>
              </div>
            ))}
          </div>
        </div>

        {/* Row 4: Summary Context Passed to Context Engine */}
        <div className="nlp-context-banner">
          <div className="context-banner-left">
            <span className="context-tag">Context Engine Payload:</span>
            <p className="context-text">{summaryContext}</p>
          </div>
        </div>
      </div>
    </section>
  );
}
