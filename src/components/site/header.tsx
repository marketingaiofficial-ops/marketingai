"use client";

import * as React from "react";
import Link from "next/link";
import * as NavigationMenu from "@radix-ui/react-navigation-menu";
import * as Dialog from "@radix-ui/react-dialog";
import { ChevronDown, Menu, X } from "lucide-react";

import { Logo } from "@/components/site/logo";
import { ServiceIcon } from "@/components/site/service-icon";
import { Button, ButtonArrow } from "@/components/ui/button";
import { serviceGroups, services, site } from "@/lib/content";
import { cn } from "@/lib/utils";

/*
 * Mega menu built on Radix NavigationMenu (the primitive behind shadcn's navigation-menu),
 * with the grouped, icon-and-description panel pattern from the 21st.dev candidates
 * "Rich Navigation Menu" (shadcnui-blocks) and "Navigation Menu" (wensity).
 * Radix gives us keyboard support, focus management and aria-expanded for free.
 */

const links = [
  { href: "/#process", label: "How we work" },
  { href: "/#faq", label: "FAQ" },
  { href: "/design-system", label: "Design system" },
];

export function SiteHeader() {
  const [scrolled, setScrolled] = React.useState(false);

  React.useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 8);
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  return (
    <header
      className={cn(
        "sticky top-0 z-50 transition-[background-color,box-shadow] duration-300",
        scrolled
          ? "bg-white/85 shadow-[0_1px_0_var(--color-line)] backdrop-blur-md"
          : "bg-white/0",
      )}
    >
      <div className="container-site flex h-16 items-center justify-between gap-6 md:h-[4.5rem]">
        <Logo />

        <NavigationMenu.Root className="relative hidden lg:block" delayDuration={80}>
          <NavigationMenu.List className="flex items-center gap-1">
            <NavigationMenu.Item>
              <NavigationMenu.Trigger className="group inline-flex h-10 items-center gap-1 rounded-sm px-3.5 text-[0.9375rem] font-medium text-ink transition-colors hover:bg-paper-2 data-[state=open]:bg-paper-2">
                Services
                <ChevronDown
                  aria-hidden="true"
                  className="size-4 text-ink-muted transition-transform duration-200 group-data-[state=open]:rotate-180"
                />
              </NavigationMenu.Trigger>
              <NavigationMenu.Content className="absolute top-0 left-0 w-[min(56rem,calc(100vw-4rem))] data-[motion=from-end]:animate-none">
                <ServicesPanel />
              </NavigationMenu.Content>
            </NavigationMenu.Item>
            {links.map((l) => (
              <NavigationMenu.Item key={l.href}>
                <NavigationMenu.Link asChild>
                  <Link
                    href={l.href}
                    className="inline-flex h-10 items-center rounded-sm px-3.5 text-[0.9375rem] font-medium text-ink transition-colors hover:bg-paper-2"
                  >
                    {l.label}
                  </Link>
                </NavigationMenu.Link>
              </NavigationMenu.Item>
            ))}
          </NavigationMenu.List>
          <div className="absolute top-full left-0 pt-3">
            <NavigationMenu.Viewport className="relative h-(--radix-navigation-menu-viewport-height) w-(--radix-navigation-menu-viewport-width) origin-top-left overflow-hidden rounded-lg bg-white shadow-lg ring-1 ring-line transition-[width,height,opacity,transform] duration-200 data-[state=closed]:scale-[0.98] data-[state=closed]:opacity-0 data-[state=open]:scale-100 data-[state=open]:opacity-100" />
          </div>
        </NavigationMenu.Root>

        <div className="flex items-center gap-2">
          <Button asChild variant="ghost" size="sm" className="hidden md:inline-flex">
            <Link href={site.diagnosticHref}>Find my lead leaks</Link>
          </Button>
          <Button asChild size="sm" className="hidden sm:inline-flex">
            <Link href={site.bookingHref}>
              Book a strategy call
              <ButtonArrow />
            </Link>
          </Button>
          <MobileNav />
        </div>
      </div>
    </header>
  );
}

function ServicesPanel() {
  return (
    <div className="grid grid-cols-[1fr_1fr_1fr_15rem] gap-1 p-3">
      {serviceGroups.map(({ group, blurb }) => (
        <div key={group} className="flex flex-col gap-1 p-2">
          <p className="px-2 pt-1 pb-2">
            <span className="block text-eyebrow font-semibold text-brand-600 uppercase">{group}</span>
            <span className="mt-1.5 block text-[0.8125rem] text-ink-muted">{blurb}</span>
          </p>
          {services
            .filter((s) => s.group === group)
            .map((s) => (
              <NavigationMenu.Link asChild key={s.slug}>
                <Link
                  href={`/#services`}
                  className="group/item flex gap-3 rounded-sm p-2 transition-colors hover:bg-paper focus-visible:bg-paper"
                >
                  <span className="mt-0.5 grid size-8 shrink-0 place-items-center rounded-xs bg-brand-50 text-brand-600 ring-1 ring-brand-100 ring-inset transition-colors group-hover/item:bg-brand-500 group-hover/item:text-white">
                    <ServiceIcon name={s.icon} className="size-4" />
                  </span>
                  <span>
                    <span className="block text-sm font-medium text-ink">{s.title}</span>
                    <span className="mt-0.5 block text-[0.8125rem] leading-snug text-ink-muted">
                      {s.short}
                    </span>
                  </span>
                </Link>
              </NavigationMenu.Link>
            ))}
        </div>
      ))}
      <NavigationMenu.Link asChild>
        <Link
          href={site.diagnosticHref}
          className="group/feat relative flex flex-col justify-between overflow-hidden rounded-md bg-navy-900 p-5 text-white"
        >
          <span aria-hidden="true" className="bg-grid-dark absolute inset-0 opacity-60" />
          <span
            aria-hidden="true"
            className="absolute -top-16 -right-16 size-48 rounded-full bg-brand-500/40 blur-3xl"
          />
          <span className="relative text-eyebrow font-semibold text-brand-300 uppercase">
            Free diagnostic
          </span>
          <span className="relative mt-10">
            <span className="block text-lg leading-tight font-semibold">
              Find where your pipeline leaks
            </span>
            <span className="mt-2 block text-[0.8125rem] text-navy-300">
              Answer a few questions and see your lead flow mapped.
            </span>
            <span className="mt-4 inline-flex items-center gap-1.5 text-sm font-medium text-brand-300 group-hover/feat:text-white">
              Start the diagnostic <span aria-hidden="true">→</span>
            </span>
          </span>
        </Link>
      </NavigationMenu.Link>
    </div>
  );
}

function MobileNav() {
  const [open, setOpen] = React.useState(false);
  return (
    <Dialog.Root open={open} onOpenChange={setOpen}>
      <Dialog.Trigger asChild>
        <button
          type="button"
          className="inline-grid size-10 place-items-center rounded-sm text-ink ring-1 ring-line ring-inset hover:bg-paper-2 lg:hidden"
          aria-label="Open menu"
        >
          <Menu className="size-5" aria-hidden="true" />
        </button>
      </Dialog.Trigger>
      <Dialog.Portal>
        <Dialog.Overlay className="fixed inset-0 z-50 bg-navy-950/40 backdrop-blur-sm" />
        <Dialog.Content className="fixed inset-y-0 right-0 z-50 flex w-full max-w-sm flex-col bg-white shadow-lg focus:outline-none">
          <div className="flex h-16 items-center justify-between px-(--gutter)">
            <Dialog.Title className="sr-only">Menu</Dialog.Title>
            <Dialog.Description className="sr-only">Site navigation</Dialog.Description>
            <Logo />
            <Dialog.Close
              className="inline-grid size-10 place-items-center rounded-sm text-ink ring-1 ring-line ring-inset hover:bg-paper-2"
              aria-label="Close menu"
            >
              <X className="size-5" aria-hidden="true" />
            </Dialog.Close>
          </div>
          <nav aria-label="Mobile" className="flex-1 overflow-y-auto px-(--gutter) pb-6">
            {serviceGroups.map(({ group }) => (
              <div key={group} className="border-b border-line py-4">
                <p className="text-eyebrow font-semibold text-brand-600 uppercase">{group}</p>
                <ul className="mt-2">
                  {services
                    .filter((s) => s.group === group)
                    .map((s) => (
                      <li key={s.slug}>
                        <Link
                          href="/#services"
                          onClick={() => setOpen(false)}
                          className="flex items-center gap-3 rounded-sm py-2.5 text-[0.9375rem] font-medium text-ink"
                        >
                          <ServiceIcon name={s.icon} className="size-4 text-brand-600" />
                          {s.title}
                        </Link>
                      </li>
                    ))}
                </ul>
              </div>
            ))}
            <ul className="py-4">
              {links.map((l) => (
                <li key={l.href}>
                  <Link
                    href={l.href}
                    onClick={() => setOpen(false)}
                    className="block rounded-sm py-2.5 text-[0.9375rem] font-medium text-ink"
                  >
                    {l.label}
                  </Link>
                </li>
              ))}
            </ul>
          </nav>
          <div className="grid gap-2 border-t border-line p-(--gutter)">
            <Button asChild size="lg">
              <Link href={site.bookingHref} onClick={() => setOpen(false)}>
                Book a strategy call
                <ButtonArrow />
              </Link>
            </Button>
            <Button asChild variant="secondary" size="lg">
              <Link href={site.diagnosticHref} onClick={() => setOpen(false)}>
                Find my lead leaks
              </Link>
            </Button>
          </div>
        </Dialog.Content>
      </Dialog.Portal>
    </Dialog.Root>
  );
}
