export const OUTPUT_TYPES = [
  {
    id: 'linkedin',
    label: 'LinkedIn Post',
    category: 'Social',
    badge: 'Engagement',
    description: 'Professional narrative with hooks, structured takeaways, and targeted hashtags.',
    icon: 'linkedin'
  },
  {
    id: 'twitter',
    label: 'X / Twitter Post',
    category: 'Social',
    badge: 'Viral Thread',
    description: 'Punchy 280-character takeaways, thread structure, and high-impact key lines.',
    icon: 'twitter'
  },
  {
    id: 'advisory',
    label: 'Advisory',
    category: 'Enterprise',
    badge: 'Security / Ops',
    description: 'Actionable notice detailing threat/impact, affected systems, and mitigation steps.',
    icon: 'advisory'
  },
  {
    id: 'executive',
    label: 'Executive Summary',
    category: 'Enterprise',
    badge: 'C-Suite',
    description: 'High-level strategic briefing, financial/operational implications, and executive TL;DR.',
    icon: 'executive'
  },
  {
    id: 'infographic',
    label: 'Infographic',
    category: 'Visual',
    badge: 'Data Callouts',
    description: 'Structured visual hierarchy, key statistics, comparative metrics, and layout briefs.',
    icon: 'infographic'
  },
  {
    id: 'presentation',
    label: 'Presentation',
    category: 'Visual',
    badge: 'Slide Deck',
    description: 'Slide-by-slide storyline with titles, structured bullet points, and speaker notes.',
    icon: 'presentation'
  },
  {
    id: 'video',
    label: 'Video Package',
    category: 'Media',
    badge: 'Script & B-Roll',
    description: 'Video script outline, timed narrator prompts, visual cues, and b-roll suggestions.',
    icon: 'video'
  }
];

export const AUDIENCE_OPTIONS = [
  'Business Executives & C-Suite',
  'Technical & Engineering Teams',
  'Security & Compliance Officers',
  'Investors & Board Members',
  'General Public / Consumers',
  'Cross-Functional Stakeholders'
];

export const TONE_OPTIONS = [
  'Professional & Authoritative',
  'Engaging & Conversational',
  'Technical & In-depth',
  'Urgent & Action-Oriented',
  'Persuasive & Visionary'
];

export const LANGUAGE_OPTIONS = [
  'English (US)',
  'English (UK)',
  'Spanish',
  'French',
  'German',
  'Japanese',
  'Mandarin'
];

export const DETAIL_LEVELS = [
  'Concise (Key Highlights & Bullets)',
  'Balanced (Standard Comprehensive Overview)',
  'In-depth (Full Deep Dive & Technical Analysis)'
];

export const OBJECTIVE_OPTIONS = [
  'Inform & Educate',
  'Drive Immediate Action & Mitigation',
  'Executive Decision Support',
  'Thought Leadership & Industry Influence',
  'Internal Alignment & Status Reporting'
];

export const SAMPLE_INPUTS = {
  advisory: `CRITICAL SECURITY ADVISORY (CVE-2026-4401)
Affected Product: Enterprise Cloud Gateway versions 4.2.0 through 4.9.1
Severity: 9.8 Critical (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H)

Summary:
A remote code execution vulnerability has been discovered in the authentication handling module of Enterprise Cloud Gateway. Unauthenticated remote attackers can send specially crafted HTTP headers to execute arbitrary code with root privileges.

Mitigation & Remediation:
1. Immediately upgrade to version 4.9.2 or apply patch KB-89104.
2. In the interim, restrict ingress traffic on port 8443 to internal trusted IP blocks.
3. Review audit logs for anomalous POST requests to /api/v2/auth/token endpoint.`,

  research: `Executive Briefing: The Shift Toward Agentic Multi-Model AI Workflows in Enterprise
Published: Q1 2026
Source: Global Enterprise AI Research Group

Key Findings:
1. Enterprise adoption of multi-agent AI architectures grew 280% year-over-year, moving beyond single-shot prompt interactions.
2. 74% of surveyed CTOs report that cross-format content repurposing (turning research into slide decks, executive summaries, and social media announcements) is the single most frequent time-sink for knowledge teams.
3. Automated multi-format transformation platforms reduce time-to-publish from 4.5 hours per asset down to under 90 seconds while maintaining 95%+ factual fidelity.`
};

export const PIPELINE_STAGES = [
  {
    id: 'ingestion',
    step: 1,
    title: 'Content Ingestion',
    subtitle: 'Input normalized & token checked',
    description: 'Raw source content sanitized, tokenized, and prepared for processing.'
  },
  {
    id: 'nlp',
    step: 2,
    title: 'NLP Analysis',
    subtitle: 'Keywords, entities & facts extracted',
    description: 'Named entity recognition (NER), topic modeling, and fact synthesis.'
  },
  {
    id: 'context',
    step: 3,
    title: 'Context Engine',
    subtitle: 'Parameters & metadata unified',
    description: 'Fusing source + NLP insights + persona, tone & communication objective.'
  },
  {
    id: 'llm',
    step: 4,
    title: 'LLM Processing',
    subtitle: 'Prompt templates compiled',
    description: 'Dispatching structured prompt payloads to configured LLM engine.'
  },
  {
    id: 'generative',
    step: 5,
    title: 'Generative AI Transformation',
    subtitle: 'Multi-artifact generation',
    description: 'Synthesizing format-tailored schemas per channel rules.'
  },
  {
    id: 'outputs',
    step: 6,
    title: 'Outputs Generated',
    subtitle: 'Artefacts synthesized & ready',
    description: 'Multi-format artefacts compiled and available for review, copy & export.'
  }
];

export const DEMO_NLP_INSIGHTS = {
  advisory: {
    topic: 'Cybersecurity & Vulnerability Management',
    contentType: 'Critical Security Advisory',
    detectedTone: 'Urgent & Action-Oriented',
    confidenceScore: 98.4,
    keywords: [
      'CVE-2026-4401',
      'remote code execution',
      'Enterprise Cloud Gateway',
      'CVSS 9.8',
      'authentication module',
      'patch KB-89104',
      'ingress traffic',
      'port 8443'
    ],
    entities: [
      { name: 'Enterprise Cloud Gateway', type: 'PRODUCT' },
      { name: 'CVE-2026-4401', type: 'VULNERABILITY' },
      { name: 'KB-89104', type: 'SECURITY_PATCH' },
      { name: 'CVSS:3.1', type: 'BENCHMARK' }
    ],
    keyFacts: [
      'Unauthenticated remote attackers can execute arbitrary code with root privileges.',
      'Severity rated at 9.8 Critical (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).',
      'Affects Enterprise Cloud Gateway releases 4.2.0 through 4.9.1.',
      'Remediation requires immediate upgrade to version 4.9.2 or patch KB-89104.',
      'Interim mitigation: restrict port 8443 ingress traffic to trusted internal IP ranges.'
    ],
    summaryContext:
      'Critical remote code execution vulnerability (CVE-2026-4401) affecting Enterprise Cloud Gateway auth modules requiring urgent patching to v4.9.2 and ingress traffic containment.'
  },
  research: {
    topic: 'Enterprise AI & Multi-Agent Automation',
    contentType: 'Strategic Research Briefing',
    detectedTone: 'Thought Leadership & Strategic',
    confidenceScore: 96.8,
    keywords: [
      'agentic AI workflows',
      'multi-agent architectures',
      'cross-format repurposing',
      'time-to-publish',
      'factual fidelity',
      'CTO survey',
      'knowledge productivity'
    ],
    entities: [
      { name: 'Global Enterprise AI Research Group', type: 'ORGANIZATION' },
      { name: 'Q1 2026', type: 'TIMEFRAME' },
      { name: 'Agentic AI', type: 'TECHNOLOGY' },
      { name: 'CTO', type: 'ROLE' }
    ],
    keyFacts: [
      'Enterprise multi-agent AI adoption surged 280% year-over-year in enterprise deployments.',
      '74% of surveyed CTOs cite cross-format repurposing as their teams primary operational time-sink.',
      'Automated multi-format transformation cuts production time from 4.5 hours to under 90 seconds.',
      'Maintains 95%+ factual fidelity across diverse derivative communication formats.'
    ],
    summaryContext:
      'Executive research reveals rapid transition to multi-agent generative transformation pipelines, slashing cross-channel content repurposing time from hours to seconds with high factual precision.'
  }
};

export const DEMO_STRUCTURED_OUTPUTS = {
  advisory: {
    linkedin: {
      title: '🚨 Critical Security Advisory: CVE-2026-4401 in Enterprise Cloud Gateway',
      content: `A critical Remote Code Execution vulnerability (CVE-2026-4401) with a CVSS score of 9.8 has been identified affecting Enterprise Cloud Gateway versions 4.2.0 through 4.9.1.

Unauthenticated attackers can exploit HTTP header handling to trigger code execution with root system privileges.

Immediate Actions Required:
• Upgrade immediately to version 4.9.2 or apply security hotfix KB-89104.
• Filter ingress traffic on port 8443 to verified internal corporate IP blocks.
• Audit gateway access logs for suspicious POST activity targeting /api/v2/auth/token.

Ensure your infrastructure and security teams review perimeter configurations today.`,
      hashtags: ['#Cybersecurity', '#CloudSecurity', '#InfoSec', '#VulnerabilityManagement', '#SecOps']
    },
    twitter: {
      hook: '🚨 CRITICAL ADVISORY: RCE vulnerability CVE-2026-4401 in Enterprise Cloud Gateway (CVSS 9.8). Immediate patching required.',
      tweets: [
        {
          index: 1,
          text: '1/4 🚨 ALERT: A CVSS 9.8 Critical Remote Code Execution flaw (CVE-2026-4401) has been confirmed in Enterprise Cloud Gateway (v4.2.0 - 4.9.1). Unauthenticated remote attackers can obtain root privileges.'
        },
        {
          index: 2,
          text: '2/4 🔍 Root Cause: Specially crafted HTTP headers allow malicious command execution via the authentication handling module.'
        },
        {
          index: 3,
          text: '3/4 🛡️ Mitigation Steps:\n1. Upgrade to v4.9.2 or patch KB-89104 immediately.\n2. Restrict ingress on port 8443 to internal IP ranges.\n3. Audit logs for anomalous POSTs to /api/v2/auth/token.'
        },
        {
          index: 4,
          text: '4/4 🔗 Check your perimeter gateways now and share with your SecOps and DevOps teams. #Cybersecurity #Infosec #DevSecOps'
        }
      ]
    },
    advisory: {
      advisory_id: 'ADV-2026-4401-CRIT',
      severity: 'CRITICAL (CVSS:3.1 - 9.8)',
      title: 'Remote Code Execution in Enterprise Cloud Gateway Authentication Module',
      affected_systems: [
        'Enterprise Cloud Gateway 4.2.0',
        'Enterprise Cloud Gateway 4.5.x',
        'Enterprise Cloud Gateway 4.9.0 - 4.9.1'
      ],
      impact: 'Unauthenticated remote attackers can execute arbitrary code with root privileges by sending forged HTTP headers to the authentication service.',
      mitigation_steps: [
        'Apply official vendor patch KB-89104 or upgrade to firmware version 4.9.2 immediately.',
        'Implement network firewall filtering on TCP port 8443, limiting exposure solely to trusted corporate subnets.',
        'Inspect reverse proxy and gateway access logs for abnormal POST payloads submitted to /api/v2/auth/token.'
      ]
    },
    executive: {
      title: 'Executive Briefing: High-Risk Vulnerability CVE-2026-4401 in Gateway Infrastructure',
      summary: 'A maximum-severity (CVSS 9.8) security flaw in Enterprise Cloud Gateway exposes core perimeter infrastructure to unauthorized remote compromise. Rapid mitigation is underway to eliminate exposure before active exploitation occurs.',
      key_points: [
        'Critical vulnerability enables unauthenticated root compromise across versions 4.2.0 through 4.9.1.',
        'Official security patch (KB-89104) and stable release (v4.9.2) are available immediately.',
        'Zero downtime expected when applying interim firewall ingress restrictions on port 8443.'
      ],
      recommendations: [
        'Authorize immediate change window for SecOps and IT infrastructure teams to deploy patch KB-89104.',
        'Enforce ingress isolation on perimeter ports until all gateway clusters are verified at version 4.9.2.',
        'Mandate an automated audit log review across all regional gateway deployments.'
      ]
    },
    infographic: {
      title: 'Vulnerability Impact & Mitigation Architecture: CVE-2026-4401',
      headline_stat: '9.8 / 10',
      data_callouts: [
        { metric: '9.8', label: 'CVSS Severity Rating' },
        { metric: 'v4.9.2', label: 'Target Safe Release' },
        { metric: 'KB-89104', label: 'Emergency Hotfix ID' },
        { metric: 'Port 8443', label: 'Critical Ingress Port' }
      ],
      visual_sections: [
        {
          header: 'Attack Vector Breakdown',
          bullet_points: [
            'Attacker transmits crafted HTTP headers over WAN',
            'Authentication module parses headers without validation',
            'Arbitrary binary executed with root-level OS permissions'
          ]
        },
        {
          header: 'Three-Tier Defense Protocol',
          bullet_points: [
            'Tier 1: Restrict Port 8443 ingress at perimeter firewall',
            'Tier 2: Deploy firmware upgrade 4.9.2 across cluster',
            'Tier 3: SIEM log query for /api/v2/auth/token anomalies'
          ]
        }
      ]
    },
    presentation: {
      title: 'Emergency Security Briefing: CVE-2026-4401 Gateway Remediation',
      slides: [
        {
          slide_number: 1,
          title: 'Threat Identification: CVE-2026-4401',
          content: [
            'Severity: CVSS 9.8 Critical (AV:N/AC:L/PR:N/UI:N)',
            'Affected Asset: Enterprise Cloud Gateway (v4.2.0 – 4.9.1)',
            'Exploitation Type: Unauthenticated Remote Code Execution'
          ],
          speaker_notes: 'Begin by stressing that this vulnerability does not require credentials or user interaction to exploit.'
        },
        {
          slide_number: 2,
          title: 'Technical Impact & Risk Exposure',
          content: [
            'Attack vector operates via specially crafted HTTP headers',
            'Code executes under root OS context on the gateway',
            'Potential for lateral network pivot into internal corporate databases'
          ],
          speaker_notes: 'Highlight that perimeter gateways bridge public traffic to internal services, making root access an extreme risk.'
        },
        {
          slide_number: 3,
          title: 'Action Plan & Deployment Timeline',
          content: [
            'Phase 1: Ingress port 8443 filtering deployed within 2 hours',
            'Phase 2: Firmware v4.9.2 / Patch KB-89104 rolling deployment',
            'Phase 3: Log verification and IOC hunting via SIEM'
          ],
          speaker_notes: 'Conclude with clear assignments of responsibility to Network Engineering and Security Operations.'
        }
      ]
    },
    video: {
      title: 'CVE-2026-4401 Urgent Security Action Brief (60s)',
      objective: 'Alert system administrators and SecOps teams to immediately patch Enterprise Cloud Gateway vulnerabilities.',
      script: 'Attention all infrastructure engineers: A critical remote code execution flaw rated 9.8 has been identified in Enterprise Cloud Gateway. Unauthenticated attackers can exploit authentication headers to gain root control. If you manage versions 4.2.0 through 4.9.1, execute patch KB-89104 or upgrade to 4.9.2 today, and restrict port 8443 ingress immediately.',
      scenes: [
        {
          scene_number: 1,
          visual: 'Red alert screen overlay displaying "CRITICAL VULNERABILITY CVE-2026-4401" with CVSS 9.8 meter.',
          audio_narration: 'A critical remote code execution vulnerability rated 9.8 has been uncovered in Enterprise Cloud Gateway.'
        },
        {
          scene_number: 2,
          visual: 'Network topology graphic showing unauthenticated HTTP header packet reaching gateway authentication component.',
          audio_narration: 'Attackers can exploit crafted HTTP headers to run commands with root OS privileges without valid credentials.'
        },
        {
          scene_number: 3,
          visual: 'Action checklist on screen highlighting firmware version 4.9.2, Patch KB-89104, and Port 8443 firewall block.',
          audio_narration: 'Deploy version 4.9.2 or hotfix KB-89104 now, and restrict port 8443 to internal traffic immediately.'
        }
      ],
      narration: 'Urgent security notice: Enterprise Cloud Gateway has a critical CVSS 9.8 vulnerability. Upgrade to 4.9.2 or apply patch KB-89104 without delay.',
      subtitles: [
        '[00:00] Critical alert: CVE-2026-4401 discovered in Enterprise Cloud Gateway.',
        '[00:15] CVSS score is 9.8 - unauthenticated remote code execution with root access.',
        '[00:32] Upgrade to version 4.9.2 or apply patch KB-89104 immediately.',
        '[00:48] Restrict ingress port 8443 to trusted internal subnets now.'
      ],
      visual_recommendations: [
        'Display high-contrast red warning badge for CVSS 9.8',
        'Use animated network packet diagram to visualize header exploit path',
        'Show clean three-step remediation checklist with download URL'
      ]
    }
  },
  research: {
    linkedin: {
      title: 'The Shift to Agentic Multi-Model AI Workflows in Enterprise (Q1 2026 Report)',
      content: `Autonomous AI workflows are undergoing a massive evolution.

According to latest data from Global Enterprise AI Research Group, enterprise adoption of multi-agent AI architectures grew 280% year-over-year.

Why? Because 74% of surveyed CTOs identified cross-format content repurposing (turning reports into slide decks, executive summaries, and multi-channel briefs) as their knowledge teams' primary productivity bottleneck.

Automated multi-format transformation platforms solve this:
• Reduces turnaround time from 4.5 hours down to under 90 seconds
• Sustains 95%+ factual fidelity across all derivative outputs
• Frees senior specialists from repetitive communication formatting

How is your engineering organization leveraging multi-agent workflows this year?`,
      hashtags: ['#ArtificialIntelligence', '#GenerativeAI', '#EnterpriseAI', '#Productivity', '#CTO']
    },
    twitter: {
      hook: '🚀 Enterprise adoption of multi-agent AI architectures is up 280% YoY. Here is the biggest finding from Q1 2026 research:',
      tweets: [
        {
          index: 1,
          text: '1/4 🚀 Enterprise adoption of multi-agent AI architectures grew 280% YoY, shifting from single-prompt chatbots to automated multi-stage pipelines.'
        },
        {
          index: 2,
          text: '2/4 ⏱️ The Bottleneck: 74% of CTOs report that cross-format content repurposing (converting research into decks, executive summaries & posts) is their knowledge teams #1 time sink.'
        },
        {
          index: 3,
          text: '3/4 ⚡ The Solution: Automated multi-format AI platforms slash asset generation from 4.5 hours to under 90 seconds, all while preserving 95%+ factual fidelity.'
        },
        {
          index: 4,
          text: '4/4 The future of enterprise productivity is agentic content synthesis. How is your team adapting? #GenerativeAI #AI #TechTrends'
        }
      ]
    },
    advisory: {
      advisory_id: 'AI-TECH-2026-01',
      severity: 'INFORMATIONAL / STRATEGIC',
      title: 'Enterprise Multi-Agent Workflow Adoption Advisory',
      affected_systems: [
        'Knowledge Management Systems',
        'Content Publishing Pipelines',
        'Executive Communication Workflows'
      ],
      impact: 'Failure to adopt automated multi-format synthesis leads to 4.5x higher turnaround latency on enterprise communication assets compared to industry peers.',
      mitigation_steps: [
        'Pilot agentic transformation pipelines for research paper and advisory dissemination.',
        'Standardize on structured JSON output schemas across all downstream communication channels.',
        'Establish automated factual verification gates to maintain 95%+ fidelity benchmarks.'
      ]
    },
    executive: {
      title: 'Executive Briefing: Accelerating Knowledge Velocity via Multi-Agent AI Pipelines',
      summary: 'Research from Q1 2026 reveals enterprise multi-agent AI adoption accelerated 280% YoY. Automated content transformation platforms reduce communication asset turnaround from 4.5 hours down to 90 seconds with 95%+ factual precision, addressing the top operational time-sink reported by 74% of CTOs.',
      key_points: [
        'Adoption grew 280% YoY as organizations move from manual copy adaptation to automated synthesis.',
        'Content repurposing is identified by 74% of CTOs as the largest operational drain on strategic teams.',
        'Speed improves by ~99% (4.5 hours down to <90 seconds per communication asset).'
      ],
      recommendations: [
        'Evaluate multi-format AI transformation pipelines for cross-functional knowledge distribution.',
        'Integrate NLP extraction layers prior to LLM generation to guarantee factual consistency.',
        'Incorporate multi-channel export tooling for executive briefings, social channels, and presentation decks.'
      ]
    },
    infographic: {
      title: 'The Enterprise Multi-Agent Revolution at a Glance',
      headline_stat: '+280% YoY Growth',
      data_callouts: [
        { metric: '+280%', label: 'Multi-Agent Adoption Growth' },
        { metric: '74%', label: 'CTOs Citing Repurposing As #1 Bottleneck' },
        { metric: '<90 sec', label: 'Turnaround Time (vs 4.5 hrs)' },
        { metric: '95%+', label: 'Verified Factual Fidelity' }
      ],
      visual_sections: [
        {
          header: 'The Knowledge Repurposing Challenge',
          bullet_points: [
            '4.5 hours spent manually converting single research papers',
            'Context lost between technical authors and marketing / PR',
            'Delayed time-to-market for critical business advisories'
          ]
        },
        {
          header: 'The Automated AI Synthesis Advantage',
          bullet_points: [
            'Unified pipeline transforms one source into 7+ communication formats',
            'Sub-90 second generation cycle with real-time NLP fact extraction',
            'Preserves enterprise domain fidelity and stylistic alignment'
          ]
        }
      ]
    },
    presentation: {
      title: 'Strategic Briefing: The Multi-Agent AI Content Transformation Paradigm',
      slides: [
        {
          slide_number: 1,
          title: 'The Enterprise Productivity Dilemma',
          content: [
            'High-value research and advisories are trapped in monolithic PDFs',
            '74% of CTOs identify manual content repurposing as #1 productivity drain',
            'Average knowledge team spends 4.5 hours adapting a single document'
          ],
          speaker_notes: 'Set the stage by highlighting how much executive and technical time is wasted re-formatting existing knowledge.'
        },
        {
          slide_number: 2,
          title: 'The Agentic Solution & Metrics',
          content: [
            'Multi-agent architecture adoption grew 280% YoY in 2026',
            'Turnaround slashed from 4.5 hours to under 90 seconds',
            'Measured factual fidelity exceeds 95% across derivative channels'
          ],
          speaker_notes: 'Present the quantitative breakthroughs: dramatic speed increases without sacrificing factual precision.'
        },
        {
          slide_number: 3,
          title: 'Architecture Blueprint & Next Steps',
          content: [
            'Pipeline: Source -> Ingestion -> NLP -> Context Engine -> LLM -> Multi-Artifacts',
            'Immediate step: integrate automated synthesis into technical communication workflows'
          ],
          speaker_notes: 'Conclude with actionable recommendations on deploying the pipeline within internal business units.'
        }
      ]
    },
    video: {
      title: 'The 90-Second Knowledge Shift: Enterprise AI (60s)',
      objective: 'Demonstrate how autonomous multi-format AI synthesis eliminates manual content repurposing bottlenecks.',
      script: 'Imagine turning a 20-page research briefing into an executive summary, slide deck, LinkedIn post, and video package in under 90 seconds. 74% of CTOs say repurposing content is their team’s single biggest time sink. Multi-agent AI architectures are changing that, delivering 280% growth and 95% factual fidelity. Welcome to automated content transformation.',
      scenes: [
        {
          scene_number: 1,
          visual: 'Split screen comparing traditional manual document drafting (4.5 hours clock) vs automated AI synthesis (90 seconds).',
          audio_narration: 'Imagine turning a 20-page briefing into multi-channel communication assets in under 90 seconds.'
        },
        {
          scene_number: 2,
          visual: 'Dynamic bar chart showing 280% year-over-year enterprise multi-agent adoption surge.',
          audio_narration: 'Enterprise multi-agent adoption jumped 280% this year to solve the content repurposing bottleneck.'
        },
        {
          scene_number: 3,
          visual: 'Flow visualization showing one input splitting seamlessly into LinkedIn, Presentations, and Advisories.',
          audio_narration: 'One source of truth, infinite high-impact formats, with guaranteed factual fidelity.'
        }
      ],
      narration: 'Autonomous AI synthesis transforms technical knowledge into executive, social, and visual formats in seconds with 95% fidelity.',
      subtitles: [
        '[00:00] Manual content repurposing drains 4.5 hours per asset.',
        '[00:18] 74% of surveyed CTOs cite cross-format adaptation as top bottleneck.',
        '[00:35] Automated multi-agent platforms reduce delivery time to under 90 seconds.',
        '[00:50] Deliver multi-channel impact without losing factual fidelity.'
      ],
      visual_recommendations: [
        'Use side-by-side animated countdown timers (4.5h vs 90s)',
        'Display clean floating cards representing LinkedIn, Slides, and Executive Briefs',
        'Incorporate high-tech glowing particle pipeline visualization'
      ]
    }
  }
};

export function getMockNlpData(content) {
  const isResearch = content.toLowerCase().includes('agentic') || content.toLowerCase().includes('research') || content.toLowerCase().includes('findings');
  if (isResearch) return DEMO_NLP_INSIGHTS.research;

  const isAdvisory = content.toLowerCase().includes('advisory') || content.toLowerCase().includes('cve') || content.toLowerCase().includes('vulnerability');
  if (isAdvisory) return DEMO_NLP_INSIGHTS.advisory;

  // Dynamic fallback for custom user-pasted text
  const words = content.trim().split(/\s+/).filter((w) => w.length > 4);
  const uniqueWords = [...new Set(words.map((w) => w.replace(/[^a-zA-Z0-9]/g, '')))].slice(0, 8);
  const lines = content.split('\n').map((l) => l.trim()).filter((l) => l.length > 20);

  return {
    topic: 'Automated Knowledge Processing & Synthesis',
    contentType: 'User Submitted Source Document',
    detectedTone: 'Analytical & Informative',
    confidenceScore: 94.5,
    keywords: uniqueWords.length ? uniqueWords : ['content transformation', 'knowledge', 'synthesis', 'intelligence', 'automated pipeline'],
    entities: [
      { name: 'Source Input Document', type: 'DOCUMENT' },
      { name: 'GenAI Engine', type: 'SYSTEM' },
      { name: 'Target Audience Persona', type: 'STAKEHOLDER' }
    ],
    keyFacts: lines.length >= 3 ? lines.slice(0, 4) : [
      'Primary thesis established in source content paragraph 1.',
      'Key contextual parameters extracted for multi-channel adaptation.',
      'Core message structured for high-fidelity communication synthesis.'
    ],
    summaryContext: `Structured semantic extraction of ${content.trim().split(/\s+/).length} words, ready for context building and multi-format LLM generation.`
  };
}

export function getMockOutputs(content, selectedTypes, settings, nlpData) {
  const isResearch = content.toLowerCase().includes('agentic') || content.toLowerCase().includes('research') || content.toLowerCase().includes('findings');
  const baseOutputs = isResearch ? DEMO_STRUCTURED_OUTPUTS.research : DEMO_STRUCTURED_OUTPUTS.advisory;

  // Return base outputs if advisory/research, else construct customized fallback
  if (isResearch || content.toLowerCase().includes('advisory') || content.toLowerCase().includes('cve')) {
    return baseOutputs;
  }

  const titleSnippet = content.trim().slice(0, 60) || 'Synthesized Communication Artefact';
  const customOutputs = {};

  if (selectedTypes.includes('linkedin')) {
    customOutputs.linkedin = {
      title: `Key Takeaways: ${titleSnippet}`,
      content: `Here are the essential insights synthesized from the latest source update:\n\n• ${nlpData.keyFacts[0] || 'Strategic development noted.'}\n• ${nlpData.keyFacts[1] || 'Impact evaluated across key stakeholders.'}\n\nTailored for ${settings.audience} with a ${settings.tone.toLowerCase()} focus.\n\nWhat are your thoughts on this approach?`,
      hashtags: ['#GenAI', '#KnowledgeManagement', '#Innovation', '#DigitalTransformation']
    };
  }

  if (selectedTypes.includes('twitter')) {
    customOutputs.twitter = {
      hook: `Essential insights on ${titleSnippet} (Thread 🧵)`,
      tweets: [
        { index: 1, text: `1/3 💡 Key update: ${titleSnippet} — tailored for ${settings.audience}.` },
        { index: 2, text: `2/3 🔍 Fact: ${nlpData.keyFacts[0] || 'Core takeaway analyzed via NLP pipeline.'}` },
        { index: 3, text: `3/3 🎯 Objective: ${settings.objective}. More updates to follow. #GenAI #Tech` }
      ]
    };
  }

  if (selectedTypes.includes('advisory')) {
    customOutputs.advisory = {
      advisory_id: 'ADV-CUSTOM-001',
      severity: 'NOTICE / ACTION REQUIRED',
      title: `Operational Notice: ${titleSnippet}`,
      affected_systems: ['Core Business Workflows', 'Stakeholder Communications'],
      impact: `Information tailored specifically for ${settings.audience} with ${settings.detailLevel.toLowerCase()} granularity.`,
      mitigation_steps: [
        'Review the key facts highlighted in the NLP analysis panel.',
        'Distribute targeted communication briefs to appropriate internal owners.',
        'Monitor stakeholder response metrics and adapt subsequent releases.'
      ]
    };
  }

  if (selectedTypes.includes('executive')) {
    customOutputs.executive = {
      title: `Executive Briefing: ${titleSnippet}`,
      summary: nlpData.summaryContext,
      key_points: nlpData.keyFacts,
      recommendations: [
        `Align functional leadership with the stated objective: ${settings.objective}.`,
        `Maintain continuous factual oversight across communication channels.`,
        `Adopt automated transformation pipelines to accelerate knowledge distribution.`
      ]
    };
  }

  if (selectedTypes.includes('infographic')) {
    customOutputs.infographic = {
      title: `Visual Data Summary: ${titleSnippet}`,
      headline_stat: `${nlpData.confidenceScore}% NLP Confidence`,
      data_callouts: [
        { metric: `${content.trim().split(/\s+/).length}`, label: 'Source Word Count' },
        { metric: `${nlpData.keywords.length}`, label: 'Key Terms Extracted' },
        { metric: `${nlpData.keyFacts.length}`, label: 'Core Facts Verified' },
        { metric: `${settings.language}`, label: 'Target Language' }
      ],
      visual_sections: [
        {
          header: 'Core Analytical Findings',
          bullet_points: nlpData.keyFacts
        },
        {
          header: 'Target Execution Strategy',
          bullet_points: [
            `Audience Persona: ${settings.audience}`,
            `Stylistic Register: ${settings.tone}`,
            `Strategic Goal: ${settings.objective}`
          ]
        }
      ]
    };
  }

  if (selectedTypes.includes('presentation')) {
    customOutputs.presentation = {
      title: `Deck: ${titleSnippet}`,
      slides: [
        {
          slide_number: 1,
          title: 'Executive Context & Objectives',
          content: [
            `Primary Objective: ${settings.objective}`,
            `Target Persona: ${settings.audience}`,
            `Tone & Voice: ${settings.tone}`
          ],
          speaker_notes: 'Introduce the core reason for briefing and set the stage for detailed findings.'
        },
        {
          slide_number: 2,
          title: 'Key Facts & Findings',
          content: nlpData.keyFacts,
          speaker_notes: 'Walk the executive committee through the NLP-verified facts line by line.'
        },
        {
          slide_number: 3,
          title: 'Actionable Recommendations',
          content: [
            'Immediate execution of priority deliverables',
            'Cross-functional alignment across stakeholder groups',
            'Continuous performance reporting'
          ],
          speaker_notes: 'Conclude with explicit decisions required from the audience.'
        }
      ]
    };
  }

  if (selectedTypes.includes('video')) {
    customOutputs.video = {
      title: `Video Brief: ${titleSnippet}`,
      objective: settings.objective,
      script: `Welcome. Today we examine an essential update: ${nlpData.summaryContext}. As we address ${settings.audience}, our priority is clear: ${settings.objective}. Thank you for watching.`,
      scenes: [
        {
          scene_number: 1,
          visual: 'Title card with glowing logo and core topic headline.',
          audio_narration: `Today we examine an essential update regarding ${nlpData.topic}.`
        },
        {
          scene_number: 2,
          visual: 'Animated bullet callouts displaying the verified facts.',
          audio_narration: nlpData.keyFacts[0] || 'Core takeaway highlighted for stakeholders.'
        },
        {
          scene_number: 3,
          visual: 'Concluding call-to-action slide with resource links and next steps.',
          audio_narration: `This briefing is aligned with our commitment to ${settings.objective}.`
        }
      ],
      narration: `Full audio transcript crafted for a ${settings.tone.toLowerCase()} presentation style.`,
      subtitles: [
        `[00:00] Briefing on ${nlpData.topic}.`,
        `[00:15] Key finding: ${nlpData.keyFacts[0] || 'Analysis complete.'}`,
        `[00:30] Next steps and strategic alignment.`
      ],
      visual_recommendations: [
        'Use corporate branded color palette with high-contrast text overlays',
        'Incorporate kinetic typography for key statistics',
        'Include clear closing banner with call to action'
      ]
    };
  }

  return customOutputs;
}
