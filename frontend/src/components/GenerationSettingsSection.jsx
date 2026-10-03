import {
  AUDIENCE_OPTIONS,
  TONE_OPTIONS,
  LANGUAGE_OPTIONS,
  DETAIL_LEVELS,
  OBJECTIVE_OPTIONS
} from '../data/constants';

export default function GenerationSettingsSection({ settings, setSettings }) {
  const handleChange = (key, value) => {
    setSettings((prev) => ({
      ...prev,
      [key]: value
    }));
  };

  return (
    <section className="dashboard-card" aria-labelledby="generation-settings-heading">
      <div className="card-header">
        <div className="card-header-left">
          <span className="card-step-badge">3</span>
          <div>
            <h2 id="generation-settings-heading" className="card-title">Generation Settings</h2>
            <p className="card-subtitle">
              Tune target personas, tone, linguistic style, and structural depth
            </p>
          </div>
        </div>
      </div>

      <div className="settings-grid">
        {/* Target Audience */}
        <div className="setting-field">
          <label htmlFor="setting-audience" className="setting-label">
            Target Audience
          </label>
          <div className="select-container">
            <select
              id="setting-audience"
              className="custom-select"
              value={settings.audience}
              onChange={(e) => handleChange('audience', e.target.value)}
            >
              {AUDIENCE_OPTIONS.map((item) => (
                <option key={item} value={item}>
                  {item}
                </option>
              ))}
            </select>
          </div>
          <span className="setting-help">Aligns technical jargon and depth for the reader</span>
        </div>

        {/* Tone */}
        <div className="setting-field">
          <label htmlFor="setting-tone" className="setting-label">
            Tone
          </label>
          <div className="select-container">
            <select
              id="setting-tone"
              className="custom-select"
              value={settings.tone}
              onChange={(e) => handleChange('tone', e.target.value)}
            >
              {TONE_OPTIONS.map((item) => (
                <option key={item} value={item}>
                  {item}
                </option>
              ))}
            </select>
          </div>
          <span className="setting-help">Sets the voice and emotional register</span>
        </div>

        {/* Language */}
        <div className="setting-field">
          <label htmlFor="setting-language" className="setting-label">
            Language
          </label>
          <div className="select-container">
            <select
              id="setting-language"
              className="custom-select"
              value={settings.language}
              onChange={(e) => handleChange('language', e.target.value)}
            >
              {LANGUAGE_OPTIONS.map((item) => (
                <option key={item} value={item}>
                  {item}
                </option>
              ))}
            </select>
          </div>
          <span className="setting-help">Target localization and regional phrasing</span>
        </div>

        {/* Level of Detail */}
        <div className="setting-field">
          <label htmlFor="setting-detail" className="setting-label">
            Level of Detail
          </label>
          <div className="select-container">
            <select
              id="setting-detail"
              className="custom-select"
              value={settings.detailLevel}
              onChange={(e) => handleChange('detailLevel', e.target.value)}
            >
              {DETAIL_LEVELS.map((item) => (
                <option key={item} value={item}>
                  {item}
                </option>
              ))}
            </select>
          </div>
          <span className="setting-help">Controls length, complexity, and granularity</span>
        </div>

        {/* Communication Objective */}
        <div className="setting-field setting-field-full">
          <label htmlFor="setting-objective" className="setting-label">
            Communication Objective
          </label>
          <div className="select-container">
            <select
              id="setting-objective"
              className="custom-select"
              value={settings.objective}
              onChange={(e) => handleChange('objective', e.target.value)}
            >
              {OBJECTIVE_OPTIONS.map((item) => (
                <option key={item} value={item}>
                  {item}
                </option>
              ))}
            </select>
          </div>
          <span className="setting-help">Defines the primary goal (call to action, alerting, or education)</span>
        </div>
      </div>
    </section>
  );
}
