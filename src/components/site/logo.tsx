import Link from "next/link";

import { cn } from "@/lib/utils";

/*
 * TODO(brand): placeholder wordmark. No official logo file was available when this was built.
 * Replace the contents of this component with the official SVG and keep the same props.
 */
export function Logo({
  tone = "light",
  className,
}: {
  tone?: "light" | "dark";
  className?: string;
}) {
  return (
    <Link
      href="/"
      aria-label="Your Marketing AI, home"
      className={cn("inline-flex items-center gap-2.5 rounded-sm", className)}
    >
      <span
        aria-hidden="true"
        className={cn(
          "grid size-8 place-items-center rounded-[9px] text-[0.8125rem] font-bold tracking-tight",
          tone === "light" ? "bg-navy-900 text-white" : "bg-white text-navy-900",
        )}
      >
        <span className="translate-y-px">
          M<span className="text-brand-500">.</span>
        </span>
      </span>
      <span
        className={cn(
          "text-[0.9375rem] font-semibold tracking-tight",
          tone === "light" ? "text-ink" : "text-white",
        )}
      >
        Your Marketing AI
      </span>
    </Link>
  );
}
