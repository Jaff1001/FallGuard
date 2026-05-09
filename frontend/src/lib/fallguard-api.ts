// FastAPI client for the FallGuard Python backend.
// Configure the base URL via VITE_FALLGUARD_API (defaults to http://localhost:8000).

export const API_BASE =
  (typeof import.meta !== "undefined" && (import.meta as any).env?.VITE_FALLGUARD_API) ||
  "http://localhost:8000";

export const WS_BASE = API_BASE.replace(/^http/, "ws");

export type FallStatus = "normal" | "fall";

export interface Telemetry {
  status: FallStatus;
  fps: number;
  latency_ms: number;
  confidence: number; // 0-100
  stable_since?: string;
}

export interface ApiEvent {
  time: string; // "HH:MM"
  message: string;
  type: "info" | "normal" | "alert" | "system";
}

// ---- REST ----
async function req<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...init,
  });
  if (!res.ok) throw new Error(`${res.status} ${res.statusText}`);
  return res.json() as Promise<T>;
}

export const api = {
  getTelemetry: () => req<Telemetry>("/api/telemetry"),
  getEvents: () => req<ApiEvent[]>("/api/events"),
  startCamera: () => req<{ ok: boolean }>("/api/camera/start", { method: "POST" }),
  stopCamera: () => req<{ ok: boolean }>("/api/camera/stop", { method: "POST" }),
  setPrivacy: (enabled: boolean) =>
    req<{ ok: boolean }>("/api/camera/privacy", {
      method: "POST",
      body: JSON.stringify({ enabled }),
    }),
  setSkeleton: (enabled: boolean) =>
    req<{ ok: boolean }>("/api/camera/skeleton", {
      method: "POST",
      body: JSON.stringify({ enabled }),
    }),
};

// MJPEG stream URL for the live feed (FastAPI StreamingResponse).
export const mjpegUrl = () => `${API_BASE}/api/camera/stream`;

// ---- WebSocket ----
export function openTelemetrySocket(
  onMessage: (msg: { telemetry?: Telemetry; event?: ApiEvent }) => void,
  onStatus?: (connected: boolean) => void,
) {
  let ws: WebSocket | null = null;
  let retry: ReturnType<typeof setTimeout> | null = null;
  let closed = false;

  const connect = () => {
    try {
      ws = new WebSocket(`${WS_BASE}/ws`);
    } catch {
      onStatus?.(false);
      retry = setTimeout(connect, 2000);
      return;
    }
    ws.onopen = () => onStatus?.(true);
    ws.onclose = () => {
      onStatus?.(false);
      if (!closed) retry = setTimeout(connect, 2000);
    };
    ws.onerror = () => ws?.close();
    ws.onmessage = (e) => {
      try {
        onMessage(JSON.parse(e.data));
      } catch {
        /* ignore malformed payloads */
      }
    };
  };

  connect();
  return () => {
    closed = true;
    if (retry) clearTimeout(retry);
    ws?.close();
  };
}
