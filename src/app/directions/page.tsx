import type { Metadata } from "next";
import Link from "next/link";

import { DirectionEditorial, DirectionPlatform, DirectionSaas } from "@/components/directions/directions";
import { Logo } from "@/components/site/logo";
import { Badge, Container } from "@/components/ui/primitives";

export const metadata: Metadata = { title: "Visual directions" };

const directions = [
  {
    id: "a",
    name: "A. Premium white-and-blue SaaS",
    summary:
      "Centred hero, soft blue glow, product mockup as the hero image. Familiar and trustworthy, but closest to every other SaaS site.",
    Component: DirectionSaas,
  },
  {
    id: "b",
    name: "B. Editorial technology agency",
    summary:
      "Big mixed serif/sans headline, numbered service index, hairline rules. Feels like a studio with a point of view; least 'tech demo'.",
    Component: DirectionEditorial,
  },
  {
    id: "c",
    name: "C. Interactive automation platform",
    summary:
      "Dark navy stage with the live lead-flow diagram front and centre. Most memorable and most 'show the machine', heaviest on motion.",
    Component: DirectionPlatform,
  },
];

export default function DirectionsPage() {
  return (
    <main id="main" className="bg-paper pb-24">
      <Container className="flex items-center justify-between py-6">
        <Logo />
        <Link href="/" className="text-sm font-medium text-brand-600 hover:underline">
          View recommended homepage →
        </Link>
      </Container>
      <Container size="content" className="py-10">
        <Badge variant="neutral">Phase 2 · design review</Badge>
        <h1 className="mt-4 text-h1 font-semibold text-ink">Three homepage directions</h1>
        <p className="mt-4 max-w-2xl text-lead text-ink-muted">
          Same tokens, same content, three different personalities. The recommended homepage
          combines A&apos;s white-and-blue clarity with C&apos;s interactive lead-flow diagram, and
          borrows B&apos;s numbered rhythm for lists.
        </p>
        <nav aria-label="Directions" className="mt-6 flex flex-wrap gap-2">
          {directions.map((d) => (
            <a key={d.id} href={`#${d.id}`} className="rounded-full bg-white px-3.5 py-1.5 text-sm font-medium text-ink ring-1 ring-line hover:ring-brand-300">
              {d.name}
            </a>
          ))}
        </nav>
      </Container>

      <div className="flex flex-col gap-16">
        {directions.map(({ id, name, summary, Component }) => (
          <section key={id} id={id} aria-labelledby={`${id}-title`}>
            <Container className="mb-4 flex flex-col gap-1 md:flex-row md:items-baseline md:justify-between md:gap-8">
              <h2 id={`${id}-title`} className="text-h3 font-semibold text-ink">
                {name}
              </h2>
              <p className="max-w-xl text-sm text-ink-muted">{summary}</p>
            </Container>
            <Container>
              <div className="overflow-hidden rounded-xl shadow-md ring-1 ring-line">
                <Component />
              </div>
            </Container>
          </section>
        ))}
      </div>
    </main>
  );
}
