import Link from "next/link";
import { ArrowRight } from "lucide-react";

import { LeadFlow } from "@/components/home/lead-flow";
import { PipelineBoard, WorkflowMockup } from "@/components/home/mockups";
import { ServiceIcon } from "@/components/site/service-icon";
import { Button, ButtonArrow } from "@/components/ui/button";
import { Spotlight } from "@/components/ui/motion";
import { Badge, Card, Container, IconTile, LiveDot } from "@/components/ui/primitives";
import { leaks, services, site } from "@/lib/content";

/* Three homepage directions explored for review. All share the same tokens and content. */

/* ---------- A. Premium white-and-blue SaaS ---------- */

export function DirectionSaas() {
  return (
    <div className="relative isolate overflow-hidden bg-white">
      <div aria-hidden="true" className="absolute inset-x-0 top-0 -z-10 h-[36rem] bg-gradient-to-b from-brand-50 to-white" />
      <div
        aria-hidden="true"
        className="absolute top-[-12rem] left-1/2 -z-10 h-[28rem] w-[56rem] -translate-x-1/2 rounded-full bg-brand-500/15 blur-[100px]"
      />
      <Spotlight className="-z-10" />
      <Container className="flex flex-col items-center pt-20 pb-16 text-center md:pt-28">
        <Badge>
          <LiveDot /> For teams running on GoHighLevel
        </Badge>
        <h2 className="mt-6 max-w-4xl text-display font-semibold text-ink">
          The revenue system your sales team <span className="text-brand-500">wishes it had.</span>
        </h2>
        <p className="mt-6 max-w-2xl text-lead text-ink-muted">
          CRM pipelines, automated follow-up and AI agents, designed and built inside your own
          GoHighLevel account.
        </p>
        <div className="mt-9 flex flex-col gap-3 sm:flex-row">
          <Button size="lg" asChild>
            <Link href={site.bookingHref}>
              Book a strategy call <ButtonArrow />
            </Link>
          </Button>
          <Button size="lg" variant="secondary" asChild>
            <Link href={site.diagnosticHref}>Find my lead leaks</Link>
          </Button>
        </div>
        <div className="mt-16 w-full max-w-5xl rounded-xl bg-navy-900 p-2 shadow-lg ring-1 ring-navy-700 sm:p-3">
          <PipelineBoard />
        </div>
      </Container>
      <Container className="grid gap-4 pb-20 sm:grid-cols-2 lg:grid-cols-4">
        {leaks.map((l) => (
          <Card key={l.title} className="p-5 text-left">
            <h3 className="font-semibold text-ink">{l.title}</h3>
            <p className="mt-1.5 text-sm text-ink-muted">{l.body}</p>
          </Card>
        ))}
      </Container>
    </div>
  );
}

/* ---------- B. Editorial technology agency ---------- */

export function DirectionEditorial() {
  return (
    <div className="bg-[#fbfbf9]">
      <Container className="pt-20 pb-10 md:pt-28">
        <div className="flex items-center justify-between border-b border-ink/15 pb-4 text-[0.8125rem] text-ink-muted">
          <span>Automation studio</span>
          <span className="hidden sm:inline">GoHighLevel · CRM · AI agents</span>
          <span>Design · Build · Optimise</span>
        </div>
        <h2 className="mt-12 max-w-5xl text-display font-semibold text-ink">
          We build the{" "}
          <em className="font-serif font-normal tracking-normal text-brand-600 italic">quiet machinery</em>{" "}
          behind every closed deal.
        </h2>
        <div className="mt-12 grid gap-10 md:grid-cols-[1fr_1.4fr]">
          <div className="flex flex-col items-start gap-6">
            <p className="text-lead text-ink-muted">
              Pipelines, follow-up and AI agents, set up so leads are answered, qualified and
              booked without anyone chasing them.
            </p>
            <Button size="lg" asChild>
              <Link href={site.bookingHref}>
                Start a conversation <ButtonArrow />
              </Link>
            </Button>
          </div>
          <ol className="border-t border-ink/15">
            {services.map((s, i) => (
              <li key={s.slug}>
                <Link
                  href="/#services"
                  className="group grid grid-cols-[3rem_1fr_auto] items-baseline gap-4 border-b border-ink/15 py-5 transition-colors hover:bg-white"
                >
                  <span className="font-mono text-[0.8125rem] text-ink-muted">0{i + 1}</span>
                  <span>
                    <span className="block text-h3 font-semibold text-ink group-hover:text-brand-600">
                      {s.title}
                    </span>
                    <span className="mt-1 block text-[0.9375rem] text-ink-muted">{s.short}</span>
                  </span>
                  <ArrowRight
                    aria-hidden="true"
                    className="size-5 -translate-x-2 text-brand-600 opacity-0 transition-all group-hover:translate-x-0 group-hover:opacity-100"
                  />
                </Link>
              </li>
            ))}
          </ol>
        </div>
      </Container>
      <Container className="pb-20">
        <blockquote className="mt-10 max-w-3xl border-l-2 border-brand-500 pl-6 font-serif text-[clamp(1.5rem,1.2rem+1.2vw,2.25rem)] leading-snug text-ink">
          “Most lost deals were never really lost. They were left waiting.”
        </blockquote>
      </Container>
    </div>
  );
}

/* ---------- C. Interactive automation platform ---------- */

export function DirectionPlatform() {
  return (
    <div className="on-dark relative isolate overflow-hidden bg-navy-950">
      <div aria-hidden="true" className="bg-grid-dark absolute inset-0 -z-10" />
      <div
        aria-hidden="true"
        className="absolute top-1/3 left-1/2 -z-10 h-[30rem] w-[50rem] -translate-x-1/2 rounded-full bg-brand-500/25 blur-[120px]"
      />
      <Spotlight className="-z-10" color="rgb(77 123 255 / 0.18)" />
      <Container className="flex flex-col items-center pt-20 pb-20 text-center md:pt-28">
        <Badge variant="dark">
          <LiveDot /> Lead flow, live
        </Badge>
        <h2 className="mt-6 max-w-4xl text-display font-semibold text-white">
          Watch a lead go from <span className="text-brand-300">hello</span> to{" "}
          <span className="text-brand-300">booked.</span>
        </h2>
        <p className="mt-6 max-w-2xl text-lead text-navy-300">
          Every channel feeds one CRM. AI replies and qualifies, workflows follow up, your team
          steps in when it counts.
        </p>
        <div className="mt-9 flex flex-col gap-3 sm:flex-row">
          <Button size="lg" variant="primary-dark" asChild>
            <Link href={site.bookingHref}>
              Book a strategy call <ButtonArrow />
            </Link>
          </Button>
          <Button size="lg" variant="secondary-dark" asChild>
            <Link href={site.diagnosticHref}>Find my lead leaks</Link>
          </Button>
        </div>
        <div className="mt-16 grid w-full max-w-5xl gap-4 text-left lg:grid-cols-[1.5fr_1fr]">
          <Card variant="dark" className="rounded-xl p-5 sm:p-7">
            <LeadFlow tone="dark" />
          </Card>
          <Card variant="dark" className="rounded-xl p-5 sm:p-7">
            <div className="mb-4 flex items-center gap-3">
              <IconTile tone="dark">
                <ServiceIcon name="workflow" />
              </IconTile>
              <p className="text-sm font-semibold">Speed-to-lead workflow</p>
            </div>
            <div className="rounded-md bg-paper p-3">
              <WorkflowMockup />
            </div>
          </Card>
        </div>
      </Container>
    </div>
  );
}
