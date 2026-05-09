import { useEffect, useState } from "react";
import { Shield, Bell, Settings, Clock } from "lucide-react";

export function Header() {
  const [now, setNow] = useState<Date>(new Date());

  useEffect(() => {
    const id = setInterval(() => setNow(new Date()), 1000);
    return () => clearInterval(id);
  }, []);

  const time = now.toLocaleTimeString('es-ES', {
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
  });

  const date = now.toLocaleDateString('es-ES', {
    weekday: "long",
    day: "numeric",
    month: "long",
  }).replace(/^\w/, (c) => c.toUpperCase());

  return (
    <header className="sticky top-0 z-50 w-full border-b border-gray-200 bg-white shadow-sm">
      <div className="flex items-center justify-between px-6 py-3">

        {/* Brand */}
        <div className="flex items-center gap-3">
          <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-blue-600 text-white">
            <Shield className="h-6 w-6" />
          </div>
          <div className="flex flex-col leading-tight">
            <h1 className="text-xl font-bold text-gray-900">
              FallGuard
            </h1>
            <p className="text-[10px] font-semibold uppercase tracking-wider text-gray-500">
              Sistema de Monitoreo
            </p>
          </div>
        </div>


        {/* Date, Time & Icons */}
        <div className="flex items-center gap-6">
          <div className="flex items-center gap-3 rounded-md border border-gray-200 px-3 py-1.5 text-sm font-medium text-gray-600">
            <Clock className="h-4 w-4 text-gray-400" />
            <span className="font-mono">{time}</span>
            <span className="text-gray-300">|</span>
            <span className="capitalize">{date}</span>
          </div>
          
          <div className="flex items-center gap-4 text-gray-500">
            <button className="hover:text-gray-900 transition-colors"><Bell className="h-5 w-5" /></button>
            <button className="hover:text-gray-900 transition-colors"><Settings className="h-5 w-5" /></button>
          </div>
        </div>

      </div>
    </header>
  );
}