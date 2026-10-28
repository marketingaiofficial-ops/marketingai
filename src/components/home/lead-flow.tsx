"use client";

import * as React from "react";
import { AnimatePresence, motion, useReducedMotion } from "motion/react";
import {
  CalendarCheck,
  FileText,
  MessageCircle,
  PhoneMissed,
  Repeat,
  Sparkles,
  Target,
  UserCheck,
} from "lucide-react";

import { AnimatedBeam } from "@/components/ui/animated-beam";
import { LiveDot } from "@/components/ui/primitives";
import { cn } from "@/lib/utils";

/*
 * Signature visual: a lead arrives from any channel, the system replies, qualifies,
 * books and follows up. Built on the adapted Animated Beam. Events are illustrative
 * examples of what the system does, not real data, and are labelled as such.
 */

const sources = [
  { id: "form", label: "Website form", icon: FileText },
  { id: "wa", label: "WhatsApp", icon: MessageCircle },
  { id: "call", label: "Missed call", icon: PhoneMissed },
  { id: "ads", label: "Lead ad", icon: Target },
] as const;

const outcomes = [
  { id: "reply", label: "Instant reply", icon: Sparkles },
  { id: "qualify", label: "Qualified", icon: UserCheck },
  { id: "book", label: "Call booked", icon: CalendarCheck },
  { id: "follow", label: "Follow-up set", icon: Repeat },
] as const;

const events = [
  { source: "WhatsApp", text: "New enquiry received", stage: "New lead" },
  { source: "AI agent", text: "Replied and asked 3 qualifying questions", stage: "Contacted" },
  { source: "AI agent", text: "Budget and timeline captured", stage: "Qualified" },
  { source: "Calendar", text: "Strategy call booked for Thursday", stage: "Booked" },
  { source: "Workflow", text: "Reminder sequence scheduled", stage: "Nurture" },
];

type Tone = "light" | "dark";

export function LeadFlow({ tone = "light", className }: { tone?: Tone; className?: string }) {
  const containerRef = React.useRef<HTMLDivElement>(null);
  const hubRef = React.useRef<HTMLDivElement>(null);
  const sourceRefs = React.useMemo(() => sources.map(() => React.createRef<HTMLDivElement>()), []);
  const outcomeRefs = React.useMemo(() => outcomes.map(() => React.createRef<HTMLDivElement>()), []);
  const [ready, setReady] = React.useState(false);

  // Refs are filled after first paint; render beams once they exist.
  React.useEffect(() => setReady(true), []);

  const dark = tone === "dark";
  const beamColors = dark
    ? { pathColor: "var(--color-navy-700)", start: "var(--color-brand-300)", stop: "var(--color-brand-400)" }
    : { pathColor: "var(--color-line-strong)", start: "var(--color-brand-300)", stop: "var(--color-brand-500)" };

  return (
    <div className={cn("flex flex-col gap-4", className)}>
      <div
        ref={containerRef}
        className="relative grid grid-cols-[minmax(0,1fr)_auto_minmax(0,1fr)] items-center gap-x-5 sm:gap-x-12"
      >
        <ul className="flex flex-col gap-3" aria-label="Lead sources">
          {sources.map((s, i) => (
            <li key={s.id}>
              <Node
                ref={sourceRefs[i]}
                icon={s.icon}
                label={s.label}
                tone={tone}
              />
            </li>
          ))}
        </ul>

        <div
          ref={hubRef}
          className={cn(
            "relative z-10 grid size-16 place-items-center rounded-lg sm:size-24",
            dark
              ? "bg-brand-500 text-white shadow-[0_0_0_8px_rgb(31_79_255/0.15),0_0_48px_rgb(31_79_255/0.5)]"
              : "bg-navy-900 text-white shadow-[0_0_0_8px_rgb(31_79_255/0.08),0_16px_40px_-8px_rgb(10_22_51/0.45)]",
          )}
        >
          <div className="text-center">
            <span className="block text-[0.6875rem] font-semibold tracking-wide text-brand-50 uppercase">
              CRM
            </span>
            <span className="mt-0.5 block text-[0.8125rem] leading-tight font-semibold">
              + AI
            </span>
          </div>
        </div>

        <ul className="flex flex-col gap-3" aria-label="What happens next">
          {outcomes.map((o, i) => (
            <li key={o.id}>
              <Node
                ref={outcomeRefs[i]}
                icon={o.icon}
                label={o.label}
                tone={tone}
                accent
              />
            </li>
          ))}
        </ul>

        {ready &&
          sources.map((s, i) => (
            <AnimatedBeam
              key={`in-${s.id}`}
              containerRef={containerRef}
              fromRef={sourceRefs[i]}
              toRef={hubRef}
              curvature={(1.5 - i) * 18}
              duration={4.5}
              delay={i * 0.6}
              pathColor={beamColors.pathColor}
              gradientStartColor={beamColors.start}
              gradientStopColor={beamColors.stop}
            />
          ))}
        {ready &&
          outcomes.map((o, i) => (
            <AnimatedBeam
              key={`out-${o.id}`}
              containerRef={containerRef}
              fromRef={hubRef}
              toRef={outcomeRefs[i]}
              curvature={(1.5 - i) * -18}
              duration={4.5}
              delay={1.2 + i * 0.6}
              pathColor={beamColors.pathColor}
              gradientStartColor={beamColors.start}
              gradientStopColor={beamColors.stop}
            />
          ))}
      </div>

      <EventLog tone={tone} />
    </div>
  );
}

const Node = React.forwardRef<
  HTMLDivElement,
  { icon: React.ElementType; label: string; tone: Tone; accent?: boolean }
>(({ icon: Icon, label, tone, accent }, ref) => {
  const dark = tone === "dark";
  return (
    <div
      ref={ref}
      className={cn(
        "relative z-10 flex items-center gap-2.5 rounded-sm px-2.5 py-2 text-[0.8125rem] font-medium sm:px-3",
        dark
          ? "bg-navy-800 text-white ring-1 ring-navy-700"
          : "bg-white text-ink shadow-xs ring-1 ring-line",
      )}
    >
      <span
        aria-hidden="true"
        className={cn(
          "grid size-6 shrink-0 place-items-center rounded-xs [&_svg]:size-3.5",
          accent
            ? dark
              ? "bg-brand-500 text-white"
              : "bg-brand-500 text-white"
            : dark
              ? "bg-navy-700 text-brand-300"
              : "bg-paper-2 text-ink-muted",
        )}
      >
        <Icon />
      </span>
      <span className="truncate">{label}</span>
    </div>
  );
});
Node.displayName = "Node";

function EventLog({ tone }: { tone: Tone }) {
  const reduce = useReducedMotion();
  const [index, setIndex] = React.useState(0);
  const dark = tone === "dark";

  React.useEffect(() => {
    if (reduce) return;
    const t = window.setInterval(() => setIndex((i) => (i + 1) % events.length), 2600);
    return () => window.clearInterval(t);
  }, [reduce]);

  const e = events[index];
  return (
    <div
      className={cn(
        "flex items-center justify-between gap-3 rounded-sm px-3 py-2.5 text-[0.8125rem]",
        dark ? "bg-navy-950/60 ring-1 ring-navy-700" : "bg-paper ring-1 ring-line",
      )}
    >
      <div className="flex min-w-0 items-center gap-2.5">
        <LiveDot />
        <div className="relative h-5 min-w-0 flex-1 overflow-hidden">
          <AnimatePresence mode="wait" initial={false}>
            <motion.p
              key={index}
              initial={{ y: 12, opacity: 0 }}
              animate={{ y: 0, opacity: 1 }}
              exit={{ y: -12, opacity: 0 }}
              transition={{ duration: 0.3 }}
              className={cn("truncate", dark ? "text-navy-300" : "text-ink-muted")}
            >
              <span className={cn("font-medium", dark ? "text-white" : "text-ink")}>{e.source}</span>{" "}
              · {e.text}
            </motion.p>
          </AnimatePresence>
        </div>
      </div>
      <span
        className={cn(
          "shrink-0 rounded-full px-2 py-0.5 text-xs font-medium",
          dark ? "bg-brand-500/20 text-brand-300" : "bg-brand-50 text-brand-700",
        )}
      >
        {e.stage}
      </span>
    </div>
  );
}
