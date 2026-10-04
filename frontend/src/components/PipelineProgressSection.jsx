import { PIPELINE_STAGES } from '../data/constants';
import {
  FileTextIcon,
  BrainIcon,
  LayersIcon,
  CpuIcon,
  SparklesIcon,
  CheckCircleIcon
} from './Icons';

export default function PipelineProgressSection({
  isTransforming,
  currentStageIndex,
  transformedState
}) {
  const renderStageIcon = (id, isCompleted, isActive) => {
    const iconClass = isActive
      ? 'pipeline-icon icon-pulse'
      : isCompleted
      ? 'pipeline-icon icon-completed'
      : 'pipeline-icon icon-idle';

    switch (id) {
      case 'ingestion':
        return <FileTextIcon className={iconClass} />;
      case 'nlp':
        return <BrainIcon className={iconClass} />;
      case 'context':
        return <LayersIcon className={iconClass} />;
      case 'llm':
        return <CpuIcon className={iconClass} />;
      case 'generative':
        return <SparklesIcon className={iconClass} />;
      case 'outputs':
        return <CheckCircleIcon className={iconClass} />;
      default:
        return <CheckCircleIcon className={iconClass} />;
    }
  };

  return (
    <section className="dashboard-card pipeline-card" aria-label="AI Processing Pipeline">
      <div className="card-header">
        <div className="card-header-left">
          <span className="card-step-badge">4</span>
          <div>
            <h2 className="card-title">AI Processing Pipeline</h2>
            <p className="card-subtitle">
              End-to-end multi-stage architecture: Ingestion → NLP Analysis → Context Engine → LLM → Generative Transformation
            </p>
          </div>
        </div>

        <div className="pipeline-status-badge-wrap">
          {isTransforming ? (
            <span className="pipeline-live-pill pill-pulsing">
              <span className="live-dot-pulse"></span>
              Stage {currentStageIndex + 1} of 6: {PIPELINE_STAGES[currentStageIndex]?.title}
            </span>
          ) : transformedState ? (
            <span className="pipeline-live-pill pill-success">
              <CheckCircleIcon className="icon-tiny text-emerald" />
              Complete Pipeline Executed (6/6 Stages Verified)
            </span>
          ) : (
            <span className="pipeline-live-pill pill-idle">
              Ready for Execution
            </span>
          )}
        </div>
      </div>

      <div className="pipeline-flow-wrapper">
        <div className="pipeline-stages-grid">
          {PIPELINE_STAGES.map((stage, idx) => {
            const isCompleted = transformedState || (isTransforming && idx < currentStageIndex);
            const isActive = isTransforming && idx === currentStageIndex;

            let stageStatusClass = 'stage-pending';
            if (isActive) stageStatusClass = 'stage-active';
            else if (isCompleted) stageStatusClass = 'stage-completed';

            return (
              <div
                key={stage.id}
                className={`pipeline-stage-node ${stageStatusClass}`}
                id={`pipeline-step-${stage.id}`}
              >
                <div className="stage-top-indicator">
                  <span className="stage-number">{stage.step}</span>
                  <div className="stage-icon-circle">
                    {renderStageIcon(stage.id, isCompleted, isActive)}
                  </div>
                  {isCompleted ? (
                    <span className="stage-check-badge">✓</span>
                  ) : isActive ? (
                    <span className="stage-active-badge">●</span>
                  ) : (
                    <span className="stage-idle-badge">○</span>
                  )}
                </div>

                <div className="stage-content">
                  <h4 className="stage-title">{stage.title}</h4>
                  <p className="stage-subtitle">{stage.subtitle}</p>
                </div>

                {idx < PIPELINE_STAGES.length - 1 && (
                  <div className={`stage-connector ${isCompleted ? 'connector-completed' : ''}`}>
                    <span className="connector-arrow">→</span>
                  </div>
                )}
              </div>
            );
          })}
        </div>

        {isTransforming && (
          <div className="pipeline-live-activity-bar">
            <div className="progress-bar-track">
              <div
                className="progress-bar-fill"
                style={{ width: `${Math.round(((currentStageIndex + 1) / PIPELINE_STAGES.length) * 100)}%` }}
              ></div>
            </div>
            <span className="activity-text">
              Active Module: <strong>{PIPELINE_STAGES[currentStageIndex]?.description}</strong>
            </span>
          </div>
        )}
      </div>
    </section>
  );
}
