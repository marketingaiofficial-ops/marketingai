import { Bot, KanbanSquare, LayoutTemplate, Magnet, Settings2, Workflow } from "lucide-react";

import type { Service } from "@/lib/content";

const icons = {
  settings: Settings2,
  kanban: KanbanSquare,
  workflow: Workflow,
  bot: Bot,
  magnet: Magnet,
  layout: LayoutTemplate,
} as const;

export function ServiceIcon({ name, className }: { name: Service["icon"]; className?: string }) {
  const Icon = icons[name];
  return <Icon className={className} aria-hidden="true" strokeWidth={1.75} />;
}
