import type { Metadata } from "next";

import { SiteHeader } from "@/components/site/header";
import { Button, ButtonArrow } from "@/components/ui/button";
import { Field, Input, Select, Textarea } from "@/components/ui/form";
import { Badge, Card, Container, IconTile, LiveDot, SectionHeading } from "@/components/ui/primitives";
import { ServiceIcon } from "@/components/site/service-icon";

export const metadata: Metadata = { title: "Design system" };

const palette = [
  {
    group: "Neutrals",
    swatches: [
      { name: "white", value: "#FFFFFF", cls: "bg-white", note: "Page" },
      { name: "paper", value: "#F5F7FB", cls: "bg-paper", note: "Soft section" },
      { name: "paper-2", value: "#EEF2F8", cls: "bg-paper-2", note: "Inset / input fill" },
      { name: "line", value: "#E3E8F0", cls: "bg-line", note: "Hairline border" },
      { name: "line-strong", value: "#CBD3E1", cls: "bg-line-strong", note: "Input border" },
      { name: "ink-muted", value: "#5B6475", cls: "bg-ink-muted", note: "5.96:1 on white" },
      { name: "ink", value: "#0B1220", cls: "bg-ink", note: "18.7:1 on white" },
    ],
  },
  {
    group: "Navy",
    swatches: [
      { name: "navy-300", value: "#A9B6CF", cls: "bg-navy-300", note: "Muted text on navy, 8.7:1" },
      { name: "navy-700", value: "#1C2F5E", cls: "bg-navy-700", note: "Border on navy" },
      { name: "navy-800", value: "#12224A", cls: "bg-navy-800", note: "Panel on navy" },
      { name: "navy-900", value: "#0A1633", cls: "bg-navy-900", note: "Dark section" },
      { name: "navy-950", value: "#050D24", cls: "bg-navy-950", note: "Footer" },
    ],
  },
  {
    group: "Electric blue",
    swatches: [
      { name: "brand-50", value: "#EEF3FF", cls: "bg-brand-50", note: "Tint" },
      { name: "brand-100", value: "#DDE7FF", cls: "bg-brand-100", note: "Tint border" },
      { name: "brand-300", value: "#8EB4FF", cls: "bg-brand-300", note: "Links on navy, 8.6:1" },
      { name: "brand-400", value: "#4D7BFF", cls: "bg-brand-400", note: "Icons on navy" },
      { name: "brand-500", value: "#1F4FFF", cls: "bg-brand-500", note: "Primary, white text 5.8:1" },
      { name: "brand-600", value: "#1A44E0", cls: "bg-brand-600", note: "Hover, links 7.1:1" },
      { name: "brand-700", value: "#1536B3", cls: "bg-brand-700", note: "Text on tint" },
    ],
  },
];

const typeScale = [
  { token: "text-display", sample: "Every lead answered.", cls: "text-display font-semibold" },
  { token: "text-h1", sample: "A clear plan first.", cls: "text-h1 font-semibold" },
  { token: "text-h2", sample: "One connected system.", cls: "text-h2 font-semibold" },
  { token: "text-h3", sample: "Workflow automation", cls: "text-h3 font-semibold" },
  { token: "text-lead", sample: "We design and build the systems behind your sales.", cls: "text-lead text-ink-muted" },
  { token: "text-base", sample: "Body copy sits at 16px with a 1.5 line height.", cls: "text-base" },
  { token: "text-eyebrow", sample: "Section eyebrow", cls: "text-eyebrow font-semibold uppercase text-brand-600" },
];

function Block({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <section className="border-t border-line py-14">
      <h2 className="mb-8 text-h3 font-semibold text-ink">{title}</h2>
      {children}
    </section>
  );
}

export default function DesignSystemPage() {
  return (
    <>
      <SiteHeader />
      <main id="main">
        <Container className="pt-12 pb-24">
          <SectionHeading
            as="h1"
            eyebrow="Design system · v0.1"
            title="Your Marketing AI tokens and components"
            lead="Every value here lives in src/app/globals.css as a Tailwind v4 theme token. Components only use tokens, never raw hex values."
          />

          <Block title="Colour">
            <div className="grid gap-10">
              {palette.map((p) => (
                <div key={p.group}>
                  <p className="mb-3 text-sm font-medium text-ink-muted">{p.group}</p>
                  <ul className="grid grid-cols-2 gap-3 sm:grid-cols-4 lg:grid-cols-7">
                    {p.swatches.map((s) => (
                      <li key={s.name} className="overflow-hidden rounded-md ring-1 ring-line">
                        <div className={`h-16 ${s.cls}`} />
                        <div className="p-3">
                          <p className="text-sm font-medium text-ink">{s.name}</p>
                          <p className="font-mono text-xs text-ink-muted">{s.value}</p>
                          <p className="mt-1 text-xs text-ink-muted">{s.note}</p>
                        </div>
                      </li>
                    ))}
                  </ul>
                </div>
              ))}
            </div>
          </Block>

          <Block title="Typography">
            <p className="mb-6 text-sm text-ink-muted">
              Geist Sans for everything, tight tracking on headings. Instrument Serif is reserved
              for rare editorial accents (direction B). Headings are fluid with clamp().
            </p>
            <ul className="grid gap-6">
              {typeScale.map((t) => (
                <li key={t.token} className="grid gap-2 md:grid-cols-[10rem_1fr] md:items-baseline">
                  <code className="font-mono text-xs text-ink-muted">{t.token}</code>
                  <p className={t.cls}>{t.sample}</p>
                </li>
              ))}
            </ul>
          </Block>

          <Block title="Radius and shadow">
            <div className="grid grid-cols-2 gap-6 sm:grid-cols-5">
              {[
                ["rounded-xs", "6px · chips"],
                ["rounded-sm", "10px · buttons, inputs"],
                ["rounded-md", "14px · cards"],
                ["rounded-lg", "20px · panels"],
                ["rounded-xl", "28px · hero, CTA"],
              ].map(([cls, label]) => (
                <div key={cls} className="flex flex-col gap-2">
                  <div className={`h-20 bg-brand-50 ring-1 ring-brand-100 ${cls}`} />
                  <code className="font-mono text-xs text-ink">{cls}</code>
                  <span className="text-xs text-ink-muted">{label}</span>
                </div>
              ))}
            </div>
            <div className="mt-10 grid grid-cols-2 gap-6 sm:grid-cols-5">
              {["shadow-xs", "shadow-sm", "shadow-md", "shadow-lg", "shadow-glow"].map((cls) => (
                <div key={cls} className="flex flex-col gap-3">
                  <div className={`h-20 rounded-md bg-white ${cls}`} />
                  <code className="font-mono text-xs text-ink">{cls}</code>
                </div>
              ))}
            </div>
          </Block>

          <Block title="Buttons">
            <div className="flex flex-wrap items-center gap-3">
              <Button>
                Primary <ButtonArrow />
              </Button>
              <Button variant="secondary">Secondary</Button>
              <Button variant="ghost">Ghost</Button>
              <Button variant="link">Text link</Button>
              <Button size="sm">Small</Button>
              <Button size="lg">Large</Button>
              <Button disabled>Disabled</Button>
            </div>
            <div className="on-dark mt-6 flex flex-wrap items-center gap-3 rounded-lg bg-navy-900 p-6">
              <Button variant="primary-dark">
                Primary on navy <ButtonArrow />
              </Button>
              <Button variant="secondary-dark">Secondary on navy</Button>
            </div>
          </Block>

          <Block title="Badges">
            <div className="flex flex-wrap items-center gap-3">
              <Badge>
                <LiveDot /> Brand
              </Badge>
              <Badge variant="neutral">Neutral</Badge>
              <Badge variant="outline">Outline</Badge>
              <Badge variant="success">Success</Badge>
              <span className="rounded-full bg-navy-900 p-2">
                <Badge variant="dark">Dark</Badge>
              </span>
              <Badge size="sm">Small</Badge>
            </div>
          </Block>

          <Block title="Cards">
            <div className="grid gap-4 md:grid-cols-3">
              <Card className="p-6">
                <IconTile>
                  <ServiceIcon name="workflow" />
                </IconTile>
                <p className="mt-5 font-semibold text-ink">Default</p>
                <p className="mt-1 text-sm text-ink-muted">Hairline ring, extra-small shadow.</p>
              </Card>
              <Card interactive className="p-6">
                <IconTile>
                  <ServiceIcon name="bot" />
                </IconTile>
                <p className="mt-5 font-semibold text-ink">Interactive</p>
                <p className="mt-1 text-sm text-ink-muted">Lifts 2px and tints its border on hover.</p>
              </Card>
              <Card variant="muted" className="p-6">
                <IconTile>
                  <ServiceIcon name="kanban" />
                </IconTile>
                <p className="mt-5 font-semibold text-ink">Muted</p>
                <p className="mt-1 text-sm text-ink-muted">For use on white sections.</p>
              </Card>
            </div>
          </Block>

          <Block title="Form controls">
            <div className="grid max-w-2xl gap-5 sm:grid-cols-2">
              <Field id="ds-name" label="Name" hint="Hint text sits below the field.">
                <Input placeholder="Placeholder" />
              </Field>
              <Field id="ds-email" label="Email" error="Please enter a valid email address.">
                <Input defaultValue="not-an-email" />
              </Field>
              <Field id="ds-select" label="Select">
                <Select defaultValue="b">
                  <option value="a">Option A</option>
                  <option value="b">Option B</option>
                </Select>
              </Field>
              <Field id="ds-disabled" label="Disabled" optional>
                <Input disabled placeholder="Disabled" />
              </Field>
              <div className="sm:col-span-2">
                <Field id="ds-message" label="Message">
                  <Textarea />
                </Field>
              </div>
            </div>
          </Block>

          <Block title="Section heading">
            <div className="grid gap-12">
              <SectionHeading
                eyebrow="Eyebrow"
                title="Left-aligned section heading"
                lead="Lead paragraph, max 42rem wide, muted colour."
              />
              <div className="on-dark rounded-lg bg-navy-900 p-10">
                <SectionHeading
                  tone="dark"
                  align="center"
                  eyebrow="Eyebrow"
                  title="Centred heading on navy"
                  lead="Same component, dark tone."
                />
              </div>
            </div>
          </Block>
        </Container>
      </main>
    </>
  );
}
