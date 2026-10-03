export default function Footer() {
  return (
    <footer className="dashboard-footer">
      <div className="footer-content">
        <div className="footer-left">
          <span className="footer-brand">GenAI Content Transformation Platform</span>
          <span className="footer-separator">•</span>
          <span className="footer-tagline">Multi-channel AI synthesis &amp; format adaptation</span>
        </div>
        <div className="footer-right">
          <span className="tech-badge">Python 3.10</span>
          <span className="tech-badge">FastAPI</span>
          <span className="tech-badge">React 19</span>
          <span className="tech-badge">Vite</span>
          <span className="tech-badge">MongoDB 8</span>
          <span className="tech-badge">Docker</span>
        </div>
      </div>
    </footer>
  );
}
