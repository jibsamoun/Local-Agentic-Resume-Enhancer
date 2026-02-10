export type VariantType = 'impact_first' | 'scope_first' | 'tech_first';

export interface RewriteRequest {
    bullets: string[];
    job_description?: string;
}

export interface RewriteVariant {
    variant_type: VariantType;
    text: string;
}

export interface ValidationResponse {
    warnings: string[];
    errors: string[];
}

export interface BulletRewrite {
    original_bullet: string;
    variants: RewriteVariant[];
    follow_up_questions: string[];
    validation: ValidationResponse | null;
}

export interface RewriteResponse {
    results: BulletRewrite[];
}