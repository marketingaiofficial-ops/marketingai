# Your Marketing AI website

Next.js 15 (App Router) + TypeScript + Tailwind CSS v4 + Radix primitives + Motion.

## Run it

```bash
npm install
npm run dev      # http://localhost:3000
npm run build    # production build (all routes statically prerendered)
npm run lint
```

## Routes (prototype)

- `/`: recommended homepage direction
- `/directions`: the three visual directions explored
- `/design-system`: live reference for tokens and components

## Where things live

- `src/app/globals.css`: design tokens (colour, type scale, radius, shadow, motion)
- `src/components/ui/`: reusable primitives (button, badge, card, form controls, motion helpers, animated beam)
- `src/components/site/`: header with mega menu, footer, logo (placeholder)
- `src/components/home/`: homepage sections and mockups
- `src/lib/content.ts`: all copy and service data
- `docs/`: audit, design direction, design system and implementation plan

## Content rules

Never add clients, testimonials, statistics, awards, certifications or guarantees without proof from the business. Mockups use placeholder data and show an "Example" label.
