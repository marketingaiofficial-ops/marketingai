import * as React from "react";
import { Slot } from "@radix-ui/react-slot";
import { cva, type VariantProps } from "class-variance-authority";

import { cn } from "@/lib/utils";

const buttonVariants = cva(
  "group/button relative inline-flex shrink-0 items-center justify-center gap-2 whitespace-nowrap rounded-sm font-medium transition-[background-color,color,box-shadow,transform] duration-200 ease-out disabled:pointer-events-none disabled:opacity-50 active:translate-y-px [&_svg]:size-4 [&_svg]:shrink-0",
  {
    variants: {
      variant: {
        primary:
          "bg-brand-500 text-white shadow-sm hover:bg-brand-600 hover:shadow-glow",
        secondary:
          "bg-white text-ink ring-1 ring-line-strong ring-inset shadow-xs hover:bg-paper hover:ring-ink-muted/40",
        ghost: "text-ink hover:bg-paper-2",
        link: "h-auto px-0 text-brand-600 underline-offset-4 hover:underline",
        /* For navy sections */
        "primary-dark":
          "bg-white text-navy-900 hover:bg-brand-50 hover:shadow-[0_8px_24px_-6px_rgb(142_180_255/0.5)]",
        "secondary-dark":
          "text-white ring-1 ring-navy-700 ring-inset hover:bg-navy-800 hover:ring-brand-400/60",
      },
      size: {
        sm: "h-9 px-3.5 text-sm",
        md: "h-11 px-5 text-[0.9375rem]",
        lg: "h-13 px-6 text-base",
      },
    },
    defaultVariants: { variant: "primary", size: "md" },
  },
);

export interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {
  asChild?: boolean;
}

export const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant, size, asChild = false, ...props }, ref) => {
    const Comp = asChild ? Slot : "button";
    return (
      <Comp
        ref={ref}
        className={cn(buttonVariants({ variant, size }), className)}
        {...props}
      />
    );
  },
);
Button.displayName = "Button";

/** Trailing arrow that nudges on hover. Place inside a Button. */
export function ButtonArrow() {
  return (
    <svg
      viewBox="0 0 16 16"
      fill="none"
      aria-hidden="true"
      className="transition-transform duration-200 ease-out group-hover/button:translate-x-0.5"
    >
      <path
        d="M3 8h9.5M8.5 4l4 4-4 4"
        stroke="currentColor"
        strokeWidth="1.6"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  );
}

export { buttonVariants };
