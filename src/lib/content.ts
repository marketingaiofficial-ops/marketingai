/*
 * Site content for the prototype. Copy describes capabilities only: no clients,
 * testimonials, statistics, awards, certifications or guarantees. Anything that
 * needs the owner's input is marked TODO(content).
 */

export const site = {
  name: "Your Marketing AI",
  url: "https://yourmarketingai.com",
  description:
    "GoHighLevel implementation, CRM pipelines, workflow automation and AI agents that capture, qualify and follow up with every lead.",
  bookingHref: "/#contact", // TODO(content): replace with the GHL calendar link
  diagnosticHref: "/#diagnostic", // TODO(content): point at the lead-leak diagnostic
};

export type ServiceGroup = "Capture" | "Convert" | "Automate";

export type Service = {
  slug: string;
  title: string;
  short: string;
  description: string;
  group: ServiceGroup;
  icon: "settings" | "kanban" | "workflow" | "bot" | "magnet" | "layout";
  deliverables: string[];
};

export const services: Service[] = [
  {
    slug: "gohighlevel-setup",
    title: "GoHighLevel setup",
    short: "Implementation, migration and clean-up",
    description:
      "We configure GoHighLevel around how your business actually sells: sub-accounts, users, phone and email, calendars, custom fields and the integrations you rely on.",
    group: "Automate",
    icon: "settings",
    deliverables: ["Account architecture", "Data migration plan", "Team training session"],
  },
  {
    slug: "crm-pipelines",
    title: "CRM & sales pipelines",
    short: "Every deal stage visible",
    description:
      "Pipelines, stages and ownership rules that match your sales process, so your team always knows which leads need attention next.",
    group: "Convert",
    icon: "kanban",
    deliverables: ["Pipeline design", "Lead scoring rules", "Reporting dashboard"],
  },
  {
    slug: "workflow-automation",
    title: "Workflow automation",
    short: "Follow-ups that run themselves",
    description:
      "Multi-step workflows for speed-to-lead, reminders, nurture, no-show recovery and review requests across SMS, email and WhatsApp.",
    group: "Automate",
    icon: "workflow",
    deliverables: ["Workflow map", "Message templates", "Test and QA log"],
  },
  {
    slug: "ai-agents",
    title: "AI chat & voice agents",
    short: "Instant replies, qualified handoffs",
    description:
      "AI agents trained on your offers and FAQs that answer enquiries, ask qualifying questions and book calls, handing over to a person whenever it matters.",
    group: "Convert",
    icon: "bot",
    deliverables: ["Agent knowledge base", "Qualification script", "Human handoff rules"],
  },
  {
    slug: "lead-generation",
    title: "Lead generation systems",
    short: "Capture from every channel",
    description:
      "Forms, ad landing pages, missed-call text-back and social inbox capture, all feeding a single pipeline with source tracking.",
    group: "Capture",
    icon: "magnet",
    deliverables: ["Capture points audit", "UTM and source tracking", "Lead routing"],
  },
  {
    slug: "websites-funnels",
    title: "Websites & funnels",
    short: "Pages built to convert",
    description:
      "Fast, focused websites and funnels connected to your CRM from day one, so every visitor who raises a hand lands in the right workflow.",
    group: "Capture",
    icon: "layout",
    deliverables: ["Funnel strategy", "Page build", "CRM-connected forms"],
  },
];

export const serviceGroups: { group: ServiceGroup; blurb: string }[] = [
  { group: "Capture", blurb: "Bring every enquiry into one place" },
  { group: "Convert", blurb: "Reply, qualify and book faster" },
  { group: "Automate", blurb: "Run the busywork in the background" },
];

export const leaks = [
  {
    title: "Slow first replies",
    body: "Enquiries arrive after hours or mid-job, and the first response comes too late to matter.",
    service: "ai-agents",
  },
  {
    title: "No pipeline visibility",
    body: "Leads live in inboxes, spreadsheets and memory, so nobody can see what is stuck.",
    service: "crm-pipelines",
  },
  {
    title: "Manual follow-up",
    body: "Second and third touches depend on someone remembering, so most never happen.",
    service: "workflow-automation",
  },
  {
    title: "Disconnected tools",
    body: "Forms, calendars, ads and messaging don't talk to each other, and data gets retyped.",
    service: "gohighlevel-setup",
  },
];

export const process = [
  {
    step: "01",
    title: "Discovery",
    body: "We map how leads reach you today, where they stall and what your team does by hand.",
    output: "Lead-flow map",
  },
  {
    step: "02",
    title: "Blueprint",
    body: "A written build plan: pipelines, workflows, agents, integrations and the order we ship them.",
    output: "Implementation blueprint",
  },
  {
    step: "03",
    title: "Build",
    body: "We configure GoHighLevel, write the automations and train the AI agents on your material.",
    output: "Working system in a test account",
  },
  {
    step: "04",
    title: "Launch",
    body: "End-to-end testing with real scenarios, then a staged go-live and team handover.",
    output: "QA log and training",
  },
  {
    step: "05",
    title: "Optimise",
    body: "We review what the data shows and refine messages, routing and agent answers.",
    output: "Monthly improvement notes",
  },
];

/* Tools we connect. Shown as "works with", never as partners. TODO(content): confirm list. */
export const integrations = [
  "GoHighLevel",
  "WhatsApp",
  "Google Calendar",
  "Gmail",
  "Stripe",
  "Meta Lead Ads",
  "Zoom",
  "Slack",
  "Zapier",
  "OpenAI",
];

export const faqs = [
  {
    q: "Do I need my own GoHighLevel account?",
    a: "We can work inside your existing account or help you set one up. Either way the account and its data stay yours.",
  },
  {
    q: "How long does a typical build take?",
    a: "It depends on scope. After discovery you get a written blueprint with a timeline for each part before any build work starts.",
  },
  {
    q: "Will the AI agents talk to my customers without oversight?",
    a: "Agents follow the rules we agree with you, and hand conversations to your team for anything outside them. You can review every conversation in the CRM.",
  },
  {
    q: "Can you use WhatsApp?",
    a: "Yes, through the WhatsApp Business Platform. Approval and message template review are handled by Meta, and we guide you through it.",
  },
  {
    q: "What happens after launch?",
    a: "You can run the system yourself with the training we provide, or keep us on for ongoing optimisation and support.",
  },
];
