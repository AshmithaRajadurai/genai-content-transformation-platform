import { useState, useEffect } from 'react';
import {
  DatabaseIcon,
  XIcon,
  RefreshIcon,
  ClockIcon,
  TrashIcon,
  SparklesIcon,
  LinkedInIcon,
  TwitterIcon,
  ShieldAlertIcon,
  BriefcaseIcon,
  ChartPieIcon,
  PresentationIcon,
  VideoIcon
} from './Icons';

const CHANNEL_ICONS = {
  linkedin: LinkedInIcon,
  twitter: TwitterIcon,
  advisory: ShieldAlertIcon,
  executive: BriefcaseIcon,
  infographic: ChartPieIcon,
  presentation: PresentationIcon,
  video: VideoIcon
};

export default function HistoryModal({ isOpen, onClose, onSelectRecord }) {
  const [historyItems, setHistoryItems] = useState([]);
  const [totalCount, setTotalCount] = useState(0);
  const [dbStatus, setDbStatus] = useState('checking');
  const [loading, setLoading] = useState(false);
  const [loadingDetailId, setLoadingDetailId] = useState(null);
  const [errorMsg, setErrorMsg] = useState(null);

  const fetchHistory = async () => {
    setLoading(true);
    setErrorMsg(null);
    try {
      const res = await fetch('http://127.0.0.1:8000/api/v1/history?limit=30');
      if (res.ok) {
        const data = await res.json();
        setHistoryItems(data.items || []);
        setTotalCount(data.total || 0);
        setDbStatus(data.database_status || 'offline_fallback');
      } else {
        setDbStatus('offline_fallback');
      }
    } catch (err) {
      setDbStatus('offline_fallback');
      setErrorMsg('Could not reach backend history endpoint. Ensure FastAPI is running.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (isOpen) {
      fetchHistory();
    }
  }, [isOpen]);

  const handleLoadRecord = async (transformationId) => {
    setLoadingDetailId(transformationId);
    try {
      const res = await fetch(`http://127.0.0.1:8000/api/v1/history/${transformationId}`);
      if (res.ok) {
        const record = await res.json();
        onSelectRecord(record);
        onClose();
      } else {
        alert('Could not retrieve full transformation record.');
      }
    } catch {
      alert('Error fetching transformation detail from backend.');
    } finally {
      setLoadingDetailId(null);
    }
  };

  const handleDeleteRecord = async (transformationId, e) => {
    e.stopPropagation();
    if (!confirm('Are you sure you want to delete this transformation record from MongoDB?')) {
      return;
    }

    try {
      const res = await fetch(`http://127.0.0.1:8000/api/v1/history/${transformationId}`, {
        method: 'DELETE'
      });
      if (res.ok) {
        setHistoryItems((prev) => prev.filter((it) => it.transformation_id !== transformationId));
        setTotalCount((prev) => Math.max(0, prev - 1));
      }
    } catch {
      alert('Failed to delete transformation record.');
    }
  };

  if (!isOpen) return null;

  return (
    <div className="history-modal-backdrop" onClick={onClose}>
      <div
        className="history-modal-content"
        onClick={(e) => e.stopPropagation()}
        role="dialog"
        aria-modal="true"
      >
        {/* Modal Header */}
        <div className="history-modal-header">
          <div className="history-title-group">
            <div className="history-icon-badge">
              <DatabaseIcon className="w-5 h-5 text-emerald-400" />
            </div>
            <div>
              <h2 className="history-modal-title">Transformation History & Archive</h2>
              <p className="history-modal-subtitle">
                Inspect and reload past generative transformations stored in MongoDB Atlas
              </p>
            </div>
          </div>
          <button
            type="button"
            className="history-close-btn"
            onClick={onClose}
            aria-label="Close History Modal"
          >
            <XIcon className="w-5 h-5" />
          </button>
        </div>

        {/* Database Status & Health Bar */}
        <div className="history-status-bar">
          <div className="history-db-badge">
            <span
              className={`db-pulse-dot ${
                dbStatus === 'connected' ? 'dot-green' : 'dot-amber'
              }`}
            />
            <span className="db-status-label">
              {dbStatus === 'connected'
                ? 'MongoDB Atlas (Cloud Active)'
                : 'Session Cache (Resilient Fallback)'}
            </span>
          </div>

          <div className="history-meta-actions">
            <span className="history-count-badge">
              {totalCount} {totalCount === 1 ? 'Record' : 'Records'}
            </span>
            <button
              type="button"
              className="history-refresh-btn"
              onClick={fetchHistory}
              disabled={loading}
              title="Refresh History from MongoDB"
            >
              <RefreshIcon className={`w-4 h-4 ${loading ? 'spin-icon' : ''}`} />
              <span>Refresh</span>
            </button>
          </div>
        </div>

        {/* Error Notification */}
        {errorMsg && (
          <div className="history-error-banner">
            <span>{errorMsg}</span>
          </div>
        )}

        {/* History Records List */}
        <div className="history-list-container">
          {loading && historyItems.length === 0 ? (
            <div className="history-loading-state">
              <SparklesIcon className="w-8 h-8 spin-icon text-indigo-400" />
              <p>Querying MongoDB Atlas database...</p>
            </div>
          ) : historyItems.length === 0 ? (
            <div className="history-empty-state">
              <DatabaseIcon className="w-12 h-12 text-slate-500" />
              <h3>No Transformation History Yet</h3>
              <p>
                Run a content transformation from the main dashboard to automatically persist multi-channel artefacts here.
              </p>
            </div>
          ) : (
            <div className="history-items-grid">
              {historyItems.map((item) => (
                <div key={item.transformation_id} className="history-card">
                  <div className="history-card-header">
                    <div className="history-card-title-row">
                      <h4 className="history-card-title">
                        {item.source_title || 'Untitled Transformation'}
                      </h4>
                      <span className="history-topic-pill">{item.detected_topic || 'General'}</span>
                    </div>
                    <div className="history-card-meta">
                      <span className="history-timestamp">
                        <ClockIcon className="w-3.5 h-3.5" />
                        {new Date(item.created_at).toLocaleString([], {
                          month: 'short',
                          day: 'numeric',
                          hour: '2-digit',
                          minute: '2-digit'
                        })}
                      </span>
                      {item.total_tokens > 0 && (
                        <span className="history-tokens-badge">
                          ⚡ {item.total_tokens} tokens
                        </span>
                      )}
                    </div>
                  </div>

                  <div className="history-channels-row">
                    <span className="history-channels-label">Artefacts:</span>
                    <div className="history-channel-chips">
                      {item.channels && item.channels.length > 0 ? (
                        item.channels.map((ch) => {
                          const IconComp = CHANNEL_ICONS[ch] || SparklesIcon;
                          return (
                            <span key={ch} className="history-channel-chip" title={ch}>
                              <IconComp className="w-3.5 h-3.5" />
                              <span>{ch}</span>
                            </span>
                          );
                        })
                      ) : (
                        <span className="history-channel-chip">Multi-Channel</span>
                      )}
                    </div>
                  </div>

                  <div className="history-card-actions">
                    <button
                      type="button"
                      className="history-load-btn"
                      disabled={loadingDetailId === item.transformation_id}
                      onClick={() => handleLoadRecord(item.transformation_id)}
                      title="Load this transformation into the dashboard"
                    >
                      <SparklesIcon className="w-4 h-4" />
                      <span>
                        {loadingDetailId === item.transformation_id
                          ? 'Loading...'
                          : 'Load Artefacts'}
                      </span>
                    </button>

                    <button
                      type="button"
                      className="history-delete-btn"
                      onClick={(e) => handleDeleteRecord(item.transformation_id, e)}
                      title="Delete from MongoDB"
                    >
                      <TrashIcon className="w-4 h-4" />
                    </button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
