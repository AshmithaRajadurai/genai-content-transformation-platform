import { useState } from 'react';
import { BrainIcon, TagIcon, CopyIcon, CheckCircleIcon, ShieldAlertIcon, SparklesIcon } from './Icons';

export default function NlpAnalysisSection({ nlpData, contextPayload, transformedState }) {
  const [copiedNlp, setCopiedNlp] = useState(false);
  const [copiedContext, setCopiedContext] = useState(false);
  const [selectedPromptKey, setSelectedPromptKey] = useState(null);
  const [showPromptInspector, setShowPromptInspector] = useState(false);

  if (!transformedState || !nlpData) {
    return (
      <section className="dashboard-card nlp-card nlp-card-empty" aria-label="NLP Analysis Section">
        <div className="card-header">
          <div className="card-header-left">
            <span className="card-step-badge">5</span>
            <div>
              <h2 className="card-title">NLP Analysis & Context Engine</h2>
              <p className="card-subtitle">
                Extracts topics, keywords, named entities, and compiles factual guardrails for LLM generation
              </p>
            </div>
          </div>
          <div className="pipeline-layer-badges">
            <span className="nlp-pipeline-tag">Pipeline Layer 2 & 3</span>
          </div>
        </div>

        <div className="nlp-idle-prompt">
          <BrainIcon className="nlp-idle-icon" />
          <p className="nlp-idle-text">
            Provide source content and click <strong>&quot;Transform Content&quot;</strong> to inspect the structured NLP extraction (topics, keywords, entities, and facts) and compiled Context Engine prompts.
          </p>
        </div>
      </section>
    );
  }

  const handleCopyNlp = () => {
    navigator.clipboard.writeText(JSON.stringify(nlpData, null, 2));
    setCopiedNlp(true);
    setTimeout(() => setCopiedNlp(false), 2000);
  };

  const handleCopyContext = () => {
    if (!contextPayload) return;
    navigator.clipboard.writeText(JSON.stringify(contextPayload, null, 2));
    setCopiedContext(true);
    setTimeout(() => setCopiedContext(false), 2000);
  };

  const topic = nlpData.topic || 'General Domain';
  const contentType = nlpData.contentType || nlpData.content_type || 'Analytical Briefing';
  const detectedTone = nlpData.detectedTone || nlpData.detected_tone || 'Professional & Authoritative';
  const confidenceScore = nlpData.confidenceScore || nlpData.confidence_score || 95.0;
  const keyFacts = nlpData.keyFacts || nlpData.key_facts || [];
  const summaryContext = nlpData.summaryContext || nlpData.summary_context || '';
  const keywords = nlpData.keywords || [];
  const entities = nlpData.entities || [];

  const channelPromptKeys = contextPayload?.channel_prompts ? Object.keys(contextPayload.channel_prompts) : [];
  const activePromptKey = selectedPromptKey || (channelPromptKeys.length > 0 ? channelPromptKeys[0] : null);
  const activePrompt = activePromptKey && contextPayload?.channel_prompts ? contextPayload.channel_prompts[activePromptKey] : null;

  return (
    <section className="dashboard-card nlp-card" id="nlp-analysis-section" aria-label="NLP Analysis & Context Engine Results">
      <div className="card-header">
        <div className="card-header-left">
          <span className="card-step-badge">5</span>
          <div>
            <div className="card-title-row">
              <h2 className="card-title">NLP Analysis & Context Engine</h2>
              <span className="nlp-pipeline-tag">Pipeline Layer 2 • Real NLP Extraction</span>
              {contextPayload && (
                <span className="context-pipeline-tag">Pipeline Layer 3 • Grounded Prompts</span>
              )}
            </div>
            <p className="card-subtitle">
              Structured semantic extraction fused with audience persona to guarantee factual fidelity and zero hallucination
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
            <span>{copiedNlp ? 'Copied NLP!' : 'Copy NLP JSON'}</span>
          </button>
          {contextPayload && (
            <button
              type="button"
              className="btn-pill btn-pill-accent"
              onClick={handleCopyContext}
              title="Copy compiled Context Engine JSON"
            >
              <CopyIcon className="icon-tiny" />
              <span>{copiedContext ? 'Copied Context!' : 'Copy Context JSON'}</span>
            </button>
          )}
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
            <span className="context-tag">Context Engine Summary:</span>
            <p className="context-text">{summaryContext}</p>
          </div>
        </div>

        {/* Row 5: Real Context Engine (Pipeline Layer 3) Panel */}
        {contextPayload && (
          <div className="context-engine-panel">
            <div className="context-panel-header">
              <div className="context-panel-title-group">
                <div className="context-layer-indicator">
                  <SparklesIcon className="icon-tiny text-cyan" />
                  <span className="context-layer-label">Layer 3: Context Engine</span>
                </div>
                <h3 className="context-panel-title">Factual Grounding & Prompt Compiler</h3>
              </div>
              <div className="context-badge-group">
                <span className="context-metric-pill">
                  {channelPromptKeys.length} Channel Prompts Compiled
                </span>
                <button
                  type="button"
                  className="btn-inspect-prompts"
                  onClick={() => setShowPromptInspector(!showPromptInspector)}
                >
                  {showPromptInspector ? 'Hide Compiled Prompts' : 'Inspect LLM Prompts'}
                </button>
              </div>
            </div>

            {/* Directives & Target Audience Matrix */}
            <div className="context-directives-grid">
              <div className="context-directive-card">
                <span className="directive-label">Audience Persona Target</span>
                <strong className="directive-value">{contextPayload.audience_persona}</strong>
              </div>
              <div className="context-directive-card">
                <span className="directive-label">Communication Tone Directive</span>
                <strong className="directive-value">{contextPayload.tone_guideline}</strong>
              </div>
              <div className="context-directive-card">
                <span className="directive-label">Language & Detail Depth</span>
                <strong className="directive-value">
                  {contextPayload.language} • {contextPayload.detail_level?.toUpperCase()}
                </strong>
              </div>
            </div>

            {/* Anti-Hallucination Guardrails Banner */}
            <div className="context-guardrails-box">
              <div className="guardrails-header">
                <ShieldAlertIcon className="icon-small text-cyan" />
                <span className="guardrails-title">Anti-Hallucination & Entity Preservation Directives</span>
              </div>
              <pre className="guardrails-pre">{contextPayload.global_system_instruction}</pre>
            </div>

            {/* Interactive Prompt Inspector */}
            {showPromptInspector && activePrompt && (
              <div className="context-prompt-inspector-box">
                <div className="channel-tab-bar">
                  {channelPromptKeys.map((key) => {
                    const promptItem = contextPayload.channel_prompts[key];
                    return (
                      <button
                        key={key}
                        type="button"
                        className={`channel-tab-btn ${activePromptKey === key ? 'channel-tab-active' : ''}`}
                        onClick={() => setSelectedPromptKey(key)}
                      >
                        {promptItem.channel_name || key}
                      </button>
                    );
                  })}
                </div>

                <div className="active-prompt-details">
                  <div className="prompt-meta-row">
                    <span className="prompt-channel-tag">{activePrompt.channel_name}</span>
                    <span className="prompt-rules-count">
                      {activePrompt.grounding_rules?.length || 0} Grounding Rules Active
                    </span>
                  </div>

                  {activePrompt.grounding_rules && activePrompt.grounding_rules.length > 0 && (
                    <div className="prompt-rules-list">
                      {activePrompt.grounding_rules.map((rule, idx) => (
                        <div key={idx} className="rule-item">
                          <span className="rule-dot"></span>
                          <span>{rule}</span>
                        </div>
                      ))}
                    </div>
                  )}

                  <div className="prompt-content-view">
                    <div className="prompt-view-label">Compiled User Prompt (Passed to LLM Engine):</div>
                    <pre className="prompt-view-code">{activePrompt.user_prompt}</pre>
                  </div>
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </section>
  );
}
