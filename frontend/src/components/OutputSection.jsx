import { useState } from 'react';
import { OUTPUT_TYPES } from '../data/constants';
import { SparklesIcon, CopyIcon, CheckCircleIcon } from './Icons';

export default function OutputSection({
  transformedState,
  selectedTypes,
  settings,
  sourceContent,
  onClearOutput
}) {
  const [selectedTab, setSelectedTab] = useState('');
  const [copied, setCopied] = useState(false);

  // Derive active tab from selection without cascading effect renders
  const activeTab = selectedTypes.includes(selectedTab)
    ? selectedTab
    : (selectedTypes[0] || '');

  const activeFormatInfo = OUTPUT_TYPES.find((item) => item.id === activeTab);

  const handleCopy = () => {
    const textToCopy = `AI transformation will appear here.\n\nTarget Format: ${activeFormatInfo?.label || 'General'}\nAudience: ${settings.audience}\nTone: ${settings.tone}\nLanguage: ${settings.language}\nDetail: ${settings.detailLevel}\nObjective: ${settings.objective}`;
    navigator.clipboard.writeText(textToCopy);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <section className="dashboard-card output-card" aria-labelledby="output-results-heading">
      <div className="card-header">
        <div className="card-header-left">
          <span className="card-step-badge">4</span>
          <div>
            <h2 id="output-results-heading" className="card-title">Generated Results</h2>
            <p className="card-subtitle">
              Multi-format synthesized outputs tailored by target audience and tone
            </p>
          </div>
        </div>

        {transformedState && (
          <div className="output-header-actions">
            <button
              type="button"
              className="btn-pill"
              onClick={handleCopy}
              title="Copy output details to clipboard"
            >
              <CopyIcon className="icon-tiny" />
              <span>{copied ? 'Copied!' : 'Copy Preview'}</span>
            </button>
            <button
              type="button"
              className="btn-pill btn-pill-danger"
              onClick={onClearOutput}
              title="Reset output display"
            >
              Reset View
            </button>
          </div>
        )}
      </div>

      {!transformedState ? (
        // Initial Empty State
        <div className="output-empty-container">
          <div className="empty-sparkle-halo">
            <SparklesIcon className="empty-sparkle-icon" />
          </div>
          <h3 className="empty-title">AI transformation will appear here.</h3>
          <p className="empty-desc">
            Provide your source content above, choose one or more output formats, customize your generation settings, and click <strong>&quot;Transform Content&quot;</strong> to generate your assets.
          </p>
          <div className="empty-flow-hints">
            <span className="flow-hint-item">1. Paste source text</span>
            <span className="flow-arrow">→</span>
            <span className="flow-hint-item">2. Pick target formats</span>
            <span className="flow-arrow">→</span>
            <span className="flow-hint-item">3. Click Transform</span>
          </div>
        </div>
      ) : (
        // Transformed Output Canvas
        <div className="output-canvas">
          {/* Milestone notice banner */}
          <div className="milestone-notice-banner">
            <div className="banner-left">
              <span className="banner-status-dot"></span>
              <div>
                <strong className="banner-headline">AI transformation will appear here.</strong>
                <p className="banner-subtext">
                  Milestone 1 UI verified: Transformation pipeline initialized for <strong>{selectedTypes.length}</strong> format{selectedTypes.length > 1 ? 's' : ''}. Direct LLM &amp; NLP generative inference will be wired in Milestone 2.
                </p>
              </div>
            </div>
          </div>

          {/* Selected Formats Tabs */}
          {selectedTypes.length > 0 && (
            <div className="format-tabs-bar" role="tablist">
              {selectedTypes.map((typeId) => {
                const item = OUTPUT_TYPES.find((t) => t.id === typeId);
                if (!item) return null;
                const isActive = activeTab === typeId;

                return (
                  <button
                    key={typeId}
                    role="tab"
                    id={`tab-${typeId}`}
                    aria-selected={isActive}
                    aria-controls={`panel-${typeId}`}
                    className={`format-tab-btn ${isActive ? 'format-tab-active' : ''}`}
                    onClick={() => setSelectedTab(typeId)}
                  >
                    <span>{item.label}</span>
                    <span className="tab-badge">{item.category}</span>
                  </button>
                );
              })}
            </div>
          )}

          {/* Active Tab Panel */}
          {activeFormatInfo && (
            <div
              id={`panel-${activeFormatInfo.id}`}
              role="tabpanel"
              aria-labelledby={`tab-${activeFormatInfo.id}`}
              className="tab-panel-container"
            >
              {/* Configuration metadata bar */}
              <div className="output-meta-bar">
                <div className="meta-badge-group">
                  <span className="meta-badge" title="Target Audience">
                    <span className="meta-key">Audience:</span> {settings.audience}
                  </span>
                  <span className="meta-badge" title="Tone of Voice">
                    <span className="meta-key">Tone:</span> {settings.tone}
                  </span>
                  <span className="meta-badge" title="Language">
                    <span className="meta-key">Lang:</span> {settings.language}
                  </span>
                  <span className="meta-badge" title="Level of Detail">
                    <span className="meta-key">Detail:</span> {settings.detailLevel}
                  </span>
                  <span className="meta-badge" title="Communication Objective">
                    <span className="meta-key">Objective:</span> {settings.objective}
                  </span>
                </div>
              </div>

              {/* Main Output Content Placeholder Box */}
              <div className="output-content-display">
                <div className="output-placeholder-header">
                  <div className="placeholder-title-group">
                    <CheckCircleIcon className="icon-small text-emerald" />
                    <span className="placeholder-format-name">{activeFormatInfo.label} Pipeline Ready</span>
                  </div>
                  <span className="source-sample-tag">
                    Source: {sourceContent.length} chars (~{sourceContent.trim() ? sourceContent.trim().split(/\s+/).length : 0} words)
                  </span>
                </div>

                <div className="output-placeholder-body">
                  <div className="placeholder-banner">
                    <SparklesIcon className="icon-medium text-accent" />
                    <h4>AI transformation will appear here.</h4>
                    <p>
                      When connected to the FastAPI backend LLM service, the generated <strong>{activeFormatInfo.label}</strong> content will be rendered here with live streaming, syntax formatting, and one-click export.
                    </p>
                  </div>

                  <div className="preview-spec-card">
                    <h5>Configured Synthesis Spec:</h5>
                    <div className="spec-grid">
                      <div className="spec-row">
                        <span className="spec-label">Format Type:</span>
                        <span className="spec-value">{activeFormatInfo.label} ({activeFormatInfo.category})</span>
                      </div>
                      <div className="spec-row">
                        <span className="spec-label">Format Goal:</span>
                        <span className="spec-value">{activeFormatInfo.description}</span>
                      </div>
                      <div className="spec-row">
                        <span className="spec-label">Audience Persona:</span>
                        <span className="spec-value">{settings.audience}</span>
                      </div>
                      <div className="spec-row">
                        <span className="spec-label">Stylistic Tone:</span>
                        <span className="spec-value">{settings.tone}</span>
                      </div>
                      <div className="spec-row">
                        <span className="spec-label">Level of Detail:</span>
                        <span className="spec-value">{settings.detailLevel}</span>
                      </div>
                      <div className="spec-row">
                        <span className="spec-label">Communication Objective:</span>
                        <span className="spec-value">{settings.objective}</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
      )}
    </section>
  );
}
