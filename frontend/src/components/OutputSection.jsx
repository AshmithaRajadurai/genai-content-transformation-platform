import { useState } from 'react';
import { OUTPUT_TYPES } from '../data/constants';
import {
  SparklesIcon,
  CopyIcon,
  CodeIcon,
  FileTextIcon,
  LinkedInIcon,
  TwitterIcon,
  ShieldAlertIcon,
  BriefcaseIcon,
  ChartPieIcon,
  PresentationIcon,
  VideoIcon
} from './Icons';

export default function OutputSection({
  transformedState,
  selectedTypes,
  settings,
  outputsData,
  llmResult,
  onClearOutput
}) {
  const [selectedTab, setSelectedTab] = useState('');
  const [viewMode, setViewMode] = useState('formatted'); // 'formatted' | 'json' | 'llm_raw'
  const [copied, setCopied] = useState(false);

  // Active tab derivation
  const activeTab = selectedTypes.includes(selectedTab)
    ? selectedTab
    : (selectedTypes[0] || '');

  const activeFormatInfo = OUTPUT_TYPES.find((item) => item.id === activeTab);
  const activeOutputContent = outputsData?.[activeTab];

  const channelMap = {
    linkedin: 'linkedin',
    twitter: 'twitter',
    advisory: 'advisory',
    executive: 'executive_summary',
    infographic: 'infographic',
    presentation: 'presentation',
    video: 'video_script'
  };
  const activeLlmKey = channelMap[activeTab] || activeTab;
  const activeLlmItem = llmResult?.results?.[activeLlmKey];

  const handleCopyCurrent = () => {
    let textToCopy;
    if (viewMode === 'llm_raw' && activeLlmItem) {
      textToCopy = activeLlmItem.content;
    } else if (viewMode === 'json' || !activeOutputContent) {
      textToCopy = JSON.stringify(activeOutputContent || {}, null, 2);
    } else if (activeTab === 'linkedin') {
      textToCopy = `${activeOutputContent.title}\n\n${activeOutputContent.content}\n\n${activeOutputContent.hashtags?.join(' ')}`;
    } else if (activeTab === 'twitter') {
      textToCopy = `${activeOutputContent.hook}\n\n${activeOutputContent.tweets?.map((t) => t.text).join('\n\n')}`;
    } else if (activeTab === 'advisory') {
      textToCopy = `ADVISORY: ${activeOutputContent.advisory_id} (${activeOutputContent.severity})\nTITLE: ${activeOutputContent.title}\n\nIMPACT:\n${activeOutputContent.impact}\n\nMITIGATION:\n${activeOutputContent.mitigation_steps?.map((s, i) => `${i + 1}. ${s}`).join('\n')}`;
    } else if (activeTab === 'executive') {
      textToCopy = `EXECUTIVE SUMMARY: ${activeOutputContent.title}\n\n${activeOutputContent.summary}\n\nKEY POINTS:\n${activeOutputContent.key_points?.map((p) => `• ${p}`).join('\n')}\n\nRECOMMENDATIONS:\n${activeOutputContent.recommendations?.map((r) => `• ${r}`).join('\n')}`;
    } else {
      textToCopy = JSON.stringify(activeOutputContent, null, 2);
    }

    navigator.clipboard.writeText(textToCopy);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };


  const renderFormatIcon = (id) => {
    switch (id) {
      case 'linkedin':
        return <LinkedInIcon className="icon-small text-linkedin" />;
      case 'twitter':
        return <TwitterIcon className="icon-small text-twitter" />;
      case 'advisory':
        return <ShieldAlertIcon className="icon-small text-advisory" />;
      case 'executive':
        return <BriefcaseIcon className="icon-small text-executive" />;
      case 'infographic':
        return <ChartPieIcon className="icon-small text-infographic" />;
      case 'presentation':
        return <PresentationIcon className="icon-small text-presentation" />;
      case 'video':
        return <VideoIcon className="icon-small text-video" />;
      default:
        return <SparklesIcon className="icon-small text-accent" />;
    }
  };

  return (
    <section className="dashboard-card output-card" id="output-results-section" aria-labelledby="output-results-heading">
      <div className="card-header">
        <div className="card-header-left">
          <span className="card-step-badge">6</span>
          <div>
            <div className="card-title-row">
              <h2 id="output-results-heading" className="card-title">Generated Communication Artefacts</h2>
              {transformedState && llmResult && (
                <span className="llm-pipeline-tag" title="LLM Engine Execution Details">
                  <span className="dot dot-green"></span>
                  LLM Engine: <strong>{llmResult.provider?.toUpperCase()}</strong> • {llmResult.total_tokens} Tokens • {llmResult.execution_time_ms}ms
                </span>
              )}
            </div>
            <p className="card-subtitle">
              Multi-channel outputs synthesized from the NLP Context Engine via grounded LLM generation
            </p>
          </div>
        </div>

        {transformedState && (
          <div className="output-header-actions">
            <div className="view-mode-toggle" role="group" aria-label="Output view modes">
              <button
                type="button"
                className={`mode-btn ${viewMode === 'formatted' ? 'mode-btn-active' : ''}`}
                onClick={() => setViewMode('formatted')}
              >
                <FileTextIcon className="icon-tiny" />
                <span>Formatted</span>
              </button>
              <button
                type="button"
                className={`mode-btn ${viewMode === 'json' ? 'mode-btn-active' : ''}`}
                onClick={() => setViewMode('json')}
              >
                <CodeIcon className="icon-tiny" />
                <span>JSON Schema</span>
              </button>
              {activeLlmItem && (
                <button
                  type="button"
                  className={`mode-btn ${viewMode === 'llm_raw' ? 'mode-btn-active' : ''}`}
                  onClick={() => setViewMode('llm_raw')}
                  title="View direct generation from LLM Engine"
                >
                  <SparklesIcon className="icon-tiny text-accent" />
                  <span>LLM Raw</span>
                </button>
              )}
            </div>


            <button
              type="button"
              className="btn-pill"
              onClick={handleCopyCurrent}
              title="Copy active format output"
            >
              <CopyIcon className="icon-tiny" />
              <span>{copied ? 'Copied!' : 'Copy Artefact'}</span>
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
            Provide your source content above, choose one or more output formats, configure your generation settings, and click <strong>&quot;Transform Content&quot;</strong> to execute the full pipeline.
          </p>
          <div className="empty-flow-hints">
            <span className="flow-hint-item">1. Ingest Source</span>
            <span className="flow-arrow">→</span>
            <span className="flow-hint-item">2. NLP Analysis</span>
            <span className="flow-arrow">→</span>
            <span className="flow-hint-item">3. Context Engine</span>
            <span className="flow-arrow">→</span>
            <span className="flow-hint-item">4. LLM Generation</span>
          </div>
        </div>
      ) : (
        // Transformed Output Canvas
        <div className="output-canvas">
          {/* Format Selection Tabs */}
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
                    {renderFormatIcon(typeId)}
                    <span>{item.label}</span>
                    <span className="tab-badge">{item.category}</span>
                  </button>
                );
              })}
            </div>
          )}

          {/* Active Tab Content */}
          {activeFormatInfo && activeOutputContent && (
            <div
              id={`panel-${activeFormatInfo.id}`}
              role="tabpanel"
              aria-labelledby={`tab-${activeFormatInfo.id}`}
              className="tab-panel-container"
            >
              {/* Metadata parameter tags */}
              <div className="output-meta-bar">
                <div className="meta-badge-group">
                  <span className="meta-badge">
                    <span className="meta-key">Format:</span> {activeFormatInfo.label}
                  </span>
                  <span className="meta-badge">
                    <span className="meta-key">Audience:</span> {settings.audience}
                  </span>
                  <span className="meta-badge">
                    <span className="meta-key">Tone:</span> {settings.tone}
                  </span>
                  <span className="meta-badge">
                    <span className="meta-key">Language:</span> {settings.language}
                  </span>
                  <span className="meta-badge">
                    <span className="meta-key">Objective:</span> {settings.objective}
                  </span>
                </div>
              </div>

              {/* View Mode: Raw LLM Output View */}
              {viewMode === 'llm_raw' ? (
                <div className="llm-raw-view">
                  <div className="llm-raw-header">
                    <div className="llm-raw-header-left">
                      <SparklesIcon className="icon-tiny text-accent" />
                      <span className="llm-raw-title">
                        Raw LLM Generation: {activeLlmItem?.channel_name || activeFormatInfo.label}
                      </span>
                    </div>
                    <div className="llm-raw-badges">
                      <span className="llm-badge-model">{activeLlmItem?.model || 'semantic-fusion-engine-v1'}</span>
                      <span className="llm-badge-tokens">{activeLlmItem?.tokens_used || 0} tokens</span>
                    </div>
                  </div>
                  <pre className="llm-raw-code-block">
                    <code>{activeLlmItem?.content || 'No LLM output available for this channel.'}</code>
                  </pre>
                </div>
              ) : viewMode === 'json' ? (
                <div className="json-schema-view">
                  <div className="json-header">
                    <div className="json-header-left">
                      <CodeIcon className="icon-tiny text-accent" />
                      <span className="json-title">Structured Output Schema: {activeFormatInfo.label}</span>
                    </div>
                    <span className="schema-valid-badge">Schema Validated ✓</span>
                  </div>
                  <pre className="json-code-block">
                    <code>{JSON.stringify(activeOutputContent, null, 2)}</code>
                  </pre>
                </div>
              ) : (
                /* View Mode: Formatted Interactive View */
                <div className="formatted-artefact-canvas">

                  {/* LinkedIn Format */}
                  {activeTab === 'linkedin' && (
                    <div className="artefact-card linkedin-view">
                      <div className="artefact-badge-bar">
                        <span className="channel-badge linkedin-badge">LinkedIn Post</span>
                        <span className="char-badge">{activeOutputContent.content?.length || 0} characters</span>
                      </div>
                      <h3 className="artefact-heading">{activeOutputContent.title}</h3>
                      <div className="artefact-text-block">
                        {activeOutputContent.content?.split('\n\n').map((paragraph, i) => (
                          <p key={i}>{paragraph}</p>
                        ))}
                      </div>
                      <div className="hashtags-row">
                        {activeOutputContent.hashtags?.map((tag, i) => (
                          <span key={i} className="hashtag-pill">{tag}</span>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* X / Twitter Format */}
                  {activeTab === 'twitter' && (
                    <div className="artefact-card twitter-view">
                      <div className="artefact-badge-bar">
                        <span className="channel-badge twitter-badge">X / Twitter Thread</span>
                        <span className="char-badge">{activeOutputContent.tweets?.length || 0} Tweets</span>
                      </div>
                      <div className="twitter-hook-box">
                        <strong>Thread Hook:</strong> {activeOutputContent.hook}
                      </div>
                      <div className="tweets-thread-list">
                        {activeOutputContent.tweets?.map((tweet, i) => (
                          <div key={i} className="tweet-card">
                            <div className="tweet-header">
                              <span className="tweet-num">Tweet {i + 1} of {activeOutputContent.tweets.length}</span>
                              <span className="tweet-length">{tweet.text.length} / 280 chars</span>
                            </div>
                            <p className="tweet-body">{tweet.text}</p>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Advisory Format */}
                  {activeTab === 'advisory' && (
                    <div className="artefact-card advisory-view">
                      <div className="advisory-top-banner">
                        <div className="advisory-id-group">
                          <ShieldAlertIcon className="icon-medium text-amber" />
                          <div>
                            <span className="advisory-id">{activeOutputContent.advisory_id}</span>
                            <h3 className="advisory-title">{activeOutputContent.title}</h3>
                          </div>
                        </div>
                        <span className="advisory-severity-pill">{activeOutputContent.severity}</span>
                      </div>

                      <div className="advisory-section">
                        <h4 className="advisory-subhead">Impact Assessment</h4>
                        <p className="advisory-impact-text">{activeOutputContent.impact}</p>
                      </div>

                      <div className="advisory-section">
                        <h4 className="advisory-subhead">Affected Systems</h4>
                        <div className="systems-list">
                          {activeOutputContent.affected_systems?.map((sys, i) => (
                            <span key={i} className="system-pill">{sys}</span>
                          ))}
                        </div>
                      </div>

                      <div className="advisory-section">
                        <h4 className="advisory-subhead">Mitigation &amp; Remediation Procedures</h4>
                        <ol className="mitigation-steps-list">
                          {activeOutputContent.mitigation_steps?.map((step, i) => (
                            <li key={i} className="mitigation-item">{step}</li>
                          ))}
                        </ol>
                      </div>
                    </div>
                  )}

                  {/* Executive Summary Format */}
                  {activeTab === 'executive' && (
                    <div className="artefact-card executive-view">
                      <div className="artefact-badge-bar">
                        <span className="channel-badge executive-badge">Executive Briefing</span>
                        <span className="char-badge">C-Suite Focus</span>
                      </div>
                      <h3 className="executive-main-title">{activeOutputContent.title}</h3>

                      <div className="executive-summary-block">
                        <h4 className="exec-section-label">Strategic TL;DR</h4>
                        <p className="exec-summary-text">{activeOutputContent.summary}</p>
                      </div>

                      <div className="executive-grid">
                        <div className="exec-col">
                          <h4 className="exec-section-label">Key Findings &amp; Implications</h4>
                          <ul className="exec-points-list">
                            {activeOutputContent.key_points?.map((pt, i) => (
                              <li key={i}>{pt}</li>
                            ))}
                          </ul>
                        </div>

                        <div className="exec-col">
                          <h4 className="exec-section-label">Strategic Recommendations</h4>
                          <ul className="exec-recs-list">
                            {activeOutputContent.recommendations?.map((rec, i) => (
                              <li key={i}>{rec}</li>
                            ))}
                          </ul>
                        </div>
                      </div>
                    </div>
                  )}

                  {/* Infographic Format */}
                  {activeTab === 'infographic' && (
                    <div className="artefact-card infographic-view">
                      <div className="artefact-badge-bar">
                        <span className="channel-badge infographic-badge">Infographic Visual Blueprint</span>
                        <span className="char-badge">Data-Driven Callouts</span>
                      </div>
                      <h3 className="infographic-title">{activeOutputContent.title}</h3>

                      <div className="infographic-headline-stat">
                        <span className="stat-sub">Headline Metric</span>
                        <div className="stat-big">{activeOutputContent.headline_stat}</div>
                      </div>

                      <div className="infographic-stats-grid">
                        {activeOutputContent.data_callouts?.map((item, i) => (
                          <div key={i} className="callout-card">
                            <span className="callout-metric">{item.metric}</span>
                            <span className="callout-label">{item.label}</span>
                          </div>
                        ))}
                      </div>

                      <div className="infographic-sections-row">
                        {activeOutputContent.visual_sections?.map((sec, i) => (
                          <div key={i} className="visual-section-box">
                            <h4 className="section-box-header">{sec.header}</h4>
                            <ul className="section-bullets">
                              {sec.bullet_points?.map((bp, j) => (
                                <li key={j}>{bp}</li>
                              ))}
                            </ul>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Presentation Format */}
                  {activeTab === 'presentation' && (
                    <div className="artefact-card presentation-view">
                      <div className="artefact-badge-bar">
                        <span className="channel-badge presentation-badge">Slide Deck Outline</span>
                        <span className="char-badge">{activeOutputContent.slides?.length || 0} Slides</span>
                      </div>
                      <h3 className="presentation-title">{activeOutputContent.title}</h3>

                      <div className="presentation-slides-grid">
                        {activeOutputContent.slides?.map((slide, i) => (
                          <div key={i} className="slide-card">
                            <div className="slide-header">
                              <span className="slide-num-pill">Slide {slide.slide_number}</span>
                              <h4 className="slide-title">{slide.title}</h4>
                            </div>
                            <ul className="slide-bullets">
                              {slide.content?.map((bullet, j) => (
                                <li key={j}>{bullet}</li>
                              ))}
                            </ul>
                            <div className="speaker-notes-box">
                              <span className="notes-label">Speaker Notes:</span>
                              <p className="notes-text">&quot;{slide.speaker_notes}&quot;</p>
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Video Package Format */}
                  {activeTab === 'video' && (
                    <div className="artefact-card video-view">
                      <div className="artefact-badge-bar">
                        <span className="channel-badge video-badge">Video Production Package</span>
                        <span className="char-badge">Script &amp; Storyboard</span>
                      </div>
                      <h3 className="video-title">{activeOutputContent.title}</h3>

                      <div className="video-objective-box">
                        <strong>Target Video Objective:</strong> {activeOutputContent.objective}
                      </div>

                      <div className="video-script-box">
                        <h4 className="video-section-heading">Master Voiceover Script</h4>
                        <p className="script-text">{activeOutputContent.script}</p>
                      </div>

                      <div className="video-scenes-section">
                        <h4 className="video-section-heading">Scene-by-Scene Storyboard</h4>
                        <div className="scenes-grid">
                          {activeOutputContent.scenes?.map((scene, i) => (
                            <div key={i} className="scene-card">
                              <div className="scene-header">
                                <span className="scene-num">Scene {scene.scene_number}</span>
                              </div>
                              <div className="scene-visual">
                                <span className="scene-field-tag">Visual Cue:</span>
                                <p>{scene.visual}</p>
                              </div>
                              <div className="scene-narration">
                                <span className="scene-field-tag">Audio Narration:</span>
                                <p>&quot;{scene.audio_narration}&quot;</p>
                              </div>
                            </div>
                          ))}
                        </div>
                      </div>

                      <div className="video-subtitles-section">
                        <h4 className="video-section-heading">Timed Subtitles / Captions</h4>
                        <div className="subtitles-list">
                          {activeOutputContent.subtitles?.map((sub, i) => (
                            <div key={i} className="subtitle-item">
                              <code>{sub}</code>
                            </div>
                          ))}
                        </div>
                      </div>

                      <div className="video-recs-section">
                        <h4 className="video-section-heading">Director &amp; Motion Design Recommendations</h4>
                        <ul className="video-recs-list">
                          {activeOutputContent.visual_recommendations?.map((rec, i) => (
                            <li key={i}>{rec}</li>
                          ))}
                        </ul>
                      </div>
                    </div>
                  )}
                </div>
              )}
            </div>
          )}
        </div>
      )}
    </section>
  );
}
