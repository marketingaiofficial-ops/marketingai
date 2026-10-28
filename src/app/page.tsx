import {
  ContactCta,
  Faq,
  Hero,
  Integrations,
  Leaks,
  PipelineSection,
  Process,
  ServicesBento,
} from "@/components/home/sections";
import { SiteFooter } from "@/components/site/footer";
import { SiteHeader } from "@/components/site/header";

export default function HomePage() {
  return (
    <>
      <SiteHeader />
      <main id="main">
        <Hero />
        <Integrations />
        <Leaks />
        <ServicesBento />
        <PipelineSection />
        <Process />
        <Faq />
        <ContactCta />
      </main>
      <SiteFooter />
    </>
  );
}
