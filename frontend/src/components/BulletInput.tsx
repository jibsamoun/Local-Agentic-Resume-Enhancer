import { useState } from "react";

interface BulletInputProps {
    onSubmit: (bullets: string[], jobDescription?: string) => void;
    isLoading: boolean;
}

export function BulletInput({ onSubmit, isLoading }: BulletInputProps) {
    const [bulletText, setBulletText] = useState("");
    const [jobDescription, setJobDescription] = useState("");

    function handleSubmit(e: React.FormEvent) {
        e.preventDefault();
        
        const bullets = bulletText
            .split("\n")
            .map(line => line.trim())
            .filter(line => line.length > 0);
        
        if (bullets.length === 0) return;
        
        onSubmit(bullets, jobDescription || undefined);
    }

    const bulletCount = bulletText.split("\n").filter(line => line.trim().length > 0).length;

    return (
        <form onSubmit={handleSubmit} className="bullet-input-form">
            <div className="input-section">
                <div className="label-row">
                    <label htmlFor="bullets">Resume Bullets</label>
                    <span className="input-hint">One per line</span>
                </div>
                <textarea
                    id="bullets"
                    value={bulletText}
                    onChange={(e) => setBulletText(e.target.value)}
                    placeholder="Led a team of 8 engineers to build a new microservices architecture&#10;Increased user engagement by 45% through data-driven feature optimization&#10;Managed $2M budget and delivered project 3 weeks ahead of schedule"
                    rows={6}
                    className="input-textarea"
                />
                {bulletCount > 0 && (
                    <div className="bullet-counter">
                        {bulletCount} {bulletCount === 1 ? 'bullet' : 'bullets'}
                    </div>
                )}
            </div>
            
            <div className="input-section">
                <div className="label-row">
                    <label htmlFor="jobDescription">Target Role</label>
                    <span className="input-hint optional-badge">Optional</span>
                </div>
                <textarea
                    id="jobDescription"
                    value={jobDescription}
                    onChange={(e) => setJobDescription(e.target.value)}
                    placeholder="Senior Product Manager at fintech startup focused on B2B payments and enterprise solutions..."
                    rows={4}
                    className="input-textarea"
                />
            </div>
            
            <button type="submit" disabled={isLoading || bulletCount === 0} className="submit-button">
                {isLoading ? (
                    <>
                        <span className="spinner"></span>
                        Rewriting...
                    </>
                ) : (
                    <>
                        <svg width="18" height="18" viewBox="0 0 18 18" fill="none">
                            <path d="M14 9.5l-4 4m0 0l-4-4m4 4V4.5M3.5 14.5h11" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
                        </svg>
                        Enhance Bullets
                    </>
                )}
            </button>
        </form>
    );
}