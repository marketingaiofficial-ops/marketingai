"use client";

import * as React from "react";

import { Button, ButtonArrow } from "@/components/ui/button";
import { Field, Input, Select, Textarea } from "@/components/ui/form";

/*
 * Prototype form. Not connected yet: Phase 3 wires it to a server action that creates
 * the contact in GoHighLevel with tags and UTM source. Submitting here only shows the
 * success state so the design can be reviewed.
 */
export function ContactForm() {
  const [errors, setErrors] = React.useState<Record<string, string>>({});
  const [sent, setSent] = React.useState(false);

  function onSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    const data = new FormData(e.currentTarget);
    const next: Record<string, string> = {};
    if (!String(data.get("name") ?? "").trim()) next.name = "Please enter your name.";
    const email = String(data.get("email") ?? "");
    if (!/^\S+@\S+\.\S+$/.test(email)) next.email = "Please enter a valid email address.";
    setErrors(next);
    if (Object.keys(next).length === 0) setSent(true);
  }

  if (sent) {
    return (
      <div role="status" className="rounded-lg bg-brand-50 p-8 ring-1 ring-brand-100">
        <p className="text-h3 font-semibold text-ink">Thanks, that looks good.</p>
        <p className="mt-2 text-ink-muted">
          This is a design prototype, so nothing was sent. In the live site this goes straight
          into the CRM and you get a booking link.
        </p>
      </div>
    );
  }

  return (
    <form noValidate onSubmit={onSubmit} className="grid gap-5 sm:grid-cols-2">
      <Field id="name" label="Name" error={errors.name}>
        <Input name="name" autoComplete="name" />
      </Field>
      <Field id="email" label="Work email" error={errors.email}>
        <Input name="email" type="email" autoComplete="email" />
      </Field>
      <Field id="company" label="Company" optional>
        <Input name="company" autoComplete="organization" />
      </Field>
      <Field id="interest" label="Main interest">
        <Select name="interest" defaultValue="">
          <option value="" disabled>
            Choose one
          </option>
          <option>GoHighLevel setup</option>
          <option>CRM & pipelines</option>
          <option>Workflow automation</option>
          <option>AI chat & voice agents</option>
          <option>Lead generation & funnels</option>
          <option>Not sure yet</option>
        </Select>
      </Field>
      <div className="sm:col-span-2">
        <Field id="message" label="Where are leads getting stuck?" optional hint="A sentence or two is plenty.">
          <Textarea name="message" rows={4} />
        </Field>
      </div>
      <div className="flex flex-col gap-3 sm:col-span-2 sm:flex-row sm:items-center sm:justify-between">
        <p className="text-[0.8125rem] text-ink-muted">Takes about a minute. No obligation.</p>
        <Button type="submit" size="lg">
          Send and book a call
          <ButtonArrow />
        </Button>
      </div>
    </form>
  );
}
