import { SparklesIcon, RefreshIcon } from './Icons';

export default function TransformActionBar({
  content,
  selectedTypesCount,
  onTransform,
  onReset,
  isTransforming
}) {
  const isReady = content.trim().length > 0 && selectedTypesCount > 0;

  return (
    <div className="action-bar-container">
      <div className="action-bar-info">
        <div className="action-status-indicator">
          <span
            className={`status-dot ${isReady ? 'status-dot-active' : 'status-dot-idle'}`}
          />
          <span className="action-status-text">
            {!content.trim()
              ? 'Awaiting source content'
              : selectedTypesCount === 0
              ? 'Select at least 1 output format'
              : `${selectedTypesCount} target format${selectedTypesCount > 1 ? 's' : ''} configured`}
          </span>
        </div>
      </div>

      <div className="action-bar-buttons">
        <button
          type="button"
          className="btn-secondary"
          onClick={onReset}
          title="Reset all inputs and selections"
        >
          <RefreshIcon className="icon-small" />
          <span>Reset</span>
        </button>

        <button
          type="button"
          id="transform-content-btn"
          className={`btn-primary ${!isReady ? 'btn-disabled' : ''}`}
          disabled={!isReady || isTransforming}
          onClick={onTransform}
          title={!isReady ? 'Enter source text and select formats to transform' : 'Execute content transformation'}
        >
          <SparklesIcon className={`icon-small ${isTransforming ? 'spin-icon' : ''}`} />
          <span>{isTransforming ? 'Synthesizing...' : 'Transform Content'}</span>
        </button>
      </div>
    </div>
  );
}
