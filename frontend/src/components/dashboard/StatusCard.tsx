import { Heart, CheckCircle2, AlertTriangle } from "lucide-react";
import type { FallStatus } from "@/lib/fallguard-api";

export function StatusCard({
  status = "normal" as FallStatus,
  since = "12 min",
}: {
  status?: FallStatus;
  since?: string;
}) {
  const isFall = status === "fall";
  
  return (
    <div className="rounded-xl border border-gray-200 bg-white p-5 shadow-sm">
      <div className="flex items-center gap-2 text-xs font-bold uppercase tracking-wide text-blue-500">
        <Heart className="h-4 w-4" />
        Estado del Paciente
      </div>
      
      <div className="mt-4 flex items-center gap-4">
        {isFall ? (
          <div className="rounded-full bg-red-50 p-2">
            <AlertTriangle className="h-10 w-10 text-red-500" />
          </div>
        ) : (
          <div className="rounded-full bg-green-50 p-2">
            <CheckCircle2 className="h-10 w-10 text-green-500" />
          </div>
        )}
        <div>
          <h2 className={`text-xl font-bold uppercase tracking-wide ${isFall ? "text-red-500" : "text-green-600"}`}>
            {isFall ? "Caída Detectada" : "Normal"}
          </h2>
          <p className="text-sm text-gray-500">
            {isFall ? "Atención inmediata requerida" : `Estable por ${since}`}
          </p>
        </div>
      </div>

      <div className="mt-6 flex items-center gap-3 border-t border-gray-100 pt-4">
        <span className="text-xs font-medium text-gray-500">Estado</span>
        <div className="h-2 flex-1 rounded-full bg-green-500"></div>
        <span className="text-xs font-bold text-green-600">OK</span>
      </div>
    </div>
  );
}