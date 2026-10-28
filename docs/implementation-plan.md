# Implementation Plan: Your Marketing AI Website Rebuild

## 1. Recommended architecture

There is no existing codebase to preserve (see `website-audit.md` §0–1), so I propose a fresh build.

| Layer | Choice | Why |
|---|---|---|
| Framework | **Next.js 15 (App Router) + TypeScript** | Static generation and server rendering fix the biggest current problem: crawlers see an empty page. It also gives file-based routes for service pages, a built-in metadata API, and generated sitemap.xml and robots.txt. |
| Styling | **Tailwind CSS v4 + shadcn/ui** | 21st.dev components are shadcn-compatible. This matches the stack in your Lovable projects, so patterns and components carry over. |
| Motion | **Motion (Framer Motion)**. Add GSAP only if the directional mega menu is chosen. | Standard for 21st components. Reduced-motion support is built in. |
| Content | MDX files in the repo for service pages, FAQ and (later) blog posts | No CMS cost, version-controlled, fast. Can move to a headless CMS later if non-developers need to edit. |
| Forms and leads | Server action → **GoHighLevel API (v2, private integration token)** creates or updates the contact with tags, source and UTMs, and can trigger a workflow. Fallback: a GHL inbound webhook. | Leads land in your own CRM, which also demonstrates your service. |
| Booking | Embedded **GHL calendar** widget on /contact and in CTA modals | Native to your stack. |
| Diagnostic | Phase 3: rebuild the Marketing AI Flow diagnostic as a native /diagnostic route. Phase 1–2 fallback: link out to the existing Lovable app. | Keeps one domain, one analytics setup and one lead path. |
| Analytics | GA4 or Plausible, plus Meta Pixel / GTM if you run ads, all behind a consent banner | Consent is needed for EU/UK visitors given the "international" positioning. |
| Hosting | **Vercel** (simplest for Next.js). **Render** is the alternative, since you already have it connected. | Preview deploys per pull request, edge CDN. |
| Repo | `marketingaiofficial-ops/marketingai` (currently empty) | Confirm this is the right home. See the decision at the end. |

**Alternative if you'd rather stay in Lovable:** Lovable now offers TanStack Start with SSR (used in your BlueWork HR Build project). That keeps your no-code editing loop, but you get less control over SEO details, performance budgets and 21st component integration. I recommend Next.js in GitHub. Lovable can still be used for prototypes.

## 2. Already available, so nothing new to buy or install yet

- **Skills:** 21st-ui (component research and install), marketing:seo-audit, marketing:content-creation, marketing:brand-review (claims screening), design:accessibility-review, design:ux-copy, engineering:code-review / testing-strategy, render:* (if hosting on Render).
- **Tools and connectors:** 21st.dev MCP (search works; free tier allows 2 installs per day), Lovable MCP (read your existing projects), GitHub, Render MCP (it failed to connect in this session; needs reconnecting if we use Render).
- **Local toolchain:** Node 22, npm 10, pnpm 10, Playwright with Chromium (for screenshots and visual QA of preview deploys).
- **Not available:** a live browser view of yourmarketingai.com or atheostech.com from my environment (network policy). Ahrefs, Similarweb and Figma connectors failed to connect this session.

## 3. Phases and milestones

### Phase 0: Unblock (½ day, mostly on you)
- Confirm the repo, brand name, regions and industries, and the proof you can publish.
- Provide the current site source or desktop and mobile screenshots.
- Provide a GHL private integration token and target location ID (stored as an environment secret, never committed), plus your calendar embed.
- **Exit:** the decisions in design-direction.md §8 are answered.

### Phase 1: Foundation (2–3 days)
- Scaffold Next.js, TypeScript, Tailwind v4, shadcn/ui, ESLint/Prettier, and a CI workflow (typecheck, lint, build).
- Design tokens (colors, type, radii, motion) and base primitives.
- Layout: header with mega menu (desktop and mobile), footer, skip link, consent banner.
- SEO plumbing: metadata helper, absolute canonical URLs, generated OG images, sitemap.xml, robots.txt, Organization and ProfessionalService JSON-LD.
- Deploy previews on Vercel or Render.
- **Acceptance:** a preview URL renders the shell. Lighthouse mobile scores are ≥ 95 for SEO, accessibility and best practices. Keyboard navigation works through the whole mega menu. View-source shows real HTML content.

### Phase 2: Homepage and conversion path (4–5 days)
- All homepage sections from design-direction.md §5, with copy drafted from your real services and run through a claims check.
- The signature lead-flow walkthrough (Animated Beam base plus custom nodes).
- Contact page: form → GHL contact with tags and UTMs → thank-you state. GHL calendar embed. WhatsApp link.
- Analytics events: CTA clicks, form start and submit, booking.
- **Acceptance:** a test submission appears in GHL with the correct tags and source within 10 seconds. The form validates on client and server and is spam protected (honeypot plus rate limit). Mobile LCP is under 2.5s and CLS under 0.1 on the preview build. No unverified claims remain in the copy.

### Phase 3: Service discovery depth (4–6 days)
- Six service pages from an MDX template: problem, what we build, deliverables, process, integrations, FAQ, CTA.
- /services overview with a problem-led selector. /how-we-work. /about.
- Native /diagnostic (port of Marketing AI Flow logic) with results that route into GHL.
- Service and FAQ JSON-LD on each page.
- **Acceptance:** every service is reachable in two clicks or fewer from any page. Each page has a unique title and description and passes Rich Results Test validation. The diagnostic completes in about 3 minutes and creates a tagged GHL contact.

### Phase 4: Proof, pricing and growth (ongoing)
- Pricing or engagement models (if approved), case study template, testimonials (only real ones, with permission).
- Optional /solutions/[industry] pages and blog.
- Google Search Console and Bing verification, then submit the sitemap.
- **Acceptance:** pages are indexed in GSC. Conversion baselines are recorded.

### Phase 5: Launch and cutover (1 day)
- Set up 301 redirects from any old URLs, point DNS at the new host, verify SSL, and check OG previews on LinkedIn and WhatsApp.
- Keep the old site's host warm for 7 days as a rollback.
- **Acceptance:** zero 404s on known old URLs, forms are live in GHL, and analytics is receiving events.

## 4. Dependencies

| Dependency | Needed by | Owner |
|---|---|---|
| Repo confirmation | Phase 1 | You |
| Brand name, regions, industries | Phase 2 copy | You |
| GHL API token, location ID, calendar | Phase 2 forms | You |
| Real proof assets | Phase 4 | You |
| DNS access for yourmarketingai.com | Phase 5 | You |
| 21st.dev API key with 2 installs/day (or a paid plan) | Phases 1–3 | You (the key is already configured, so this is only a pacing constraint) |

## 5. Risks

| Risk | Impact | Mitigation |
|---|---|---|
| Losing content or features from the current site that I couldn't see | Medium | Get the source or screenshots in Phase 0 and do a content inventory before cutover |
| Overclaiming (legal and trust) | High | Claims checklist on every page. Capability language only. The marketing:brand-review pass runs before launch. |
| Heavy animation hurting mobile performance | Medium | Performance budget (JS under 170KB gzipped on the homepage), lazy-loaded diagrams, reduced-motion fallbacks, no WebGL above the fold |
| 21st component licensing or quality varies | Low | Review each component's code before install, restyle it to our tokens, and keep a list of what's installed and its source |
| 21st free-tier install limit | Low | Sequence installs (nav and beam first, then bento and timeline). Build simple pieces ourselves. |
| GHL API rate limits or token scope | Low | Server-side calls only, retry with backoff, webhook fallback |
| DNS cutover downtime | Low | Lower the TTL 48h before, make the switch in a low-traffic window, keep the rollback host |
| Looking like an AI template | Medium | Follow the principles in design-direction.md §7, plus a design review checkpoint after Phase 2 |

## 6. Definition of done (whole project)

- Server-rendered or static HTML for every public page, with a sitemap and schema.
- Lighthouse mobile scores ≥ 90 for performance and ≥ 95 for accessibility, best practices and SEO on the home and service pages.
- WCAG 2.2 AA: contrast, focus states, keyboard navigation, reduced motion.
- Every lead path writes to GHL with source attribution.
- No invented clients, testimonials, statistics, awards, certifications or guarantees.
- README with setup, environment variables, deploy steps and a content-editing guide.
