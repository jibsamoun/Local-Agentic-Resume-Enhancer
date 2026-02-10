import { useState } from "react";
import type { BulletRewrite } from "../types";
import { ValidationFeedback } from "./ValidationFeedback";

interface RewriteResultsProps {
  results: BulletRewrite[];
}

export function RewriteResults({ results }: RewriteResultsProps) {
  const [copiedIndex, setCopiedIndex] = useState<string | null>(null);

  if (results.length === 0) return null;

  async function copyToClipboard(text: string, id: string) {
    try {
      await navigator.clipboard.writeText(text);
      setCopiedIndex(id);
      setTimeout(() => setCopiedIndex(null), 2000);
    } catch (err) {
      console.error('Failed to copy:', err);
    }
  }

  return (
    <div className="rewrite-results">
      <div className="results-header">
        <h2>Enhanced Bullets</h2>
        <div className="results-count">{results.length} {results.length === 1 ? 'bullet' : 'bullets'} rewritten</div>
      </div>

      {results.map((result, index) => (
        <div key={index} className="bullet-result">
          <div className="result-number">#{index + 1}</div>
          
          <div className="original-section">
            <div className="section-label">Original</div>
            <p className="original-text">{result.original_bullet}</p>
          </div>

          <ValidationFeedback validation={result.validation} />

          {result.variants.length > 0 && (
            <div className="variants-section">
              <div className="section-label">Variants</div>
              <div className="variants-grid">
                {result.variants.map((variant, vIndex) => {
                  const copyId = `${index}-${vIndex}`;
                  const isCopied = copiedIndex === copyId;
                  
                  return (
                    <div key={vIndex} className={`variant variant-${variant.variant_type}`}>
                      <div className="variant-header">
                        <span className="variant-type">
                          {formatVariantType(variant.variant_type)}
                        </span>
                        <button
                          className="copy-button"
                          onClick={() => copyToClipboard(variant.text, copyId)}
                          title="Copy to clipboard"
                        >
                          {isCopied ? (
                            <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                              <path d="M13 4L6 11L3 8" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
                            </svg>
                          ) : (
                            <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                              <rect x="5.5" y="5.5" width="8" height="8" rx="1" stroke="currentColor" strokeWidth="1.5"/>
                              <path d="M10.5 5.5V3.5a1 1 0 00-1-1h-7a1 1 0 00-1 1v7a1 1 0 001 1h2" stroke="currentColor" strokeWidth="1.5"/>
                            </svg>
                          )}
                        </button>
                      </div>
                      <p className="variant-text">{variant.text}</p>
                    </div>
                  );
                })}
              </div>
            </div>
          )}

          {result.follow_up_questions.length > 0 && (
            <div className="follow-up-section">
              <div className="section-label">
                <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                  <circle cx="8" cy="8" r="6.5" stroke="currentColor" strokeWidth="1.5"/>
                  <path d="M8 11v.5M8 5v4" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"/>
                </svg>
                Questions to strengthen this bullet
              </div>
              <ul className="follow-up-list">
                {result.follow_up_questions.map((question, qIndex) => (
                  <li key={qIndex}>{question}</li>
                ))}
              </ul>
            </div>
          )}
        </div>
      ))}
    </div>
  );
}

function formatVariantType(type: string): string {
  const labels: Record<string, string> = {
    impact_first: "Impact First",
    scope_first: "Scope First",
    tech_first: "Tech First",
  };
  return labels[type] || type;
}