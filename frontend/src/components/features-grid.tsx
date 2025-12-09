"use client";

import { BarChart3, Zap, LinkIcon, TrendingUp } from "lucide-react";

const features = [
  {
    icon: Zap,
    title: "Real-time Collaboration",
    description: "Agents communicate instantly and adapt to each other's outputs in real time",
    color: "from-blue-500 to-cyan-500",
  },
  {
    icon: BarChart3,
    title: "Drag & Drop Workflows",
    description: "Visual workflow builder with pre-built templates for common tasks",
    color: "from-purple-500 to-pink-500",
  },
  {
    icon: LinkIcon,
    title: "API Integration",
    description: "Connect external services and create custom tools for your agents",
    color: "from-emerald-500 to-teal-500",
  },
  {
    icon: TrendingUp,
    title: "Monitoring & Analytics",
    description: "Track performance metrics and view execution history for all agents",
    color: "from-orange-500 to-red-500",
  },
];

export function FeaturesGrid() {
  return (
    <section className="py-24 relative overflow-hidden">
      <div className="absolute inset-0 bg-gradient-to-br from-slate-50 to-white dark:from-slate-900 dark:to-slate-950" />

      <div className="relative container max-w-7xl px-4">
        <div className="text-center mb-16">
          <h2 className="text-4xl md:text-5xl font-bold mb-4 bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
            Powerful Features
          </h2>
          <p className="text-lg text-slate-600 dark:text-slate-400 max-w-2xl mx-auto">
            Everything you need to build and deploy intelligent multi-agent systems
          </p>
        </div>

        <div className="grid md:grid-cols-2 gap-8">
          {features.map((feature, idx) => {
            const Icon = feature.icon;
            return (
              <div
                key={idx}
                className="group relative"
              >
                {/* Glow background */}
                <div className={`absolute inset-0 bg-gradient-to-br ${feature.color} rounded-2xl opacity-0 group-hover:opacity-20 blur-xl transition-all duration-300`} />

                {/* Card */}
                <div className="relative bg-white/70 dark:bg-slate-800/70 backdrop-blur-xl border border-slate-200/50 dark:border-slate-700/50 rounded-2xl p-8 hover:border-blue-400/50 dark:hover:border-purple-500/50 transition-all duration-300 h-full">
                  {/* Icon Container */}
                  <div className={`w-14 h-14 rounded-xl bg-gradient-to-br ${feature.color} flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-300`}>
                    <Icon className="h-7 w-7 text-white" />
                  </div>

                  {/* Content */}
                  <h3 className="text-xl font-bold text-slate-900 dark:text-white mb-3">
                    {feature.title}
                  </h3>
                  <p className="text-slate-600 dark:text-slate-400 leading-relaxed">
                    {feature.description}
                  </p>

                  {/* Bottom accent line */}
                  <div className={`absolute bottom-0 left-0 h-1 bg-gradient-to-r ${feature.color} rounded-b-2xl w-0 group-hover:w-full transition-all duration-300`} />
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
}
