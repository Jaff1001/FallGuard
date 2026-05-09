import { Camera, CameraOff, Power, PersonStanding, Video, PlayCircle } from "lucide-react";
import { useState } from "react";
import { api, mjpegUrl } from "@/lib/fallguard-api";

export function CameraFeed() {
  const [running, setRunning] = useState(false);
  const [skeleton, setSkeleton] = useState(true);
  const [streamOk, setStreamOk] = useState(true);
  const [bust, setBust] = useState(0);

  const toggleCamera = async () => {
    const next = !running;
    setRunning(next);
    try {
      next ? await api.startCamera() : await api.stopCamera();
    } catch { /* error handling */ }
    setBust((n) => n + 1);
    setStreamOk(true);
  };

  const showVideo = running && streamOk;

  return (
    <section className="flex flex-col gap-4">
      {/* Contenedor del Monitor */}
      <div className="overflow-hidden rounded-xl border border-gray-200 bg-white shadow-sm">
        <div className="flex items-center justify-between border-b border-gray-100 px-4 py-3">
          <div className="flex items-center gap-2 text-gray-800">
            <Video className="h-4 w-4 text-blue-500" />
            <span className="text-sm font-semibold">Monitor Principal</span>
          </div>
          {running && streamOk && (
            <div className="flex items-center gap-1.5 text-xs font-bold text-red-500">
              <span className="h-2 w-2 rounded-full bg-red-500 animate-pulse" />
              REC
            </div>
          )}
        </div>

        <div className="relative flex aspect-[16/9] w-full items-center justify-center bg-[#Eef1f4]">
          {showVideo ? (
            <img
              key={bust}
              src={`${mjpegUrl()}?t=${bust}`}
              alt="Feed en vivo"
              className="absolute inset-0 h-full w-full object-cover"
              onError={() => setStreamOk(false)}
            />
          ) : (
            <div className="flex flex-col items-center text-center p-6">
              {!running ? (
                <>
                  <div className="mb-4 flex h-20 w-24 items-center justify-center rounded-xl bg-white shadow-sm border border-gray-100">
                    <CameraOff className="h-10 w-10 text-gray-400" />
                  </div>
                  <h3 className="text-base font-bold text-gray-800">Cámara Desactivada</h3>
                  <p className="mt-2 text-sm text-gray-500">
                    Utilice el control inferior para <strong className="text-green-600">INICIAR</strong> el monitoreo.
                  </p>
                </>
              ) : (
                <>
                  <div className="mb-4 flex h-20 w-24 items-center justify-center rounded-xl bg-white shadow-sm border border-gray-100 animate-pulse">
                    <Camera className="h-10 w-10 text-blue-500" />
                  </div>
                  <h3 className="text-base font-bold text-gray-800">Conectando al Stream...</h3>
                  <p className="mt-2 text-sm text-gray-500">
                    Asegúrese de que el backend esté corriendo en localhost:8000
                  </p>
                </>
              )}
            </div>
          )}
        </div>
      </div>

      {/* Toolbar */}
      <div className="flex flex-wrap items-center gap-3">
        {running ? (
          <button
            onClick={toggleCamera}
            className="inline-flex items-center gap-2 rounded-lg bg-red-600 px-6 py-2.5 text-sm font-bold text-white transition-all hover:bg-red-700 shadow-md"
          >
            <Power className="h-4 w-4" />
            Detener
          </button>
        ) : (
          <button
            onClick={toggleCamera}
            className="inline-flex items-center gap-2 rounded-lg bg-green-600 px-6 py-2.5 text-sm font-bold text-white transition-all hover:bg-green-700 shadow-md"
          >
            <PlayCircle className="h-4 w-4" />
            Iniciar Cámara
          </button>
        )}
        
        {/* Botón Skeleton */}
        <button
          onClick={() => setSkeleton(!skeleton)}
          className={`inline-flex items-center gap-2 rounded-lg border px-5 py-2.5 text-sm font-semibold shadow-sm transition-colors ${
            skeleton 
              ? "bg-blue-50 border-blue-200 text-blue-600 hover:bg-blue-100" 
              : "bg-white border-gray-200 text-gray-600 hover:bg-gray-50"
          }`}
        >
          <PersonStanding className="h-4 w-4" />
          {skeleton ? "Ocultar Skeleton" : "Mostrar Skeleton"}
        </button>
      </div>
    </section>
  );
}