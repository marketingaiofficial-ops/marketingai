# Design Direction: Your Marketing AI

## 1. Positioning (draft for your approval)

**Who it's for:** service businesses and agencies that lose revenue to slow replies, scattered tools and manual follow-up, plus businesses that already use GoHighLevel but haven't built it out properly.

**What you are:** an implementation partner that designs, builds and runs revenue systems on GoHighLevel. That covers CRM, pipelines, funnels and websites, workflow automation, and AI agents for chat and voice.

**Draft one-liner:** _"We build the systems that capture, qualify and follow up with every lead, on GoHighLevel, with AI agents doing the repetitive work."_

**Tone:** calm, precise and operator-grade. Show the system working instead of using hype words ("revolutionary", "10x", "autopilot"). Make capability claims, never outcome guarantees.

## 2. Creative principles

1. **Show the machine.** The signature visual is a live, animated **lead-flow diagram**: a lead enters, an AI agent replies, the lead is qualified, a pipeline stage moves, and a follow-up fires. It is drawn from your real service stack, not from stock "AI brain" imagery.
2. **Restraint over decoration.** One accent color, generous whitespace, and motion only where it explains something.
3. **Discovery by problem, not by product.** Visitors pick their pain ("leads go cold", "my team lives in spreadsheets", "GHL is half set up"), and the site routes them to the right service.
4. **Proof slots, honestly empty.** Layouts reserve space for case studies and testimonials, but they ship with process and deliverable detail instead of invented proof until you supply real material.
5. **International by default.** Plain English, no region-specific idioms, currency-neutral pricing language, and time-zone-aware booking.

## 3. Visual system

| Token | Direction |
|---|---|
| Base | Near-black ink (`#0B0D12`-ish) for dark sections, off-white paper (`#F7F7F5`-ish) for light sections. Alternating dark and light bands give the page rhythm. |
| Accent | **One** signature accent: an electric blue-violet, chosen to stay continuous with your existing blue/violet assets. Plus one functional "success" green used only in flow diagrams (lead won, step done). Drop the multi-color gradient wordmark. |
| Type | A characterful grotesk for display (e.g. Geist, Inter Display or General Sans) and the same family for body text. Use tabular numerals in diagrams. Headlines are tight, and sentence case throughout. |
| Shape | 12–16px radii, hairline 1px borders, low shadows. Cards read as "system panels". |
| Iconography | Single-weight line icons (Lucide, already standard in shadcn). Real tool logos (GoHighLevel, WhatsApp, Stripe, Google Calendar and so on) appear only in "integrates with" contexts, follow each brand's usage guidelines, and never imply partnership. |
| Imagery | UI-style illustrations of pipelines, inboxes, calendars and call transcripts built in code. No stock photos of handshakes or robots. Real team photos later, if you want them. |
| Motion | Framer Motion / Motion. Entrance animations under 400ms, flow beams that loop slowly, and everything respects `prefers-reduced-motion`. |
| Theme | Light first with dark hero and footer bands. A full dark mode toggle is optional (phase 4). |

## 4. Information architecture

```
/                       Home
/services               Overview (problem-led selector)
  /services/gohighlevel-setup        GHL implementation & migration
  /services/crm-pipelines            CRM, pipelines & sales process
  /services/workflow-automation      Workflow & business process automation
  /services/ai-agents                AI chat & voice agents
  /services/lead-generation          Lead gen systems, funnels & ads landing pages
  /services/websites-funnels         Websites & funnels on GHL
/solutions/[industry]   Only for industries you actually serve (to be confirmed)
/how-we-work            Process: discovery → blueprint → build → launch → optimise
/pricing                Packages or "from" ranges, only if you want them public
/diagnostic             Lead-leak diagnostic (the Marketing AI Flow, rebuilt or embedded)
/about                  Who you are, how you work, where you operate
/contact                Book a call + form + WhatsApp
/blog                   Optional in phase 4, for SEO
/privacy, /terms
```

**Navigation:** logo, then Services (mega menu grouped as "Capture", "Convert" and "Automate", each item with an icon and one-line description), How we work, Pricing, About, then a primary button **"Book a strategy call"** and a secondary link **"Find my lead leaks"**. On mobile this becomes a full-screen sheet with accordion groups and a sticky bottom CTA.

## 5. Homepage storyline

1. **Hero:** problem-led headline, for example _"Every lead answered. Every follow-up sent. Built on GoHighLevel."_ Subcopy names the services. Primary CTA "Book a strategy call", secondary "Find my lead leaks (3 min)". The animated lead-flow diagram sits on the right on desktop, below the copy on mobile.
2. **Where leads leak:** three or four pain cards (slow first reply, no pipeline visibility, manual follow-up, disconnected tools), each linking to the relevant service.
3. **What we build:** a services bento of six tiles mapping to the six service pages, with a small live UI vignette in each tile.
4. **How a lead moves through your system:** a scroll-driven walkthrough of a single lead from source to AI reply, qualification, booking, pipeline, follow-up and review request. This is the signature section.
5. **How we work:** a five-step process timeline with deliverables at each step (blueprint document, build, QA, handover, optimisation).
6. **Integrations:** a logo grid of tools you actually connect, labelled "Works with" and never "Partners".
7. **Proof:** reserved for real case studies or testimonials. Until those exist, use a "What you get" deliverables checklist and a short founder note.
8. **Pricing teaser or engagement models:** setup project, monthly optimisation, AI agent add-on. This section needs your input.
9. **FAQ:** GHL licensing, data ownership, timelines, WhatsApp API, what happens after launch.
10. **Final CTA band:** booking plus the diagnostic.
11. **Footer:** services, company, legal, contact, region or time zone.

## 6. 21st.dev component shortlist (research only, nothing installed)

These are candidates to adapt, not to drop in unchanged. Each will be restyled to the tokens above. The free tier allows 2 installs per day, so the plan sequences them.

| Need | Candidate(s) | Why |
|---|---|---|
| Navigation and mega menu | [Navigation Menu – wensity](https://21st.dev/@wensity/components/navigation-menu), [Rich Navigation Menu – shadcnui-blocks](https://21st.dev/@shadcnui-blocks/components/navigation-menu-06), [Directional Menu – hyperiux](https://21st.dev/@hyperiux/components/directional-menu) | Keyboard accessible, multi-column panels with icons and descriptions. Directional Menu is the premium option but adds GSAP. |
| Hero | [SaaS Hero with live workflow demo – kedhareswer](https://21st.dev/@kedhareswer/components/ink-orbit-hero), [Modern Hero (mouse-follow grid) – uniquesonu](https://21st.dev/@uniquesonu/components/modern-hero-section-1) | Use as structure only. The visual will be our own lead-flow diagram. Remove fake proof rows and invented stats. |
| Animated background | [Aurora Flow – ruixen.ui](https://21st.dev/@ruixen.ui/components/aurora-flow), [Aurora Background – pulkitxm](https://21st.dev/@pulkitxm/components/aurora-background) | Use very subtly, in the hero band only. Must pause offscreen and respect reduced motion. |
| Workflow visualization | [AI Agent Pipeline – monolythdev](https://21st.dev/@monolythdev/components/ai-agent-pipeline), [Animated Beam – Magic UI](https://21st.dev/@dillionverma/components/animated-beam), [Animated Beam Integration](https://21st.dev/@abushaidislam7/components/animated-beam-integration) | The core of the signature section. Animated Beam is the lightweight base, and AI Agent Pipeline is the closest narrative match. |
| Service showcase | [Animated Features Bento with Live Diagrams](https://21st.dev/@kedhareswer/components/ink-orbit-features), [Bento Grid – kokonutd](https://21st.dev/@kokonutd/components/bento-grid) | Six-tile services bento with live vignettes. |
| Process | [Scroll animated timeline – ibrandify](https://21st.dev/@ibrandify/components/scroll-timeline), [Timeline – Aceternity](https://21st.dev/@manuarora700/components/timeline) | "How we work" section. |
| Testimonials (later) | [Testimonials Marquee – shadcnspace](https://21st.dev/@shadcnspace/components/marquee-01), [Marquee – diceui](https://21st.dev/@diceui/components/marquee) | diceui is accessible (pause on hover, reduced motion). Only used once real testimonials exist. |
| Pricing | [Pricing Section 1 – shadcnstore](https://21st.dev/@shadcnstore/components/pricing-section-1) | Clean tiers. Engagement-model framing rather than SaaS seats. |
| CTA | [CTA Section – shadcnstore](https://21st.dev/@shadcnstore/components/cta-section-3) | Simple. We'll pair it with an embedded GHL calendar. |
| FAQ | [Accordion – wensity](https://21st.dev/@wensity/components/accordion) | Accessible and easy to restyle. |

**Avoid:** heavy WebGL or 3D (Aurora Ribbons, 3D sculptures) above the fold. They hurt mobile performance and read as "AI template".

## 7. How we avoid the "AI template" look

- No purple-to-pink gradient blobs everywhere, no glassmorphism stacks, no sparkle icons on every heading.
- Real, specific nouns: "WhatsApp reply", "Pipeline: Qualified → Booked", "Missed-call text-back".
- Asymmetric layouts in key sections (the walkthrough and the bento), not a centered stack of cards.
- Copywriting that names trade-offs and process instead of superlatives.

## 8. Decisions I need from you

1. The public brand name: "Your Marketing AI" or "Marketing AI". How should "The Visionary Web" relate to it?
2. Target regions and industries (this drives the `/solutions` pages and pricing language).
3. Whether pricing is public, and in which currency.
4. Real proof you can share: case studies, testimonials with permission, certifications.
5. Booking tool: a GHL calendar (recommended) or something else.
