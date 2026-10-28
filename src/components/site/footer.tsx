import Link from "next/link";

import { Logo } from "@/components/site/logo";
import { services, site } from "@/lib/content";

export function SiteFooter() {
  return (
    <footer className="on-dark bg-navy-950 text-navy-300">
      <div className="container-site grid gap-12 py-16 md:grid-cols-[1.4fr_1fr_1fr]">
        <div className="max-w-sm">
          <Logo tone="dark" />
          <p className="mt-4 text-sm leading-relaxed">{site.description}</p>
        </div>
        <nav aria-label="Services">
          <p className="text-sm font-semibold text-white">Services</p>
          <ul className="mt-4 grid gap-2.5 text-sm">
            {services.map((s) => (
              <li key={s.slug}>
                <Link href="/#services" className="hover:text-white">
                  {s.title}
                </Link>
              </li>
            ))}
          </ul>
        </nav>
        <nav aria-label="Company">
          <p className="text-sm font-semibold text-white">Company</p>
          <ul className="mt-4 grid gap-2.5 text-sm">
            <li>
              <Link href="/#process" className="hover:text-white">
                How we work
              </Link>
            </li>
            <li>
              <Link href="/#faq" className="hover:text-white">
                FAQ
              </Link>
            </li>
            <li>
              <Link href={site.bookingHref} className="hover:text-white">
                Contact
              </Link>
            </li>
          </ul>
        </nav>
      </div>
      <div className="border-t border-navy-800">
        <div className="container-site flex flex-col gap-2 py-6 text-[0.8125rem] sm:flex-row sm:justify-between">
          <p>© {new Date().getFullYear()} Your Marketing AI. All rights reserved.</p>
          {/* TODO(content): link privacy and terms pages once written */}
          <p>Privacy · Terms</p>
        </div>
      </div>
    </footer>
  );
}
