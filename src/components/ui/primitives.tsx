import * as React from "react";
import { cva, type VariantProps } from "class-variance-authority";

import { cn } from "@/lib/utils";

/* ---------- Container ---------- */

export function Container({
  className,
  size = "wide",
  ...props
}: React.HTMLAttributes<HTMLDivElement> & { size?: "prose" | "content" | "wide" }) {
  return (
    <div
      className={cn(
        "mx-auto w-full px-(--gutter)",
        size === "prose" && "max-w-(--container-prose)",
        size === "content" && "max-w-(--container-content)",
        size === "wide" && "max-w-(--container-wide)",
        className,
      )}
      {...props}
    />
  );
}

/* ---------- Badge ---------- */

const badgeVariants = cva(
  "inline-flex items-center gap-1.5 rounded-full font-medium whitespace-nowrap",
  {
    variants: {
      variant: {
        brand: "bg-brand-50 text-brand-700 ring-1 ring-brand-100 ring-inset",
        neutral: "bg-paper-2 text-ink-muted ring-1 ring-line ring-inset",
        outline: "text-ink ring-1 ring-line-strong ring-inset",
        dark: "bg-navy-800 text-brand-300 ring-1 ring-navy-700 ring-inset",
        success: "bg-success/10 text-[#0b7a3b] ring-1 ring-success/20 ring-inset",
      },
      size: {
        sm: "px-2 py-0.5 text-xs",
        md: "px-3 py-1 text-[0.8125rem]",
      },
    },
    defaultVariants: { variant: "brand", size: "md" },
  },
);

export function Badge({
  className,
  variant,
  size,
  ...props
}: React.HTMLAttributes<HTMLSpanElement> & VariantProps<typeof badgeVariants>) {
  return <span className={cn(badgeVariants({ variant, size }), className)} {...props} />;
}

/** Small live indicator dot, used in badges and diagrams. */
export function LiveDot({ className }: { className?: string }) {
  return (
    <span
      aria-hidden="true"
      className={cn("size-1.5 rounded-full bg-success animate-pulse-dot", className)}
    />
  );
}

/* ---------- Eyebrow + Section heading ---------- */

export function Eyebrow({
  className,
  tone = "light",
  ...props
}: React.HTMLAttributes<HTMLParagraphElement> & { tone?: "light" | "dark" }) {
  return (
    <p
      className={cn(
        "text-eyebrow font-semibold uppercase",
        tone === "light" ? "text-brand-600" : "text-brand-300",
        className,
      )}
      {...props}
    />
  );
}

export function SectionHeading({
  eyebrow,
  title,
  lead,
  align = "left",
  tone = "light",
  as: Heading = "h2",
  className,
}: {
  eyebrow?: string;
  title: React.ReactNode;
  lead?: React.ReactNode;
  align?: "left" | "center";
  tone?: "light" | "dark";
  as?: "h1" | "h2" | "h3";
  className?: string;
}) {
  return (
    <div
      className={cn(
        "flex max-w-3xl flex-col gap-4",
        align === "center" && "mx-auto items-center text-center",
        className,
      )}
    >
      {eyebrow ? <Eyebrow tone={tone}>{eyebrow}</Eyebrow> : null}
      <Heading
        className={cn(
          "font-semibold",
          Heading === "h1" ? "text-h1" : "text-h2",
          tone === "light" ? "text-ink" : "text-white",
        )}
      >
        {title}
      </Heading>
      {lead ? (
        <p
          className={cn(
            "max-w-2xl text-lead",
            tone === "light" ? "text-ink-muted" : "text-navy-300",
          )}
        >
          {lead}
        </p>
      ) : null}
    </div>
  );
}

/* ---------- Card ---------- */

const cardVariants = cva("relative rounded-md", {
  variants: {
    variant: {
      default: "bg-white ring-1 ring-line shadow-xs",
      raised: "bg-white ring-1 ring-line shadow-md",
      muted: "bg-paper ring-1 ring-line",
      dark: "bg-navy-800/60 ring-1 ring-navy-700 text-white",
    },
    interactive: {
      true: "transition-[box-shadow,transform,--tw-ring-color] duration-300 ease-out hover:-translate-y-0.5 hover:shadow-md hover:ring-brand-200",
      false: "",
    },
  },
  defaultVariants: { variant: "default", interactive: false },
});

export function Card({
  className,
  variant,
  interactive,
  ...props
}: React.HTMLAttributes<HTMLDivElement> & VariantProps<typeof cardVariants>) {
  return <div className={cn(cardVariants({ variant, interactive }), className)} {...props} />;
}

/** Square icon tile used at the top of service and feature cards. */
export function IconTile({
  children,
  tone = "light",
  className,
}: {
  children: React.ReactNode;
  tone?: "light" | "dark";
  className?: string;
}) {
  return (
    <span
      aria-hidden="true"
      className={cn(
        "inline-flex size-10 items-center justify-center rounded-sm [&_svg]:size-5",
        tone === "light"
          ? "bg-brand-50 text-brand-600 ring-1 ring-brand-100 ring-inset"
          : "bg-navy-800 text-brand-300 ring-1 ring-navy-700 ring-inset",
        className,
      )}
    >
      {children}
    </span>
  );
}

export { badgeVariants, cardVariants };
