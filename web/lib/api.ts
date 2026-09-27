// API client for RecommendationOS backend
export const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8080";

export interface Product {
  id: string;
  item_id_numeric: number;
  title: string;
  description?: string;
  price: number;
  rating: number;
  reviews_count: number;
  badge?: string;
  image_url?: string;
  in_stock: boolean;
  popularity_score: number;
  category_id?: string;
}

export interface Category {
  id: string;
  name: string;
  slug: string;
  icon?: string;
  color?: string;
}

export interface RecommendationItem {
  item_id: number;
  title: string;
  category: string;
  price: number;
  rating: number;
  badge?: string;
  image_url?: string;
  in_stock: boolean;
  score: number;
  rank: number;
  source: string;
  reason?: string;
}

export interface RecommendationResponse {
  user_id: string;
  organization_id: string;
  cold_start: boolean;
  strategy: string;
  model_version: string;
  variant?: string;
  latency_ms: number;
  cache_hit: boolean;
  recommendations: number[];
  detailed_recommendations: RecommendationItem[];
  user_features?: {
    total_views: number;
    total_clicks: number;
    total_purchases: number;
  };
  explanation?: string;
}

export interface AnalyticsOverview {
  total_products: number;
  total_users: number;
  total_events: number;
  recommendation_requests_today: number;
  avg_latency_ms: number;
  overall_ctr: number;
  conversion_rate: number;
  cold_start_rate: number;
  cache_hit_rate: number;
  active_experiments: number;
  current_model: string;
}

export interface ModelVersion {
  name: string;
  version: string;
  stage: string;
  run_id?: string;
  metrics?: Record<string, any>;
  created_at?: string;
}

export interface Experiment {
  id: string;
  name: string;
  status: string;
  variant_a_model: string;
  variant_b_model: string;
  traffic_split_b: number;
  total_assignments: number;
  variant_a_impressions: number;
  variant_b_impressions: number;
  variant_a_clicks: number;
  variant_b_clicks: number;
  variant_a_ctr: number;
  variant_b_ctr: number;
  statistically_significant: boolean;
  p_value?: number;
  created_at: string;
}

export interface ApiKeyItem {
  id: string;
  name: string;
  key_prefix: string;
  scopes: string[];
  last_used_at?: string;
  is_revoked: boolean;
  created_at: string;
  secret_key?: string;
}

// User personas for live simulation
export const TEST_PERSONAS = [
  { id: "0", name: "Alex Chen", role: "Audiophile & Music Producer", segment: "Audio & Hi-Fi Gear", avatar: "🎧" },
  { id: "42", name: "Sarah Jenkins", role: "Tech Creator & Streamer", segment: "Cameras, Lights & Studio Gear", avatar: "🎙️" },
  { id: "89", name: "Marcus Vance", role: "Workplace Minimalist", segment: "Displays, Docks & Ergonomics", avatar: "💻" },
  { id: "999", name: "Elena Rostova", role: "New Visitor", segment: "Cold-Start (Popularity Fallback)", avatar: "✨" },
];

export async function fetchApi<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
  const url = `${API_BASE_URL}${endpoint}`;
  const rawToken = typeof window !== "undefined" ? localStorage.getItem("reco_token") : null;
  const token = (rawToken && rawToken !== "null" && rawToken !== "undefined" && rawToken.length > 20) ? rawToken : null;
  const headers: Record<string, string> = {
    "Content-Type": "application/json",
    ...(options.headers as Record<string, string>),
  };
  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  } else if (!headers["Authorization"]) {
    headers["Authorization"] = "Bearer reco_live_demo123456789abcdef01234567";
  }

  try {
    let res = await fetch(url, { ...options, headers });
    if (res.status === 401 && token) {
      if (typeof window !== "undefined") {
        localStorage.removeItem("reco_token");
      }
      headers["Authorization"] = "Bearer reco_live_demo123456789abcdef01234567";
      res = await fetch(url, { ...options, headers });
    }
    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: res.statusText }));
      throw new Error(err.detail || `Request failed with status ${res.status}`);
    }
    return res.json();
  } catch (error) {
    console.error(`Fetch error for ${endpoint}:`, error);
    throw error;
  }
}

// Products
export const getProducts = (category?: string, search?: string) => {
  let q = "/v1/products?limit=50";
  if (category && category !== "All") q += `&category_name=${encodeURIComponent(category)}`;
  if (search) q += `&search=${encodeURIComponent(search)}`;
  return fetchApi<Product[]>(q);
};

export const getProductById = (id: string | number) => fetchApi<Product>(`/v1/products/${id}`);
export const getCategories = () => fetchApi<Category[]>("/v1/products/categories");

// Recommendations
export const getRecommendations = (userId: string, disableCache: boolean = false) =>
  fetchApi<RecommendationResponse>(`/v1/recommendations?user_id=${userId}&limit=10${disableCache ? '&disable_cache=true' : ''}`);

export const getSimilarProducts = (productId: string | number) =>
  fetchApi<RecommendationItem[]>(`/v1/similar/${productId}?limit=4`);

// Events
export const sendEvent = (userId: string, itemId: number, eventType: string, metadata?: any) =>
  fetchApi<{ id: string; event_type: string; reward: number }>("/v1/events", {
    method: "POST",
    body: JSON.stringify({ user_id: userId, item_id: itemId, event_type: eventType, metadata }),
  });

export const getEvents = (limit: number = 30) =>
  fetchApi<any[]>(`/v1/events?limit=${limit}`);

// Analytics
export const getAnalyticsOverview = () => fetchApi<AnalyticsOverview>("/v1/analytics/overview");

// Models
export const getModels = () => fetchApi<ModelVersion[]>("/v1/models");
export const deployModel = (version: string, stage: string = "Production") =>
  fetchApi<ModelVersion>("/v1/models/deploy", {
    method: "POST",
    body: JSON.stringify({ version, target_stage: stage }),
  });
export const rollbackModel = () => fetchApi<ModelVersion>("/v1/models/rollback", { method: "POST" });

// Experiments
export const getExperiments = () => fetchApi<Experiment[]>("/v1/experiments");
export const updateExperiment = (id: string, data: Partial<Experiment>) =>
  fetchApi<Experiment>(`/v1/experiments/${id}`, {
    method: "PATCH",
    body: JSON.stringify(data),
  });

// API Keys
export const getApiKeys = () => fetchApi<ApiKeyItem[]>("/v1/api-keys");
export const createApiKey = (name: string) =>
  fetchApi<ApiKeyItem>("/v1/api-keys", {
    method: "POST",
    body: JSON.stringify({ name }),
  });
export const revokeApiKey = (keyId: string) =>
  fetchApi<void>(`/v1/api-keys/${keyId}`, { method: "DELETE" });

// Health & System
export const getHealth = () => fetchApi<any>("/health");
export const getSystemStatus = () => fetchApi<any>("/api/system-status");
export const getEvaluationStats = () => fetchApi<any>("/api/evaluation-stats");
export const testDrift = (shiftMagnitude: number = 0.5) =>
  fetchApi<any>("/api/drift/test", {
    method: "POST",
    body: JSON.stringify({ shift_magnitude: shiftMagnitude }),
  });
export const triggerRetrain = () => fetchApi<any>("/api/retrain", { method: "POST" });
