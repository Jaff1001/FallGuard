import { createFileRoute } from "@tanstack/react-router";
import { Dashboard } from "@/components/dashboard/Dashboard";

export const Route = createFileRoute("/")({
  head: () => ({
    meta: [
      { title: "FallGuard Enterprise — Edge AI Fall Detection" },
      {
        name: "description",
        content:
          "Real-time elderly fall detection dashboard powered by MediaPipe and on-device machine learning.",
      },
    ],
  }),
  component: Dashboard,
});
