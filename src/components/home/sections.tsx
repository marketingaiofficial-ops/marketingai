import Link from "next/link";
import { ArrowUpRight } from "lucide-react";

import { ContactForm } from "@/components/home/contact-form";
import { FaqList } from "@/components/home/faq";
import { LeadFlow } from "@/components/home/lead-flow";
import { ChatMockup, ExampleTag, MiniPipeline, PipelineBoard, WorkflowMockup } from "@/components/home/mockups";
import { ServiceIcon } from "@/components/site/service-icon";
import { Button, ButtonArrow } from "@/components/ui/button";
import { Reveal, Spotlight } from "@/components/ui/motion";
import { Badge, Card, Container, IconTile, LiveDot, SectionHeading } from "@/components/ui/primitives";
import { integrations, leaks, process, services, site } from "@/lib/content";
import { cn } from "@/lib/utils";

/* ---------------- Hero ---------------- */

export function Hero() {
  return (
    <section className="relative isolate overflow-hidden">
      <div aria-hidden="true" className="absolute inset-0 -z-10 bg-gradient-to-b from-brand-50/70 via-white to-white" />
      <div
        aria-hidden="true"
        className="bg-grid absolute inset-0 -z-10 [mask-image:radial-gradient(ellipse_at_70%_20%,black_20%,transparent_70%)]"
      />
      <Spotlight className="-z-10" />

      <Container className="grid items-center gap-14 [&>*]:min-w-0 pt-12 pb-20 md:pt-20 lg:grid-cols-[1.05fr_1fr] lg:gap-16 lg:pt-24 lg:pb-28">
        <div className="flex flex-col items-start">
          <Badge>
            <LiveDot /> GoHighLevel · CRM · AI agents
          </Badge>
          <h1 className="mt-6 text-display font-semibold text-ink">
            Every lead answered.
            <br />
            <span className="text-brand-500">Every follow-up sent.</span>
          </h1>
          <p className="mt-6 max-w-xl text-lead text-ink-muted">
            We design and build the systems behind your sales: GoHighLevel CRM, pipelines,
            workflow automation and AI agents that reply, qualify and book while your team gets on
            with the work.
          </p>
          <div className="mt-9 flex w-full flex-col gap-3 sm:w-auto sm:flex-row">
            <Button asChild size="lg">
              <Link href={site.bookingHref}>
                Book a strategy call
                <ButtonArrow />
              </Link>
            </Button>
            <Button asChild size="lg" variant="secondary">
              <Link href={site.diagnosticHref}>Find my lead leaks</Link>
            </Button>
          </div>
          <p className="mt-5 text-[0.8125rem] text-ink-muted">
            Built inside your own GoHighLevel account. You keep the system and the data.
          </p>
        </div>

        <Reveal delay={0.1}>
          <div className="relative rounded-xl bg-white/80 p-4 shadow-lg ring-1 ring-line backdrop-blur sm:p-6">
            <div className="mb-5 flex items-center justify-between">
              <p className="text-sm font-semibold text-ink">How a lead moves through your system</p>
              <ExampleTag />
            </div>
            <LeadFlow />
          </div>
        </Reveal>
      </Container>
    </section>
  );
}

/* ---------------- Where leads leak ---------------- */

export function Leaks() {
  return (
    <section id="diagnostic" className="section-y bg-paper">
      <Container>
        <div className="flex flex-col justify-between gap-8 md:flex-row md:items-end">
          <SectionHeading
            eyebrow="Where revenue leaks"
            title="Most lost deals were never really lost. They were left waiting."
          />
          <Button asChild variant="secondary" className="self-start md:self-auto">
            <Link href={site.diagnosticHref}>
              Run the 3-minute diagnostic
              <ButtonArrow />
            </Link>
          </Button>
        </div>
        <div className="mt-12 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          {leaks.map((l, i) => (
            <Reveal key={l.title} delay={i * 0.05}>
              <Card interactive className="flex h-full flex-col p-6">
                <span className="font-mono text-[0.8125rem] text-brand-600">0{i + 1}</span>
                <h3 className="mt-6 text-h3 font-semibold text-ink">{l.title}</h3>
                <p className="mt-2 text-[0.9375rem] text-ink-muted">{l.body}</p>
              </Card>
            </Reveal>
          ))}
        </div>
      </Container>
    </section>
  );
}

/* ---------------- Services bento ---------------- */

export function ServicesBento() {
  const [setup, crm, workflow, agents, leadgen, web] = services;
  return (
    <section id="services" className="section-y">
      <Container>
        <SectionHeading
          eyebrow="What we build"
          title="One connected system, from first click to closed deal."
          lead="Six services that work on their own or together. Pick one problem to start with; we design so the rest can slot in later."
        />
        <div className="mt-14 grid gap-4 md:grid-cols-6">
          <BentoTile service={agents} className="md:col-span-3 md:row-span-2" visual={<ChatMockup />} />
          <BentoTile service={crm} className="md:col-span-3" visual={<MiniPipeline />} />
          <BentoTile service={workflow} className="md:col-span-3" visual={<WorkflowMockup />} />
          <BentoTile service={setup} className="md:col-span-2" />
          <BentoTile service={leadgen} className="md:col-span-2" />
          <BentoTile service={web} className="md:col-span-2" />
        </div>
      </Container>
    </section>
  );
}

function BentoTile({
  service,
  visual,
  className,
}: {
  service: (typeof services)[number];
  visual?: React.ReactNode;
  className?: string;
}) {
  return (
    <Card interactive className={cn("group flex flex-col overflow-hidden", className)}>
      <div className="flex flex-col p-6 sm:p-7">
        <div className="flex items-start justify-between">
          <IconTile>
            <ServiceIcon name={service.icon} />
          </IconTile>
          <Badge variant="neutral" size="sm">
            {service.group}
          </Badge>
        </div>
        <h3 className="mt-6 text-h3 font-semibold text-ink">{service.title}</h3>
        <p className="mt-2 text-[0.9375rem] text-ink-muted">{service.description}</p>
        <Link
          href="#contact"
          className="mt-5 inline-flex items-center gap-1 self-start text-sm font-medium text-brand-600 after:absolute after:inset-0 hover:underline"
          aria-label={`Talk to us about ${service.title}`}
        >
          Talk to us about this
          <ArrowUpRight className="size-4 transition-transform group-hover:translate-x-0.5 group-hover:-translate-y-0.5" />
        </Link>
      </div>
      {visual ? (
        <div className="mt-auto flex flex-1 flex-col justify-center border-t border-line bg-paper/70 p-5 sm:p-6">{visual}</div>
      ) : null}
    </Card>
  );
}

/* ---------------- Pipeline (dark) ---------------- */

export function PipelineSection() {
  return (
    <section className="on-dark relative isolate overflow-hidden bg-navy-900 section-y">
      <div aria-hidden="true" className="bg-grid-dark absolute inset-0 -z-10 [mask-image:linear-gradient(to_bottom,black,transparent)]" />
      <div
        aria-hidden="true"
        className="absolute top-0 left-1/2 -z-10 h-96 w-[60rem] -translate-x-1/2 rounded-full bg-brand-500/25 blur-[120px]"
      />
      <Container>
        <SectionHeading
          tone="dark"
          align="center"
          eyebrow="Visibility"
          title="See every lead, every stage, in one place."
          lead="Your pipeline shows who came in, what the system already did, and who needs a person next. No more digging through inboxes."
        />
        <Reveal className="mt-14">
          <PipelineBoard />
        </Reveal>
      </Container>
    </section>
  );
}

/* ---------------- Process ---------------- */

export function Process() {
  return (
    <section id="process" className="section-y">
      <Container className="grid gap-14 lg:grid-cols-[0.8fr_1.2fr]">
        <div className="lg:sticky lg:top-28 lg:self-start">
          <SectionHeading
            eyebrow="How we work"
            title="A clear plan before anything gets built."
            lead="Every engagement follows the same five steps, and each one ends with something you can keep."
          />
        </div>
        <ol className="relative flex flex-col">
          <span aria-hidden="true" className="absolute top-2 bottom-2 left-[1.1875rem] w-px bg-gradient-to-b from-brand-500 via-line-strong to-line" />
          {process.map((p, i) => (
            <li key={p.step} className="relative pb-10 last:pb-0">
              <Reveal delay={i * 0.04} className="grid grid-cols-[2.5rem_1fr] gap-5">
                <span className="z-10 grid size-10 place-items-center rounded-full bg-white font-mono text-[0.8125rem] font-medium text-brand-600 ring-1 ring-line-strong">
                  {p.step}
                </span>
                <div className="pt-1.5">
                  <h3 className="text-h3 font-semibold text-ink">{p.title}</h3>
                  <p className="mt-2 text-ink-muted">{p.body}</p>
                  <p className="mt-3 inline-flex items-center gap-2 text-[0.8125rem] font-medium text-ink">
                    <span className="size-1.5 rounded-full bg-brand-500" />
                    You get: {p.output}
                  </p>
                </div>
              </Reveal>
            </li>
          ))}
        </ol>
      </Container>
    </section>
  );
}

/* ---------------- Integrations ---------------- */

export function Integrations() {
  const row = [...integrations, ...integrations];
  return (
    <section aria-labelledby="works-with" className="border-y border-line bg-paper py-10">
      <Container className="flex flex-col items-center gap-6 md:flex-row md:gap-10">
        <p id="works-with" className="shrink-0 text-sm font-medium text-ink-muted">
          Works with the tools you already use
        </p>
        <div className="relative w-full overflow-hidden [mask-image:linear-gradient(to_right,transparent,black_10%,black_90%,transparent)]">
          <ul className="flex w-max animate-marquee gap-3 hover:[animation-play-state:paused] motion-reduce:w-full motion-reduce:flex-wrap motion-reduce:animate-none">
            {row.map((name, i) => (
              <li
                key={i}
                aria-hidden={i >= integrations.length ? true : undefined}
                className="rounded-full bg-white px-4 py-2 text-sm font-medium whitespace-nowrap text-ink ring-1 ring-line"
              >
                {name}
              </li>
            ))}
          </ul>
        </div>
      </Container>
    </section>
  );
}

/* ---------------- FAQ ---------------- */

export function Faq() {
  return (
    <section id="faq" className="section-y">
      <Container size="content" className="grid gap-12 lg:grid-cols-[0.8fr_1.2fr]">
        <SectionHeading eyebrow="FAQ" title="Questions we hear before every project." />
        <FaqList />
      </Container>
    </section>
  );
}

/* ---------------- Contact / CTA ---------------- */

export function ContactCta() {
  return (
    <section id="contact" className="pb-(--section-y)">
      <Container>
        <div className="grid overflow-hidden rounded-xl bg-white shadow-lg ring-1 ring-line lg:grid-cols-[0.9fr_1.1fr]">
          <div className="on-dark relative isolate flex flex-col justify-between gap-10 bg-navy-900 p-8 sm:p-12">
            <div aria-hidden="true" className="absolute -bottom-24 -left-24 -z-10 size-80 rounded-full bg-brand-500/30 blur-3xl" />
            <div>
              <p className="text-eyebrow font-semibold text-brand-300 uppercase">Strategy call</p>
              <h2 className="mt-4 text-h2 font-semibold text-white">
                Tell us where leads get stuck. We&apos;ll map the fix.
              </h2>
              <p className="mt-4 text-navy-300">
                A focused call to walk through your current lead flow and what a connected system
                would look like for your business.
              </p>
            </div>
            <ul className="grid gap-3 text-sm text-navy-300">
              {["Your lead flow mapped on the call", "Clear next steps, whether or not you hire us", "No obligation"].map((t) => (
                <li key={t} className="flex items-center gap-3">
                  <span className="grid size-5 place-items-center rounded-full bg-brand-500/20 text-brand-300">
                    <svg viewBox="0 0 12 12" className="size-3" aria-hidden="true">
                      <path d="M2.5 6.5l2 2 5-5" fill="none" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round" />
                    </svg>
                  </span>
                  {t}
                </li>
              ))}
            </ul>
          </div>
          <div className="p-8 sm:p-12">
            <ContactForm />
          </div>
        </div>
      </Container>
    </section>
  );
}
