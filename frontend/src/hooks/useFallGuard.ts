// Connects the dashboard to the FastAPI backend.
// Falls back to mocked data if the backend isn't reachable so the UI stays usable in dev.
import { useEffect, useRef, useState } from "react";
import {
  api,
  openTelemetrySocket,
  type ApiEvent,
  type Telemetry,
} from "@/lib/fallguard-api";

const MOCK_TELEMETRY: Telemetry = {
  status: "normal",
  fps: 29,
  latency_ms: 45,
  confidence: 98,
  stable_since: "12 min",
};

const MOCK_EVENTS: ApiEvent[] = [
  { time: "11:02", message: "Alert: Fall detected in Living Room", type: "alert" },
  { time: "10:58", message: "Posture analysis: sitting", type: "info" },
  { time: "10:51", message: "Normal posture detected", type: "normal" },
  { time: "10:47", message: "Subject identified in frame", type: "info" },
  { time: "10:45", message: "Normal posture detected", type: "normal" },
  { time: "10:43", message: "MediaPipe model loaded", type: "system" },
  { time: "10:42", message: "System Started", type: "system" },
];

export function useFallGuard() {
  const [telemetry, setTelemetry] = useState<Telemetry>(MOCK_TELEMETRY);
  const [events, setEvents] = useState<ApiEvent[]>(MOCK_EVENTS);
  const [connected, setConnected] = useState(false);
  const mockMode = useRef(false);

  useEffect(() => {
    let cancelled = false;

    // Initial REST fetch — if it fails, we stay in mock mode.
    (async () => {
      try {
        const [t, e] = await Promise.all([api.getTelemetry(), api.getEvents()]);
        if (cancelled) return;
        setTelemetry(t);
        setEvents(e);
      } catch {
        mockMode.current = true;
      }
    })();

    // Live stream
    const close = openTelemetrySocket(
      (msg) => {
        if (msg.telemetry) setTelemetry(msg.telemetry);
        if (msg.event)
          setEvents((prev) => [msg.event!, ...prev].slice(0, 50));
      },
      (ok) => setConnected(ok),
    );

    return () => {
      cancelled = true;
      close();
    };
  }, []);

  return { telemetry, events, connected, mockMode: mockMode.current };
}
