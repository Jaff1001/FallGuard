import { History, AlertTriangle, Activity, CheckCircle2 } from "lucide-react";

export type EventType = "info" | "normal" | "alert" | "system";

export interface LogEvent {
  time: string;
  message: string;
  type: EventType;
}

const MOCK_EVENTS: LogEvent[] = [
  { time: "11:02", message: "Alert: Fall detected in Living Room", type: "alert" },
  { time: "10:58", message: "Posture analysis: sitting", type: "info" },
  { time: "10:51", message: "Normal posture detected", type: "normal" },
  { time: "10:47", message: "Subject identified in frame", type: "info" },
];

export function EventLog({ events = MOCK_EVENTS }: { events?: LogEvent[] }) {
  return (
    <div className="flex flex-col rounded-xl border border-gray-200 bg-white shadow-sm">
      <div className="flex items-center justify-between border-b border-gray-100 px-5 py-4">
        <div className="flex items-center gap-2 text-xs font-bold uppercase tracking-wide text-blue-500">
          <History className="h-4 w-4" />
          Registro de Eventos
        </div>
        <span className="flex h-5 w-5 items-center justify-center rounded-full bg-blue-100 text-[10px] font-bold text-blue-600">
          7
        </span>
      </div>
      
      <div className="flex-1 px-2 pt-2">
        <ul className="space-y-1">
          {events.map((e, i) => (
            <li key={i} className={`flex items-start gap-3 rounded-lg px-3 py-2.5 ${e.type === 'alert' ? 'bg-red-50' : ''}`}>
              <EventIcon type={e.type} />
              <div className="min-w-0 flex-1">
                <p className={`truncate text-sm font-medium ${e.type === 'alert' ? 'text-red-600' : 'text-gray-700'}`}>
                  {e.message}
                </p>
                <p className="mt-0.5 text-xs text-gray-500">{e.time}</p>
              </div>
            </li>
          ))}
        </ul>
      </div>

      <div className="p-4 border-t border-gray-100 mt-2">
        <button className="w-full rounded-lg border border-gray-200 bg-white py-2.5 text-xs font-semibold text-gray-600 transition-colors hover:bg-gray-50">
          Ver Historial Completo
        </button>
      </div>
    </div>
  );
}

function EventIcon({ type }: { type: EventType }) {
  const cls = "h-4 w-4 mt-0.5 shrink-0";
  switch (type) {
    case "alert":
      return <AlertTriangle className={`${cls} text-red-500`} />;
    case "normal":
      return <CheckCircle2 className={`${cls} text-green-500`} />;
    default:
      return <Activity className={`${cls} text-gray-400`} />;
  }
}