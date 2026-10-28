"use client";

import * as React from "react";
import { MotionConfig, motion, type HTMLMotionProps } from "motion/react";

import { cn } from "@/lib/utils";

/** App-wide motion defaults. reducedMotion="user" turns transforms off for people who ask. */
export function MotionProvider({ children }: { children: React.ReactNode }) {
  return (
    <MotionConfig reducedMotion="user" transition={{ duration: 0.5, ease: [0.16, 1, 0.3, 1] }}>
      {children}
    </MotionConfig>
  );
}

/** Fade-and-rise once when scrolled into view. Short distance, no blur, no stagger chains. */
export function Reveal({
  className,
  delay = 0,
  ...props
}: HTMLMotionProps<"div"> & { delay?: number }) {
  return (
    <motion.div
      className={cn(className)}
      initial={{ opacity: 0, y: 16 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, margin: "0px 0px -10% 0px" }}
      transition={{ delay }}
      {...props}
    />
  );
}

/**
 * Cursor spotlight: a soft brand-tinted glow that follows the pointer inside its parent.
 * Pattern from the 21st.dev "Modern Hero section" mouse-follow glow, rebuilt with CSS
 * variables so it costs no React re-renders. Hidden for touch and reduced motion.
 */
export function Spotlight({
  className,
  color = "rgb(31 79 255 / 0.12)",
  size = 520,
}: {
  className?: string;
  color?: string;
  size?: number;
}) {
  const ref = React.useRef<HTMLDivElement>(null);

  React.useEffect(() => {
    const el = ref.current;
    const parent = el?.parentElement;
    if (!el || !parent) return;
    if (window.matchMedia("(prefers-reduced-motion: reduce), (pointer: coarse)").matches) return;

    let frame = 0;
    const onMove = (e: PointerEvent) => {
      cancelAnimationFrame(frame);
      frame = requestAnimationFrame(() => {
        const rect = parent.getBoundingClientRect();
        el.style.setProperty("--x", `${e.clientX - rect.left}px`);
        el.style.setProperty("--y", `${e.clientY - rect.top}px`);
        el.style.opacity = "1";
      });
    };
    const onLeave = () => {
      el.style.opacity = "0";
    };
    parent.addEventListener("pointermove", onMove);
    parent.addEventListener("pointerleave", onLeave);
    return () => {
      cancelAnimationFrame(frame);
      parent.removeEventListener("pointermove", onMove);
      parent.removeEventListener("pointerleave", onLeave);
    };
  }, []);

  return (
    <div
      ref={ref}
      aria-hidden="true"
      className={cn(
        "pointer-events-none absolute inset-0 opacity-0 transition-opacity duration-500",
        className,
      )}
      style={{
        background: `radial-gradient(${size}px circle at var(--x, 50%) var(--y, 30%), ${color}, transparent 65%)`,
      }}
    />
  );
}
