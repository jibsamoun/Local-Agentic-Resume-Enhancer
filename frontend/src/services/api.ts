import axios from "axios";
import type { RewriteRequest, RewriteResponse, ValidationResponse } from "../types";

const API_BASE_URL = "http://localhost:8000/api";

export async function rewriteBullets(request: RewriteRequest): Promise<RewriteResponse> {
    const response = await axios.post<RewriteResponse>(
        `${API_BASE_URL}/bullets/rewrite`,  
        request
    );
    return response.data;
}

export async function validateBullets(request: RewriteRequest): Promise<ValidationResponse> {
    const response = await axios.post<ValidationResponse>(
        `${API_BASE_URL}/bullets/validate`,
        request
    );
    return response.data;
}