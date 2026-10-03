import { useState } from 'react';
import './App.css';
import Header from './components/Header';
import SourceInputSection from './components/SourceInputSection';
import OutputTypeSection from './components/OutputTypeSection';
import GenerationSettingsSection from './components/GenerationSettingsSection';
import TransformActionBar from './components/TransformActionBar';
import OutputSection from './components/OutputSection';
import Footer from './components/Footer';
import {
  AUDIENCE_OPTIONS,
  TONE_OPTIONS,
  LANGUAGE_OPTIONS,
  DETAIL_LEVELS,
  OBJECTIVE_OPTIONS
} from './data/constants';

function App() {
  const [content, setContent] = useState('');
  const [selectedTypes, setSelectedTypes] = useState(['linkedin', 'executive', 'advisory']);
  const [settings, setSettings] = useState({
    audience: AUDIENCE_OPTIONS[0],
    tone: TONE_OPTIONS[0],
    language: LANGUAGE_OPTIONS[0],
    detailLevel: DETAIL_LEVELS[1],
    objective: OBJECTIVE_OPTIONS[0]
  });

  const [isTransforming, setIsTransforming] = useState(false);
  const [transformedState, setTransformedState] = useState(false);

  const handleTransform = () => {
    if (!content.trim() || selectedTypes.length === 0) return;

    setIsTransforming(true);
    // Smooth simulated processing transition
    setTimeout(() => {
      setIsTransforming(false);
      setTransformedState(true);

      // Scroll smoothly to output results
      const outputElem = document.getElementById('output-results-heading');
      if (outputElem) {
        outputElem.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    }, 450);
  };

  const handleReset = () => {
    setContent('');
    setSelectedTypes(['linkedin', 'executive', 'advisory']);
    setSettings({
      audience: AUDIENCE_OPTIONS[0],
      tone: TONE_OPTIONS[0],
      language: LANGUAGE_OPTIONS[0],
      detailLevel: DETAIL_LEVELS[1],
      objective: OBJECTIVE_OPTIONS[0]
    });
    setTransformedState(false);
  };

  const handleClearOutput = () => {
    setTransformedState(false);
  };

  return (
    <div className="app-shell">
      <div className="app-glow-background"></div>

      <div className="app-layout">
        <Header />

        <main className="main-content-flow">
          {/* Section 1: Source Content Input */}
          <SourceInputSection
            content={content}
            setContent={setContent}
          />

          {/* Section 2: Target Output Formats Multi-select */}
          <OutputTypeSection
            selectedTypes={selectedTypes}
            setSelectedTypes={setSelectedTypes}
          />

          {/* Section 3: Generation Tuning Settings */}
          <GenerationSettingsSection
            settings={settings}
            setSettings={setSettings}
          />

          {/* Main Action Bar */}
          <TransformActionBar
            content={content}
            selectedTypesCount={selectedTypes.length}
            onTransform={handleTransform}
            onReset={handleReset}
            isTransforming={isTransforming}
          />

          {/* Section 4: Output Display Area */}
          <OutputSection
            transformedState={transformedState}
            selectedTypes={selectedTypes}
            settings={settings}
            sourceContent={content}
            onClearOutput={handleClearOutput}
          />
        </main>

        <Footer />
      </div>
    </div>
  );
}

export default App;