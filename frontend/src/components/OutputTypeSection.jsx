import { OUTPUT_TYPES } from '../data/constants';
import {
  LinkedInIcon,
  TwitterIcon,
  ShieldAlertIcon,
  BriefcaseIcon,
  ChartPieIcon,
  PresentationIcon,
  VideoIcon,
  CheckCircleIcon
} from './Icons';

export default function OutputTypeSection({ selectedTypes, setSelectedTypes }) {
  const isAllSelected = selectedTypes.length === OUTPUT_TYPES.length;

  const toggleType = (id) => {
    if (selectedTypes.includes(id)) {
      setSelectedTypes(selectedTypes.filter((t) => t !== id));
    } else {
      setSelectedTypes([...selectedTypes, id]);
    }
  };

  const handleSelectAll = () => {
    if (isAllSelected) {
      setSelectedTypes([]);
    } else {
      setSelectedTypes(OUTPUT_TYPES.map((t) => t.id));
    }
  };

  const renderIcon = (iconName) => {
    switch (iconName) {
      case 'linkedin':
        return <LinkedInIcon className="format-icon text-linkedin" />;
      case 'twitter':
        return <TwitterIcon className="format-icon text-twitter" />;
      case 'advisory':
        return <ShieldAlertIcon className="format-icon text-advisory" />;
      case 'executive':
        return <BriefcaseIcon className="format-icon text-executive" />;
      case 'infographic':
        return <ChartPieIcon className="format-icon text-infographic" />;
      case 'presentation':
        return <PresentationIcon className="format-icon text-presentation" />;
      case 'video':
        return <VideoIcon className="format-icon text-video" />;
      default:
        return null;
    }
  };

  return (
    <section className="dashboard-card" aria-labelledby="output-type-heading">
      <div className="card-header">
        <div className="card-header-left">
          <span className="card-step-badge">2</span>
          <div>
            <h2 id="output-type-heading" className="card-title">Target Output Formats</h2>
            <p className="card-subtitle">
              Select one or multiple delivery formats to synthesize in parallel
            </p>
          </div>
        </div>

        <div className="format-header-actions">
          <span className="selection-count-pill">
            <strong>{selectedTypes.length}</strong> of {OUTPUT_TYPES.length} selected
          </span>
          <button
            type="button"
            className="btn-pill"
            onClick={handleSelectAll}
          >
            {isAllSelected ? 'Deselect All' : 'Select All'}
          </button>
        </div>
      </div>

      <div className="output-cards-grid">
        {OUTPUT_TYPES.map((item) => {
          const isSelected = selectedTypes.includes(item.id);

          return (
            <div
              key={item.id}
              role="button"
              tabIndex={0}
              id={`format-card-${item.id}`}
              className={`format-card ${isSelected ? 'format-card-selected' : ''}`}
              onClick={() => toggleType(item.id)}
              onKeyDown={(e) => {
                if (e.key === ' ' || e.key === 'Enter') {
                  e.preventDefault();
                  toggleType(item.id);
                }
              }}
              aria-pressed={isSelected}
            >
              <div className="format-card-top">
                <div className="format-icon-box">
                  {renderIcon(item.icon)}
                </div>
                <div className="format-checkbox-wrapper">
                  <input
                    type="checkbox"
                    id={`checkbox-${item.id}`}
                    checked={isSelected}
                    onChange={() => toggleType(item.id)}
                    onClick={(e) => e.stopPropagation()}
                    className="custom-checkbox"
                    aria-label={`Select ${item.label}`}
                  />
                  {isSelected && (
                    <CheckCircleIcon className="check-indicator-icon" />
                  )}
                </div>
              </div>

              <div className="format-card-body">
                <div className="format-title-row">
                  <h3 className="format-card-title">{item.label}</h3>
                  <span className="format-badge">{item.badge}</span>
                </div>
                <p className="format-card-desc">{item.description}</p>
              </div>
            </div>
          );
        })}
      </div>
    </section>
  );
}
