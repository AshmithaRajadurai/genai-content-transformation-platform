import { useState, useRef } from 'react';
import { SAMPLE_INPUTS } from '../data/constants';
import { UploadIcon, CheckCircleIcon } from './Icons';

const API_BASE_URL = 'http://127.0.0.1:8000';

export default function SourceInputSection({
  content,
  setContent,
  ingestionResult,
  setIngestionResult
}) {
  const [isUploading, setIsUploading] = useState(false);
  const [uploadError, setUploadError] = useState('');
  const fileInputRef = useRef(null);

  const wordCount = content.trim() ? content.trim().split(/\s+/).length : 0;
  const charCount = content.length;

  const handleLoadSample = (key) => {
    if (SAMPLE_INPUTS[key]) {
      setContent(SAMPLE_INPUTS[key]);
      setIngestionResult({
        id: `sample-${key}`,
        title: key === 'advisory' ? 'CRITICAL SECURITY ADVISORY (CVE-2026-4401)' : 'Executive Briefing: Agentic Multi-Model AI Workflows',
        source_type: key,
        word_count: SAMPLE_INPUTS[key].trim().split(/\s+/).length,
        char_count: SAMPLE_INPUTS[key].length,
        estimated_reading_time_minutes: 1,
        status: 'ready'
      });
      setUploadError('');
    }
  };

  const handleClear = () => {
    setContent('');
    setIngestionResult(null);
    setUploadError('');
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  const handleTriggerUpload = () => {
    if (fileInputRef.current) {
      fileInputRef.current.click();
    }
  };

  const handleFileSelected = async (e) => {
    const file = e.target.files?.[0];
    if (!file) return;

    setIsUploading(true);
    setUploadError('');

    try {
      const formData = new FormData();
      formData.append('file', file);

      const response = await fetch(`${API_BASE_URL}/api/v1/source/upload`, {
        method: 'POST',
        body: formData
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `Upload failed with HTTP ${response.status}`);
      }

      const result = await response.json();
      setContent(result.cleaned_content || result.raw_content || '');
      setIngestionResult(result);
    } catch (err) {
      console.warn('Backend file ingestion note:', err.message);

      // Graceful fallback for local text files if FastAPI backend is temporarily offline
      if (file.name.endsWith('.txt') || file.name.endsWith('.md')) {
        const reader = new FileReader();
        reader.onload = (event) => {
          const text = event.target?.result;
          if (typeof text === 'string') {
            setContent(text);
            setIngestionResult({
              id: 'local-file-' + Date.now(),
              title: file.name.replace(/\.[^/.]+$/, ''),
              source_type: file.name.split('.').pop() || 'text',
              filename: file.name,
              file_size_bytes: file.size,
              word_count: text.trim().split(/\s+/).length,
              char_count: text.length,
              estimated_reading_time_minutes: Math.max(1, Math.ceil(text.trim().split(/\s+/).length / 200)),
              status: 'ingested-locally'
            });
            setUploadError('Note: Ingested locally in browser (Backend offline). Start FastAPI for deep PDF/DOCX parsing.');
          }
        };
        reader.readAsText(file);
      } else {
        setUploadError(`Document Ingestion Notice: ${err.message}. (Ensure FastAPI is running on port 8000 for PDF/DOCX extraction).`);
      }
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <section className="dashboard-card source-card" aria-labelledby="source-content-heading">
      <div className="card-header">
        <div className="card-header-left">
          <span className="card-step-badge">1</span>
          <div>
            <h2 id="source-content-heading" className="card-title">Source Content Ingestion</h2>
            <p className="card-subtitle">
              Input text or upload documents (.txt, .md, .pdf, .docx, .json, .csv) for backend normalization
            </p>
          </div>
        </div>

        <div className="source-sample-actions">
          {/* Hidden File Input */}
          <input
            type="file"
            ref={fileInputRef}
            onChange={handleFileSelected}
            accept=".txt,.md,.markdown,.pdf,.docx,.json,.csv"
            style={{ display: 'none' }}
            id="source-file-upload-input"
          />

          <button
            type="button"
            className="btn-pill btn-pill-accent"
            onClick={handleTriggerUpload}
            disabled={isUploading}
            title="Upload document or PDF for extraction"
          >
            <UploadIcon className="icon-tiny" />
            <span>{isUploading ? 'Extracting...' : 'Upload Document'}</span>
          </button>

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

      {uploadError && (
        <div className="source-alert-banner">
          <span>⚠️ {uploadError}</span>
        </div>
      )}

      {ingestionResult && (
        <div className="source-ingested-meta-banner">
          <div className="meta-banner-left">
            <CheckCircleIcon className="icon-small text-emerald" />
            <span className="meta-banner-title">
              <strong>Ingested:</strong> {ingestionResult.title || ingestionResult.filename || 'Source Document'}
            </span>
          </div>
          <div className="meta-banner-pills">
            <span className="ingest-tag-pill">
              Format: <strong>{ingestionResult.source_type?.toUpperCase() || 'TEXT'}</strong>
            </span>
            {ingestionResult.file_size_bytes && (
              <span className="ingest-tag-pill">
                Size: <strong>{Math.round(ingestionResult.file_size_bytes / 1024)} KB</strong>
              </span>
            )}
            <span className="ingest-tag-pill">
              Words: <strong>{ingestionResult.word_count}</strong>
            </span>
          </div>
        </div>
      )}

      <div className="textarea-wrapper">
        <textarea
          id="source-content"
          name="sourceContent"
          value={content}
          onChange={(e) => {
            setContent(e.target.value);
            if (ingestionResult && ingestionResult.status !== 'ready') {
              setIngestionResult(null);
            }
          }}
          placeholder="Paste articles, reports, advisories, research briefs, prompts, or click 'Upload Document' to extract text from PDF or DOCX..."
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
          Multi-Format Ingestion: Supports Text, PDF, DOCX, Markdown, JSON, CSV
        </span>
      </div>
    </section>
  );
}
