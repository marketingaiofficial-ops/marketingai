"use client";

import * as Accordion from "@radix-ui/react-accordion";
import { Plus } from "lucide-react";

import { faqs } from "@/lib/content";

export function FaqList() {
  return (
    <Accordion.Root type="single" collapsible className="divide-y divide-line border-y border-line">
      {faqs.map((f, i) => (
        <Accordion.Item key={i} value={`q${i}`}>
          <Accordion.Header>
            <Accordion.Trigger className="group flex w-full items-center justify-between gap-6 py-5 text-left text-[1.0625rem] font-medium text-ink hover:text-brand-600">
              {f.q}
              <Plus
                aria-hidden="true"
                className="size-5 shrink-0 text-ink-muted transition-transform duration-300 group-data-[state=open]:rotate-45 group-data-[state=open]:text-brand-600"
              />
            </Accordion.Trigger>
          </Accordion.Header>
          <Accordion.Content className="overflow-hidden data-[state=closed]:hidden">
            <p className="max-w-2xl pb-6 text-ink-muted">{f.a}</p>
          </Accordion.Content>
        </Accordion.Item>
      ))}
    </Accordion.Root>
  );
}
