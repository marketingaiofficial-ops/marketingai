# Website Audit: Your Marketing AI

_Phase 1 audit, 28 Oct 2026. No implementation code was written._

## 0. What I could and could not inspect

Being explicit here because the rest of this audit depends on it.

| Source | Status | What I actually saw |
|---|---|---|
| GitHub repos for `marketingaiofficial-ops` | Inspected | 4 repos. `marketingai` and `fly` are **empty** (no commits, no branches). `REA-for-any-app` and `dograh-marketing-ai` are forks of third-party projects, not the website. |
| Lovable workspaces (3 workspaces, 27 projects) | Listed | No project is clearly the public website. Closest relatives: **Marketing AI Flow** (published lead-leak diagnostic) and **Marketing AI Setup Companion** (internal onboarding tool). Neither is configured, as far as I can see, to serve yourmarketingai.com. |
| https://yourmarketingai.com/ (homepage) | **Partially inspected** | Only the HTML `<head>` was retrievable. The body renders client-side with JavaScript, and my sandbox's network policy blocks a real browser from loading the domain, so I could **not** see the rendered homepage, navigation, sections, forms, or mobile layout. |
| https://yourmarketingai.com/robots.txt | Inspected | Allows all crawlers. Content matches the default robots.txt that Lovable generates. |
| https://yourmarketingai.com/sitemap.xml | Inspected | Returns the app shell instead of a sitemap, so **no sitemap exists**. |
| https://atheostech.com/ | **Partially inspected** | Text content and structure via a text fetcher. I could not see visuals, motion, colors, or the real mobile experience. |
| Search engine visibility | Checked | A `site:yourmarketingai.com` search returned no pages from the domain. |

**Implication:** sections 2 to 4 below are the parts I could verify. Everything I could not verify is listed in section 5 as an open item. Before Phase 2 starts, I need either (a) the source of the current site, or (b) screenshots or a screen recording of the desktop and mobile homepage, so nothing useful gets lost.

## 1. Repository and technical setup

**No working application exists in any connected repository.** I could not identify a framework, dependencies, routes, components, styling system, build commands, integrations or deployment setup from source.

What the live site reveals from the outside:

- **Rendering:** client-side single-page app. The server sends an empty shell, and JavaScript fills it in. Crawlers and link previews only see the `<head>`.
- **Likely origin:** Lovable (React + Vite + Tailwind + shadcn/ui is Lovable's default stack). The evidence is the robots.txt format and the SPA fallback on unknown routes. This is a reasoned guess, not confirmed.
- **Hosting:** unknown. It is probably Lovable hosting with a custom domain, but I can't confirm that.
- **Integrations:** none detectable from the head (no analytics, pixel, chat widget or calendar script were visible to me).

Related assets you already own that the rebuild can reuse:

- **Marketing AI Flow** (Lovable, published): a 10-step "Where am I losing sales?" diagnostic that builds a visual flow map of lead sources, qualification and follow-up. This is the strongest conversion asset I found and a good fit for a site-wide lead magnet.
- **Marketing AI Setup Companion** (Lovable, published, internal): the onboarding wizard for client sub-accounts. It is internal only and should not be linked publicly, but it shows the delivery process you can describe on the site.

## 2. Current homepage (from what was visible)

| Element | Current state | Assessment |
|---|---|---|
| `<title>` | "Marketing AI — AI that runs your business" | Brand is "Marketing AI", not "Your Marketing AI". It is generic and competes with many products named "MarketingAI". It doesn't mention GoHighLevel, CRM or automation. |
| Meta description | "Marketing AI is the AI that runs your business." / "Replies to new leads in seconds, qualifies them automatically, and follows up on autopilot." | It's a clear outcome promise, but it positions the company as a **software product**, while the business is a **services and implementation agency**. |
| Open Graph / Twitter image | Declared but **empty** | Shared links on LinkedIn, WhatsApp and X show no image. This is a quick fix. |
| Twitter handle | `@MarketingAI` | **Verify that this handle belongs to you.** If it doesn't, remove it. |
| Canonical URL | og:url is `/` (relative) | Should be absolute: `https://yourmarketingai.com/`. |
| Structured data | None seen | No Organization, ProfessionalService, Service or FAQ schema. |

## 3. Audit by area

### Positioning and messaging
- **Mismatch between the site and the business.** The site sells "AI that runs your business" as if it were a product. The real business (GoHighLevel services, CRM implementation, workflow automation, AI agents, lead generation systems, pipelines, funnels, websites and process automation) is never named in anything I could see.
- **Brand name inconsistency:** "Marketing AI", "Your Marketing AI", "YourMarketingAI" and "Marketing AI / The Visionary Web" all appear across your assets. Pick one public name and one legal or parent line.
- **No GoHighLevel mention.** "GoHighLevel" and "GHL" are high-intent search terms. Buyers who already pay for GHL and need it implemented are the easiest customers to win.

### Navigation and service discovery
- Not visible to me. See section 5.
- Recommendation regardless of the current state: services need their own crawlable pages, because a single-page app with in-page anchors can't rank for "GoHighLevel CRM setup", "AI voice agent for clinics" and similar terms.

### CTAs and conversion flow
- Not visible on the live site. In the related Lovable asset (Marketing AI Flow), the CTA is "Where am I losing sales?", followed by a name field and an optional company field, with the note "~3 minutes · Built live as you answer". That is a good low-friction pattern worth keeping.
- **Missing, as far as I could check:** a booking path (strategy call), a phone or WhatsApp contact route, and any way to qualify leads by budget, platform or timeline.

### Mobile
- Not verifiable. The Lovable defaults are responsive, but layout, tap targets and performance on real devices are unknown.

### SEO
| Issue | Severity | Evidence |
|---|---|---|
| Client-side rendering only, so crawlers get an empty body | **High** | The fetched HTML contained only the head |
| No sitemap.xml | High | /sitemap.xml returns the app shell |
| Site doesn't appear in search results | High | `site:` search returned no domain pages (the search tool may lag, so confirm in Google Search Console) |
| No service-specific pages or keywords | High | Title and description are generic |
| Empty OG image | Medium | Head meta |
| Relative og:url and no canonical tag | Low | Head meta |
| No structured data | Medium | Head meta |

### Forms
- Not visible on the live site. For the rebuild, every form should send leads **into your own GoHighLevel account** (dogfooding is part of the pitch), with source and UTM fields so you can attribute leads.

### Visual consistency
- Not verifiable on the live site. Across your Lovable assets the visual language varies: a blue-to-pink gradient wordmark on Marketing AI Flow, and flat blue on the Setup Companion. There is no shared design system yet.

## 4. Marketing claims that need verification

None of these should be published again until you confirm them with evidence:

| Claim | Where | What's needed |
|---|---|---|
| "Replies to new leads in seconds" | Live meta description | True only if the delivered system does it. Phrase it as a capability ("can reply within seconds") rather than a guarantee. |
| "Qualifies them automatically, follows up on autopilot" | Live meta description | Fine as a capability description. Avoid "autopilot" if any human setup or oversight is involved. |
| "Every lead replied in under 5 minutes on WhatsApp" | Marketing AI Flow | Specific and measurable. Needs real data or should be softened. Also depends on WhatsApp Business API approval. |
| "Never lose a lead again" | Marketing AI Flow tagline | An absolute guarantee. Rephrase it. |
| "AI that runs your business" | Live title | Overclaims for a services firm. Replace it. |
| `@MarketingAI` X handle | Live meta | Confirm ownership. |

I will not add clients, logos, testimonials, statistics, awards, certifications (for example "GoHighLevel Certified Admin"), or guarantees unless you provide them with proof.

## 5. Open items I could not verify

1. Rendered homepage sections, copy, imagery and footer.
2. Navigation structure and any other pages or routes.
3. Existing forms, where submissions go, and the booking calendar.
4. Analytics, Meta Pixel, Google Tag Manager, and chat widget.
5. Mobile layout and Core Web Vitals (I couldn't run Lighthouse against the domain).
6. Hosting and DNS (Lovable, Vercel, GHL or another host).
7. Which Lovable project (if any) is the live site.

**The quickest unblock:** tell me which Lovable project (or other tool) serves yourmarketingai.com, or send desktop and mobile screenshots.

## 6. Preserve, improve, remove, rebuild

| Action | Item |
|---|---|
| **Preserve** | Lead-leak framing ("where your pipeline leaks and what it's costing you"); the Marketing AI Flow diagnostic as a lead magnet; the speed-to-lead → CRM → follow-up three-step story; the domain yourmarketingai.com |
| **Improve** | Brand name consistency; title and meta copy; OG image; clear services language (GHL, CRM, automation, AI agents); low-friction CTA plus a booking CTA |
| **Remove** | "AI that runs your business"; absolute guarantees; the unverified social handle; any public link to the internal onboarding tool |
| **Rebuild** | The whole site as a server-rendered or statically generated multi-page site with dedicated service, industry and process pages, a sitemap, schema and GHL-connected forms |

## 7. Reference site: AtheosTech (text-level inspection only)

What's worth learning from, without copying content, layout, identity or assets:

- **Linear narrative:** promise, company intro, services, "why choose us", process and quality, a low-risk consultation offer, then a soft closing CTA ("Still thinking?").
- **CTAs repeated at intervals** with conversational, low-pressure wording.
- **Service cards** that each carry a one-line benefit.
- **Accessibility signals:** skip links and a cookie notice with settings.
- **Gaps to beat them on:** no visible testimonials, case studies or metrics; the navigation lists services (QA/Testing, Project Management) that have no matching cards; the story is generic ("IT consulting") rather than outcome-led.

I could not evaluate its visual design, motion, or mobile experience.
