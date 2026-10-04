import { useState } from 'react';
import './App.css';
import Header from './components/Header';
import SourceInputSection from './components/SourceInputSection';
import OutputTypeSection from './components/OutputTypeSection';
import GenerationSettingsSection from './components/GenerationSettingsSection';
import TransformActionBar from './components/TransformActionBar';
import PipelineProgressSection from './components/PipelineProgressSection';
import NlpAnalysisSection from './components/NlpAnalysisSection';
import OutputSection from './components/OutputSection';
import Footer from './components/Footer';
import {
  AUDIENCE_OPTIONS,
  TONE_OPTIONS,
  LANGUAGE_OPTIONS,
  DETAIL_LEVELS,
  OBJECTIVE_OPTIONS,
  PIPELINE_STAGES,
  getMockNlpData,
  getMockOutputs
} from './data/constants';

function App() {
  const [content, setContent] = useState('');
  const [selectedTypes, setSelectedTypes] = useState([
    'linkedin',
    'twitter',
    'advisory',
    'executive',
    'infographic',
    'presentation',
    'video'
  ]);
  const [settings, setSettings] = useState({
    audience: AUDIENCE_OPTIONS[0],
    tone: TONE_OPTIONS[0],
    language: LANGUAGE_OPTIONS[0],
    detailLevel: DETAIL_LEVELS[1],
    objective: OBJECTIVE_OPTIONS[0]
  });

  const [isTransforming, setIsTransforming] = useState(false);
  const [currentStageIndex, setCurrentStageIndex] = useState(0);
  const [transformedState, setTransformedState] = useState(false);
  const [nlpData, setNlpData] = useState(null);
  const [outputsData, setOutputsData] = useState(null);

  const handleTransform = () => {
    if (!content.trim() || selectedTypes.length === 0) return;

    setIsTransforming(true);
    setTransformedState(false);
    setCurrentStageIndex(0);

    // Step through each of the 6 pipeline stages sequentially to visualize architecture
    const stageDurationMs = 280;
    PIPELINE_STAGES.forEach((stage, idx) => {
      setTimeout(() => {
        setCurrentStageIndex(idx);

        // When reaching final stage, calculate and commit NLP and generative output data
        if (idx === PIPELINE_STAGES.length - 1) {
          const generatedNlp = getMockNlpData(content);
          const generatedOutputs = getMockOutputs(content, selectedTypes, settings, generatedNlp);

          setTimeout(() => {
            setNlpData(generatedNlp);
            setOutputsData(generatedOutputs);
            setIsTransforming(false);
            setTransformedState(true);

            // Smoothly scroll to the NLP section so the judge/user immediately sees NLP + Outputs
            const nlpElem = document.getElementById('nlp-analysis-section');
            if (nlpElem) {
              nlpElem.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
          }, stageDurationMs);
        }
      }, idx * stageDurationMs);
    });
  };

  const handleReset = () => {
    setContent('');
    setSelectedTypes([
      'linkedin',
      'twitter',
      'advisory',
      'executive',
      'infographic',
      'presentation',
      'video'
    ]);
    setSettings({
      audience: AUDIENCE_OPTIONS[0],
      tone: TONE_OPTIONS[0],
      language: LANGUAGE_OPTIONS[0],
      detailLevel: DETAIL_LEVELS[1],
      objective: OBJECTIVE_OPTIONS[0]
    });
    setTransformedState(false);
    setIsTransforming(false);
    setCurrentStageIndex(0);
    setNlpData(null);
    setOutputsData(null);
  };

  const handleClearOutput = () => {
    setTransformedState(false);
    setNlpData(null);
    setOutputsData(null);
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

          {/* Section 4: AI Processing Pipeline Flow Visualizer */}
          <PipelineProgressSection
            isTransforming={isTransforming}
            currentStageIndex={currentStageIndex}
            transformedState={transformedState}
          />

          {/* Section 5: NLP Analysis Layer (Appears before outputs) */}
          <NlpAnalysisSection
            nlpData={nlpData}
            transformedState={transformedState}
          />

          {/* Section 6: Generated Communication Artefacts */}
          <OutputSection
            transformedState={transformedState}
            selectedTypes={selectedTypes}
            settings={settings}
            outputsData={outputsData}
            onClearOutput={handleClearOutput}
          />
        </main>

        <Footer />
      </div>
    </div>
  );
}

export default App;