import { BarChart3 } from "lucide-react";

export function MetricsCard({
  fps = 29,
  latencyMs = 45,
  confidence = 98,
}: {
  fps?: number;
  latencyMs?: number;
  confidence?: number;
}) {
  return (
    <div className="rounded-xl border border-gray-200 bg-white p-5 shadow-sm">
      <div className="flex items-center gap-2 text-xs font-bold uppercase tracking-wide text-blue-500">
        <BarChart3 className="h-4 w-4" />
        Datos Técnicos
      </div>
      
      <div className="mt-4 grid grid-cols-3 gap-3">
        <MetricCard label="FPS" value={fps} unit="f/s" />
        <MetricCard label="LATENCIA" value={latencyMs} unit="ms" />
        <MetricCard label="CONFIANZA" value={confidence} unit="%" />
      </div>

      {/* Confidence progress bar */}
      <div className="mt-5">
        <div className="mb-2 flex items-center justify-between text-xs text-gray-500">
          <span className="flex items-center gap-1"><span className="text-blue-500">ⓘ</span> Nivel de Confianza IA</span>
          <span className="font-bold text-green-600">{confidence}%</span>
        </div>
        <div className="h-2.5 w-full overflow-hidden rounded-full bg-gray-100">
          <div
            className="h-full rounded-full bg-green-500 transition-all"
            style={{ width: `${confidence}%` }}
          />
        </div>
        <div className="mt-1.5 flex justify-between text-[10px] text-gray-400">
          <span>Bajo</span>
          <span>Medio</span>
          <span>Alto</span>
        </div>
      </div>
    </div>
  );
}

function MetricCard({ label, value, unit }: { label: string; value: number; unit: string }) {
  return (
    <div className="rounded-xl border border-gray-100 bg-white p-3 shadow-sm flex flex-col items-center justify-center text-center">
      <div className="mb-2 flex items-center gap-1.5 text-gray-500">
        <span className="text-[10px] font-bold uppercase tracking-wider">{label}</span>
      </div>
      <p className="font-mono text-xl font-bold text-gray-900">
        {value} <span className="text-xs font-medium text-gray-500">{unit}</span>
      </p>
    </div>
  );
}