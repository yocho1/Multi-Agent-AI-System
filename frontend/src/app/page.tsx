import { Navbar } from "@/components/navbar";
import { ParticleBackground } from "@/components/particle-background";
import { HeroSection } from "@/components/hero-section";
import { AgentShowcase } from "@/components/agent-showcase";
import { HowItWorks } from "@/components/how-it-works";
import { FeaturesGrid } from "@/components/features-grid";
import { LiveDemoSection } from "@/components/live-demo-section";
import { CTASection } from "@/components/cta-section";
import { Footer } from "@/components/footer";

export default function HomePage() {
  return (
    <div className="min-h-screen bg-white dark:bg-slate-950">
      <ParticleBackground />
      <Navbar />
      <main className="relative z-10">
        <HeroSection />
        <AgentShowcase />
        <HowItWorks />
        <FeaturesGrid />
        <LiveDemoSection />
        <CTASection />
      </main>
      <Footer />
    </div>
  );
}
