# Design System and Visual Direction (Phase 2)

_Status: prototype for review. Pages: `/` (recommended homepage), `/directions` (three explored directions), `/design-system` (live token and component reference)._

## Assumptions made (please confirm or correct)

- **Public name:** "Your Marketing AI".
- **Logo:** I couldn't find an official logo file in GitHub, Lovable, or on the live site, whose share image is empty. `src/components/site/logo.tsx` is a **placeholder** text wordmark with an "M." mark. Swap in the official SVG there, and every page picks it up.
- **Booking and diagnostic links** point at on-page anchors until the GHL calendar link and the diagnostic URL are provided (`site.bookingHref` and `site.diagnosticHref` in `src/lib/content.ts`).
- **The contact form isn't connected.** It validates and shows a success state only. Connecting it to GHL is Phase 3.
- **No proof content.** There are no clients, testimonials, statistics, awards, certifications or guarantees anywhere. Mockups show placeholder leads ("Lead A") and carry a visible **Example** tag.

## Visual directions explored

All three use the same tokens and copy, so the comparison is about personality, not content. You can see them side by side at `/directions`.

| | A. Premium white-and-blue SaaS | B. Editorial technology agency | C. Interactive automation platform |
|---|---|---|---|
| Hero | Centred headline, soft blue glow, product mockup below | Large left-aligned headline with a serif italic accent, numbered service index | Full navy stage with the live lead-flow diagram and a workflow panel |
| Feels like | A trustworthy SaaS product | A studio with a point of view | A control room for your pipeline |
| Strength | Familiar, clean, fits the requested palette exactly | Distinctive, least "template" | Most memorable, shows the service working |
| Risk | Closest to every other SaaS site | Less obviously "automation", relies on strong copy | Heavier motion, dark-first is less in line with the white palette brief |

### Recommendation: A + C hybrid (implemented at `/`)

- The **white-and-blue foundation from A**: white and soft neutral sections, electric blue for actions, navy for selected dark bands.
- The **interactive lead-flow diagram from C** as the signature hero visual, which makes "we build systems" concrete.
- **B's numbered rhythm** for lists ("01, 02...") and the process timeline. The serif accent is held back for occasional editorial moments, not used site-wide.

## Tokens

Defined once in `src/app/globals.css` (Tailwind v4 `@theme`), so they work as utilities (`bg-navy-900`, `text-h2`, `rounded-md`, `shadow-md`).

### Colour (contrast checked for WCAG AA)

| Role | Token | Hex | Use / contrast |
|---|---|---|---|
| Page | `white` | #FFFFFF | Default background |
| Soft section | `paper` | #F5F7FB | Alternating sections |
| Inset | `paper-2` | #EEF2F8 | Inset panels, hover fills |
| Border | `line` / `line-strong` | #E3E8F0 / #CBD3E1 | Hairlines / input borders |
| Text | `ink` | #0B1220 | 18.7:1 on white |
| Muted text | `ink-muted` | #5B6475 | 5.96:1 on white, 5.56:1 on paper |
| Dark section | `navy-900` / `navy-950` | #0A1633 / #050D24 | Dark bands, footer |
| Panel on navy | `navy-800` / `navy-700` | #12224A / #1C2F5E | Raised panels / borders |
| Muted on navy | `navy-300` | #A9B6CF | 8.7:1 on navy-900 |
| Primary | `brand-500` | #1F4FFF | Buttons; white text 5.8:1 |
| Primary hover / links | `brand-600` | #1A44E0 | 7.1:1 on white |
| Links on navy | `brand-300` | #8EB4FF | 8.6:1 on navy-900 |
| Tints | `brand-50` / `brand-100` | #EEF3FF / #DDE7FF | Badges, icon tiles |
| Functional | `success` | #12A150 | Diagram "live" dots only |

Gradients are restrained: a brand-50 → white wash behind the hero, and one blurred brand-500 glow on navy bands.

### Typography

Geist Sans (self-hosted through the `geist` package, so no Google Fonts request at runtime) with tight negative tracking on headings. Instrument Serif (`@fontsource`) is available for rare editorial accents.

| Token | Size (fluid) | Line height | Tracking |
|---|---|---|---|
| `text-display` | 38 → 84px | 1.02 | -0.035em |
| `text-h1` | 36 → 60px | 1.05 | -0.03em |
| `text-h2` | 30 → 46px | 1.1 | -0.025em |
| `text-h3` | 20 → 24px | 1.25 | -0.015em |
| `text-lead` | 17 → 20px | 1.6 | — |
| `text-eyebrow` | 12px, uppercase | 1 | 0.14em |

### Spacing, layout, radius, shadow

- Tailwind's 4px spacing scale. `--section-y` (72 → 128px) is the vertical rhythm for sections, and `--gutter` (16 → 32px) is the side padding.
- Containers: `prose` 672px, `content` 1152px, `wide` 1280px.
- Radius: `xs` 6 (chips), `sm` 10 (buttons, inputs), `md` 14 (cards), `lg` 20 (panels), `xl` 28 (hero visual, CTA band).
- Shadows are low and navy-tinted: `xs`, `sm`, `md`, `lg`, plus `glow` for the primary button hover.
- Breakpoints use Tailwind defaults. Layouts were checked at 390px (mobile), 834px (tablet) and 1440px (desktop).

### Focus and motion

- One focus indicator site-wide: a 2px brand ring with a 3px offset. Inside `.on-dark` sections it switches to brand-300.
- A skip link appears as the first focusable element.
- Motion uses **Motion for React**, with `MotionConfig reducedMotion="user"`, and the global CSS respects `prefers-reduced-motion`. When reduced motion is on, the beams become static lines, the event log stops cycling, the marquee becomes a wrapped list and the spotlight is disabled.
- Where motion is used: a one-time 16px fade-up on scroll, beams travelling along the lead-flow paths, the event log ticker, and the cursor spotlight (pointer devices only). There is no parallax, flashing, custom cursor or scroll-jacking.

## Components

| Component | File | Notes |
|---|---|---|
| Button (primary, secondary, ghost, link, primary-dark, secondary-dark; sm/md/lg) + `ButtonArrow` | `components/ui/button.tsx` | shadcn-style, `asChild` for links |
| Badge, LiveDot, Eyebrow, SectionHeading, Card, IconTile, Container | `components/ui/primitives.tsx` | |
| Input, Textarea, Select, Label, Field | `components/ui/form.tsx` | `Field` wires up the label, hint, error and `aria-describedby` |
| AnimatedBeam | `components/ui/animated-beam.tsx` | **From 21st.dev**, adapted (see below) |
| Reveal, Spotlight, MotionProvider | `components/ui/motion.tsx` | |
| Header with mega menu + mobile sheet | `components/site/header.tsx` | Radix NavigationMenu + Dialog |
| LeadFlow (signature diagram) | `components/home/lead-flow.tsx` | Built on AnimatedBeam |
| Mockups (chat, mini pipeline, workflow, pipeline board) | `components/home/mockups.tsx` | Drawn in code, labelled "Example" |

## 21st.dev component selection

The free plan allows 2 code downloads per day, and **only 1 was left** today. Preview images are served from `cdn.21st.dev`, which my environment can't reach, so **I couldn't view previews visually**. I judged candidates on their descriptions, demo code and dependencies instead. Please look at the links below yourself before we commit to the remaining picks.

| Need | Candidate | Decision |
|---|---|---|
| Workflow diagram | [Animated Beam – dillionverma (Magic UI)](https://21st.dev/@dillionverma/components/animated-beam) | **Installed and adapted.** Zero extra dependencies. I swapped `framer-motion` for `motion/react`, applied brand colours, made the duration deterministic (the original used `Math.random`, which breaks hydration), fixed the React 19 ref types, and added a reduced-motion fallback. |
| Mega menu | [Rich Navigation Menu – shadcnui-blocks](https://21st.dev/@shadcnui-blocks/components/navigation-menu-06), [Navigation Menu – wensity](https://21st.dev/@wensity/components/navigation-menu) | **Pattern rebuilt on Radix NavigationMenu** (the same primitive these use), so it didn't need a paid download. Rejected [Directional Menu – hyperiux](https://21st.dev/@hyperiux/components/directional-menu) because it adds GSAP. |
| Hero spotlight | [Modern Hero (mouse-follow glow) – uniquesonu](https://21st.dev/@uniquesonu/components/modern-hero-section-1) | **Effect rebuilt** as a tiny CSS-variable spotlight. The original also had invented "trust stats", which we must not use. |
| Animated background | [Aurora Flow – ruixen.ui](https://21st.dev/@ruixen.ui/components/aurora-flow) | **Not used.** It adds a WebGL dependency (OGL). A static grid plus one blurred glow gives the same premium feel at almost no cost. |
| Bento services | [Animated Features Bento – kedhareswer](https://21st.dev/@kedhareswer/components/ink-orbit-features), [Bento Grid – kokonutd](https://21st.dev/@kokonutd/components/bento-grid) | **Layout built with CSS grid.** Our tiles carry service-specific vignettes, which off-the-shelf bento demos don't have. |
| Dashboard mockup | [Financial Hero – uilayout](https://21st.dev/@uilayout.contact/components/hero-financial) | Built our own pipeline board instead, so it shows the real product context (GHL pipeline stages). |
| Process timeline | [Scroll animated timeline – ibrandify](https://21st.dev/@ibrandify/components/scroll-timeline) | Candidate for tomorrow's download if you want a scroll-drawn line. A static version is in place now. |
| Testimonials / case studies | [Marquee – diceui](https://21st.dev/@diceui/components/marquee), [Testimonials Marquee – shadcnspace](https://21st.dev/@shadcnspace/components/marquee-01) | **Deferred** until real testimonials exist. The integrations strip uses a CSS marquee with pause-on-hover and reduced-motion support. |
| Animated CTA button | — | Built in: arrow nudge plus a soft glow on hover. Nothing heavier is needed. |

## Verified

- `npm run lint`, `tsc --noEmit` and `npm run build` all pass. Every route is statically prerendered.
- Playwright screenshots of `/`, `/directions` and `/design-system` at 390, 834 and 1440px showed no console errors and no horizontal scroll.
- axe-core (WCAG 2.0/2.1 A and AA plus best practices) found **0 violations** on all three pages at desktop and mobile widths, after I fixed two issues it caught (list semantics in the process timeline, and contrast on the hub label).

## Known gaps / next

- First-load JS on `/` is 199 KB, mostly Motion and Radix. Switching to `LazyMotion` and loading the lead-flow diagram on demand should bring it under the 170 KB budget.
- The logo, booking link, diagnostic link, integrations list and FAQ answers all need owner confirmation (they're marked `TODO(content)` and `TODO(brand)` in the code).
- I haven't added a dark-mode toggle. The design uses navy bands rather than a full dark theme, as the brief asked.
