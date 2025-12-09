"use client";

import { ArrowRight } from "lucide-react";

const steps = [
  {
    number: "01",
    title: "Define Your Task",
    description: "Describe what you want to accomplish in natural language",
    icon: "✍️",
  },
  {
    number: "02",
    title: "Orchestrator Decomposes",
    description: "The orchestrator breaks your task into specialized subtasks",
    icon: "🔄",
  },
  {
    number: "03",
    title: "Agents Execute in Parallel",
    description: "Specialized agents work simultaneously on their tasks",
    icon: "⚡",
  },
  {
    number: "04",
    title: "Results Aggregated",
    description: "All results are combined into a cohesive final output",
    icon: "🎯",
  },
];

export function HowItWorks() {
  return (
    <section className="py-24 relative overflow-hidden">
      <div className="absolute inset-0 bg-gradient-to-br from-white to-blue-50 dark:from-slate-950 dark:to-slate-900" />

      <div className="relative container max-w-7xl px-4">
        <div className="text-center mb-16">
          <h2 className="text-4xl md:text-5xl font-bold mb-4 bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
            How Our Multi-Agent System Works
          </h2>
          <p className="text-lg text-slate-600 dark:text-slate-400 max-w-2xl mx-auto">
            A seamless workflow that brings complex tasks to life
          </p>
        </div>

        {/* Process Flow */}
        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8 mb-12">
          {steps.map((step, idx) => (
            <div key={idx} className="relative group">
              {/* Connection line */}
              {idx < steps.length - 1 && (
                <div className="absolute left-[calc(50%+60px)] top-20 w-[calc(100%+40px)] h-1 bg-gradient-to-r from-blue-400 to-transparent dark:from-blue-600 hidden lg:block" />
              )}

              <div className="relative">
                {/* Number Circle */}
                <div className="w-24 h-24 rounded-full bg-gradient-to-br from-blue-500 to-purple-500 flex items-center justify-center mb-6 group-hover:shadow-lg group-hover:shadow-blue-500/50 transition-all duration-300 mx-auto">
                  <span className="text-3xl font-bold text-white">{step.number}</span>
                </div>

                {/* Content Card */}
                <div className="bg-white/70 dark:bg-slate-800/70 backdrop-blur-xl border border-slate-200/50 dark:border-slate-700/50 rounded-xl p-6 hover:border-blue-400/50 dark:hover:border-purple-500/50 transition-all duration-300">
                  <div className="text-2xl mb-3">{step.icon}</div>
                  <h3 className="text-lg font-bold text-slate-900 dark:text-white mb-2">{step.title}</h3>
                  <p className="text-sm text-slate-600 dark:text-slate-400">{step.description}</p>
                </div>

                {/* Arrow Icon for desktop */}
                {idx < steps.length - 1 && (
                  <div className="absolute -right-5 top-10 hidden lg:flex items-center justify-center">
                    <ArrowRight className="h-6 w-6 text-blue-500" />
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>

        {/* Example Flow */}
        <div className="bg-gradient-to-br from-blue-50 to-purple-50 dark:from-slate-800/50 dark:to-slate-900/50 border border-blue-200/50 dark:border-slate-700/50 rounded-2xl p-8">
          <h3 className="text-xl font-bold text-slate-900 dark:text-white mb-4">Example: Plan a Trip to Tokyo</h3>
          <div className="space-y-3">
            <div className="flex items-start gap-3">
              <div className="h-6 w-6 rounded-full bg-blue-500 flex items-center justify-center text-white text-sm font-bold flex-shrink-0 mt-1">→</div>
              <span className="text-slate-700 dark:text-slate-300"><strong>You:</strong> &ldquo;Plan my weekend trip to Tokyo&rdquo;</span>
            </div>
            <div className="flex items-start gap-3">
              <div className="h-6 w-6 rounded-full bg-purple-500 flex items-center justify-center text-white text-sm font-bold flex-shrink-0 mt-1">→</div>
              <span className="text-slate-700 dark:text-slate-300"><strong>Orchestrator:</strong> Decomposes into find flights, check weather, book accommodation, create itinerary</span>
            </div>
            <div className="flex items-start gap-3">
              <div className="h-6 w-6 rounded-full bg-emerald-500 flex items-center justify-center text-white text-sm font-bold flex-shrink-0 mt-1">→</div>
              <span className="text-slate-700 dark:text-slate-300"><strong>Agents execute:</strong> Flight Agent finds cheapest flights, Weather Agent checks forecast, Planner creates schedule</span>
            </div>
            <div className="flex items-start gap-3">
              <div className="h-6 w-6 rounded-full bg-pink-500 flex items-center justify-center text-white text-sm font-bold flex-shrink-0 mt-1">→</div>
              <span className="text-slate-700 dark:text-slate-300"><strong>Result:</strong> Complete trip itinerary with flights, weather info, and day-by-day schedule 🎉</span>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
