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
