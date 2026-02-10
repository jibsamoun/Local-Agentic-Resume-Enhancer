import type { ValidationResponse } from "../types";

interface ValidationFeedbackProps {
    validation: ValidationResponse | null;
}

export function ValidationFeedback({ validation }: ValidationFeedbackProps) {
    if (!validation) return null;

    const hasErrors = validation.errors.length > 0;
    const hasWarnings = validation.warnings.length > 0;

    if (!hasErrors && !hasWarnings) return null;

    return (
        <div className="validation-feedback">
            {hasErrors && (
                <div className="validation-section errors">
                    <div className="validation-header">
                        <svg width="18" height="18" viewBox="0 0 18 18" fill="none">
                            <circle cx="9" cy="9" r="7.5" stroke="currentColor" strokeWidth="1.5"/>
                            <path d="M9 5v4.5M9 12v.5" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"/>
                        </svg>
                        <h4>Issues Found</h4>
                    </div>
                    <ul className="validation-list">
                        {validation.errors.map((error, index) => (
                            <li key={index}>{error}</li>
                        ))}
                    </ul>
                </div>
            )}

            {hasWarnings && (
                <div className="validation-section warnings">
                    <div className="validation-header">
                        <svg width="18" height="18" viewBox="0 0 18 18" fill="none">
                            <path d="M9 2L2 15h14L9 2z" stroke="currentColor" strokeWidth="1.5" strokeLinejoin="round"/>
                            <path d="M9 7v3M9 12.5v.5" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"/>
                        </svg>
                        <h4>Suggestions</h4>
                    </div>
                    <ul className="validation-list">
                        {validation.warnings.map((warning, index) => (
                            <li key={index}>{warning}</li>
                        ))}
                    </ul>
                </div>
            )}
        </div>
    );
}