"use client";

import { useEffect, useState } from "react";
import { Sparkles } from "lucide-react";

const agents = [
  { name: "Orchestrator Agent", emoji: "👑", desc: "Coordinates all agents", delay: 0 },
  { name: "Flight Agent", emoji: "✈️", desc: "Finds and books flights", delay: 0.1 },
  { name: "Weather Agent", emoji: "🌤️", desc: "Checks global weather", delay: 0.2 },
  { name: "Code Agent", emoji: "💻", desc: "Writes & executes code", delay: 0.3 },
  { name: "Writer Agent", emoji: "📝", desc: "Creates content", delay: 0.4 },
  { name: "Planner Agent", emoji: "📋", desc: "Breaks down tasks", delay: 0.5 },
];

export function HeroSection() {
  const [isVisible, setIsVisible] = useState(false);

  useEffect(() => {
    setIsVisible(true);
  }, []);

  return (
    <section className="relative min-h-screen flex items-center justify-center overflow-hidden py-20">
      {/* Background gradient */}
      <div className="absolute inset-0 bg-gradient-to-br from-blue-50 to-indigo-50 dark:from-slate-900 dark:to-slate-800" />
      
      {/* Gradient blur elements */}
      <div className="absolute top-20 left-10 w-80 h-80 bg-blue-300 dark:bg-blue-600 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-pulse" />
      <div className="absolute -bottom-40 right-10 w-80 h-80 bg-purple-300 dark:bg-purple-600 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-pulse" />

      <div className="relative container max-w-7xl px-4">
        <div className="grid lg:grid-cols-2 gap-12 items-center">
          {/* Left Content */}
          <div className={`space-y-8 transition-all duration-1000 ${isVisible ? "opacity-100 translate-y-0" : "opacity-0 translate-y-10"}`}>
            <div className="space-y-4">
              <div className="inline-flex items-center gap-2 px-4 py-2 bg-blue-100 dark:bg-blue-900/30 rounded-full border border-blue-200 dark:border-blue-800">
                <Sparkles className="h-4 w-4 text-blue-600 dark:text-blue-400" />
                <span className="text-sm font-semibold text-blue-600 dark:text-blue-400">Multi-Agent Intelligence</span>
              </div>

              <h1 className="text-5xl md:text-6xl font-bold tracking-tight bg-gradient-to-r from-blue-600 via-purple-600 to-pink-600 bg-clip-text text-transparent leading-tight">
                Orchestrate Intelligent AI Agents That Work Together
              </h1>

              <p className="text-xl text-slate-600 dark:text-slate-300 max-w-xl leading-relaxed">
                Build, manage, and deploy autonomous AI agents that collaborate to solve complex tasks. Our platform enables seamless coordination between specialized agents.
              </p>
            </div>

            {/* Feature Badges */}
            <div className="grid grid-cols-2 gap-3 pt-4">
              {["Real-time Collaboration", "API Integrations", "Multi-Agent Workflows", "Live Analytics"].map((feature) => (
                <div
                  key={feature}
                  className="px-4 py-2 bg-white/50 dark:bg-slate-800/50 backdrop-blur border border-white/20 dark:border-slate-700/50 rounded-lg text-sm font-medium text-slate-700 dark:text-slate-300 hover:bg-white/70 dark:hover:bg-slate-800/70 transition-colors"
                >
                  ✨ {feature}
                </div>
              ))}
            </div>

            {/* CTA Buttons */}
            <div className="flex flex-col sm:flex-row gap-4 pt-4">
              <a href="/playground" className="inline-flex items-center justify-center px-8 py-3 bg-gradient-to-r from-blue-600 to-purple-600 text-white font-semibold rounded-lg hover:shadow-lg hover:shadow-blue-500/50 transition-all duration-200 hover:scale-105">
                Try Playground →
              </a>
              <a href="/agents" className="inline-flex items-center justify-center px-8 py-3 bg-white/10 dark:bg-slate-800/50 border border-white/20 dark:border-slate-700 text-slate-900 dark:text-white font-semibold rounded-lg hover:bg-white/20 dark:hover:bg-slate-800 transition-all duration-200">
                Explore Agents
              </a>
            </div>
          </div>

          {/* Right Side - Agent Network Animation */}
          <div className={`relative h-96 transition-all duration-1000 delay-300 ${isVisible ? "opacity-100" : "opacity-0"}`}>
            <div className="absolute inset-0 bg-gradient-to-br from-blue-400/20 to-purple-400/20 dark:from-blue-600/10 dark:to-purple-600/10 rounded-3xl backdrop-blur-xl border border-white/10 dark:border-slate-700/50" />

            {/* Animated Agent Grid */}
            <div className="relative w-full h-full flex items-center justify-center">
              <div className="grid grid-cols-3 gap-4 p-8">
                {agents.map((agent, idx) => (
                  <div
                    key={idx}
                    className="group relative"
                    style={{
                      animation: `float ${3 + idx * 0.5}s ease-in-out infinite`,
                      animationDelay: `${agent.delay}s`,
                    }}
                  >
                    <div className="absolute inset-0 bg-gradient-to-br from-blue-500 to-purple-500 rounded-xl opacity-0 group-hover:opacity-100 blur transition-all duration-300 group-hover:blur-md" />
                    <div className="relative bg-white dark:bg-slate-800 rounded-xl p-4 text-center border border-slate-200 dark:border-slate-700 hover:border-blue-400 dark:hover:border-purple-500 transition-all duration-300 group-hover:scale-110 group-hover:shadow-xl">
                      <div className="text-3xl mb-2">{agent.emoji}</div>
                      <div className="text-xs font-semibold text-slate-900 dark:text-white line-clamp-1">{agent.name.split(" ")[0]}</div>
                      <div className="text-xs text-slate-500 dark:text-slate-400 mt-1">{agent.desc.split(" ").slice(0, 2).join(" ")}</div>
                      <div className="absolute top-2 right-2 w-2 h-2 bg-green-500 rounded-full animate-pulse" />
                    </div>
                  </div>
                ))}
              </div>
            </div>

            <style>{`
              @keyframes float {
                0%, 100% { transform: translateY(0px); }
                50% { transform: translateY(-20px); }
              }
            `}</style>
          </div>
        </div>
      </div>
    </section>
  );
}
