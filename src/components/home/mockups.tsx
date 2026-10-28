import { Bot, CheckCheck } from "lucide-react";

import { cn } from "@/lib/utils";

/*
 * UI vignettes drawn in code. All names and values are placeholders that show how
 * the product behaves; each mockup carries a visible "Example" label.
 */

export function ExampleTag({ tone = "light" }: { tone?: "light" | "dark" }) {
  return (
    <span
      className={cn(
        "rounded-full px-2 py-0.5 text-[0.6875rem] font-medium tracking-wide uppercase",
        tone === "light" ? "bg-paper-2 text-ink-muted" : "bg-navy-800 text-navy-300",
      )}
    >
      Example
    </span>
  );
}

export function ChatMockup() {
  return (
    <div className="flex flex-col gap-2.5 text-[0.8125rem]" aria-hidden="true">
      <div className="max-w-[85%] self-start rounded-md rounded-bl-xs bg-white px-3 py-2 text-ink shadow-xs ring-1 ring-line">
        Hi, do you have availability for a consultation this week?
      </div>
      <div className="flex max-w-[85%] items-end gap-2 self-end">
        <div className="rounded-md rounded-br-xs bg-brand-500 px-3 py-2 text-white">
          Yes, we do. So I can point you to the right person, is this for a new project or an
          existing one?
        </div>
        <span className="grid size-6 shrink-0 place-items-center rounded-full bg-navy-900 text-white">
          <Bot className="size-3.5" />
        </span>
      </div>
      <div className="flex items-center gap-1 self-end pr-8 text-[0.6875rem] text-ink-muted">
        <CheckCheck className="size-3.5 text-brand-500" /> AI agent · replied automatically
      </div>
    </div>
  );
}

const stages = [
  { name: "New", cards: ["Website enquiry", "Lead ad form"] },
  { name: "Qualified", cards: ["WhatsApp enquiry"] },
  { name: "Booked", cards: ["Strategy call"] },
];

export function MiniPipeline() {
  return (
    <div className="grid grid-cols-3 gap-2 text-[0.75rem]" aria-hidden="true">
      {stages.map((s) => (
        <div key={s.name} className="flex flex-col gap-1.5 rounded-sm bg-paper-2 p-2">
          <p className="flex items-center justify-between font-medium text-ink">
            {s.name}
            <span className="text-ink-muted">{s.cards.length}</span>
          </p>
          {s.cards.map((c) => (
            <div key={c} className="rounded-xs bg-white px-2 py-1.5 text-ink shadow-xs ring-1 ring-line">
              {c}
            </div>
          ))}
        </div>
      ))}
    </div>
  );
}

export function WorkflowMockup() {
  const steps = [
    { t: "Trigger", d: "Form submitted" },
    { t: "Wait", d: "1 minute" },
    { t: "Send", d: "SMS + email reply" },
    { t: "If", d: "No response in 1 day" },
    { t: "Send", d: "WhatsApp follow-up" },
  ];
  return (
    <ol className="relative flex flex-col gap-1.5 text-[0.75rem]" aria-hidden="true">
      <span className="absolute top-3 bottom-3 left-[0.6875rem] w-px bg-line-strong" />
      {steps.map((s, i) => (
        <li key={i} className="relative flex items-center gap-2.5">
          <span
            className={cn(
              "z-10 grid size-[1.375rem] place-items-center rounded-full text-[0.625rem] font-semibold",
              i === 0 ? "bg-brand-500 text-white" : "bg-white text-ink-muted ring-1 ring-line-strong",
            )}
          >
            {i + 1}
          </span>
          <span className="flex-1 rounded-xs bg-white px-2 py-1.5 ring-1 ring-line">
            <span className="font-semibold text-ink">{s.t}</span>{" "}
            <span className="text-ink-muted">{s.d}</span>
          </span>
        </li>
      ))}
    </ol>
  );
}

const board = [
  {
    stage: "New lead",
    tone: "bg-navy-300",
    cards: [
      { name: "Lead A", src: "Website form", tag: "Replied" },
      { name: "Lead B", src: "Missed call", tag: "Text-back sent" },
    ],
  },
  {
    stage: "Qualified",
    tone: "bg-brand-400",
    cards: [
      { name: "Lead C", src: "WhatsApp", tag: "Budget confirmed" },
      { name: "Lead D", src: "Lead ad", tag: "Timeline: 30 days" },
    ],
  },
  {
    stage: "Call booked",
    tone: "bg-brand-300",
    cards: [{ name: "Lead E", src: "Website form", tag: "Reminder queued" }],
  },
  {
    stage: "Won",
    tone: "bg-success",
    cards: [{ name: "Lead F", src: "Referral", tag: "Review request scheduled" }],
  },
];

/** Larger dashboard mockup for the dark "pipeline" section. */
export function PipelineBoard() {
  return (
    <div
      className="overflow-hidden rounded-xl bg-navy-800/70 ring-1 ring-navy-700 backdrop-blur"
      aria-label="Example pipeline board with placeholder leads"
      role="img"
    >
      <div className="flex items-center justify-between border-b border-navy-700 px-4 py-3">
        <div className="flex items-center gap-2">
          <span className="size-2.5 rounded-full bg-navy-700" />
          <span className="size-2.5 rounded-full bg-navy-700" />
          <span className="size-2.5 rounded-full bg-navy-700" />
          <span className="ml-3 text-[0.8125rem] font-medium text-white">Sales pipeline</span>
        </div>
        <ExampleTag tone="dark" />
      </div>
      <div className="grid grid-cols-2 gap-3 p-4 md:grid-cols-4">
        {board.map((col) => (
          <div key={col.stage} className="flex flex-col gap-2">
            <p className="flex items-center gap-2 text-[0.75rem] font-medium text-navy-300">
              <span className={cn("size-1.5 rounded-full", col.tone)} />
              {col.stage}
            </p>
            {col.cards.map((c) => (
              <div key={c.name} className="rounded-sm bg-navy-900 p-3 ring-1 ring-navy-700">
                <p className="text-[0.8125rem] font-medium text-white">{c.name}</p>
                <p className="mt-0.5 text-[0.75rem] text-navy-300">{c.src}</p>
                <p className="mt-2.5 inline-flex rounded-full bg-brand-500/15 px-2 py-0.5 text-[0.6875rem] text-brand-300">
                  {c.tag}
                </p>
              </div>
            ))}
          </div>
        ))}
      </div>
    </div>
  );
}
