import { Header } from "./Header";
import { CameraFeed } from "./CameraFeed";
import { StatusCard } from "./StatusCard";
import { MetricsCard } from "./MetricsCard";
import { EventLog } from "./EventLog";
import { Footer } from "./Footer";
import { useFallGuard } from "@/hooks/useFallGuard";

export function Dashboard() {
  const { telemetry, events } = useFallGuard();

  return (
    <div className="flex min-h-screen flex-col bg-[#F8FAFC]">
      <Header />

      <main className="mx-auto w-full max-w-[1600px] flex-1 px-6 py-8">
        <div className="grid grid-cols-1 gap-6 lg:grid-cols-12">
          <div className="lg:col-span-8">
            <CameraFeed />
          </div>

          <aside className="flex flex-col gap-5 lg:col-span-4">
            <StatusCard
              status={telemetry.status}
              since={telemetry.stable_since ?? "12 min"}
            />
            <MetricsCard
              fps={telemetry.fps}
              latencyMs={telemetry.latency_ms}
              confidence={telemetry.confidence}
            />
            <EventLog events={events} />
          </aside>
        </div>
      </main>

      <Footer />
    </div>
  );
}