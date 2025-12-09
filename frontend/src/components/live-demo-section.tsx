"use client";

import { useEffect, useState } from "react";
import { Code, Copy, Check } from "lucide-react";

export function LiveDemoSection() {
  const [copied, setCopied] = useState(false);

  const demoCode = `# Example: Plan a trip
Task: "Plan weekend trip to Tokyo"

Agents working in parallel:
✈️ Flight Agent      → Find cheapest flights
🌤️ Weather Agent    → Check forecast  
📝 Writer Agent     → Create itinerary
📋 Planner Agent    → Schedule activities

Result: Complete trip plan with all details 🎉`;

  const handleCopy = () => {
    navigator.clipboard.writeText(demoCode);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <section className="py-24 relative overflow-hidden">
      <div className="absolute inset-0 bg-gradient-to-br from-white to-slate-50 dark:from-slate-950 dark:to-slate-900" />

      <div className="relative container max-w-7xl px-4">
        <div className="text-center mb-16">
          <h2 className="text-4xl md:text-5xl font-bold mb-4 bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
            See It In Action
          </h2>
          <p className="text-lg text-slate-600 dark:text-slate-400 max-w-2xl mx-auto">
            Watch how agents work together to accomplish complex tasks
          </p>
        </div>

        <div className="grid lg:grid-cols-2 gap-8 items-center">
          {/* Demo Code */}
          <div className="relative group">
            {/* Glow */}
            <div className="absolute inset-0 bg-gradient-to-br from-blue-500/20 to-purple-500/20 rounded-2xl opacity-0 group-hover:opacity-100 blur-xl transition-all duration-300" />

            {/* Code Block */}
            <div className="relative bg-slate-900 dark:bg-slate-950 rounded-2xl border border-slate-700/50 overflow-hidden">
              {/* Header */}
              <div className="flex items-center justify-between px-6 py-4 bg-slate-800/50 border-b border-slate-700/50">
                <div className="flex items-center gap-2">
                  <Code className="h-5 w-5 text-slate-400" />
                  <span className="text-sm font-mono text-slate-400">example.py</span>
                </div>
                <button
                  onClick={handleCopy}
                  className="inline-flex items-center gap-2 px-3 py-1 bg-slate-700/50 hover:bg-slate-600/50 rounded text-sm text-slate-300 transition-colors"
                >
                  {copied ? (
                    <>
                      <Check className="h-4 w-4 text-green-500" />
                      Copied!
                    </>
                  ) : (
                    <>
                      <Copy className="h-4 w-4" />
                      Copy
                    </>
                  )}
                </button>
              </div>

              {/* Code Content */}
              <pre className="p-6 text-sm font-mono text-slate-300 overflow-x-auto">
                <code>{demoCode}</code>
              </pre>
            </div>
          </div>

          {/* Features List */}
          <div className="space-y-6">
            <div className="bg-white/70 dark:bg-slate-800/70 backdrop-blur-xl border border-slate-200/50 dark:border-slate-700/50 rounded-xl p-6 hover:border-blue-400/50 transition-all duration-300">
              <h3 className="text-xl font-bold text-slate-900 dark:text-white mb-2 flex items-center gap-2">
                <span className="text-2xl">⚡</span> Fast Execution
              </h3>
              <p className="text-slate-600 dark:text-slate-400">
                Agents execute tasks in parallel, dramatically reducing completion time
              </p>
            </div>

            <div className="bg-white/70 dark:bg-slate-800/70 backdrop-blur-xl border border-slate-200/50 dark:border-slate-700/50 rounded-xl p-6 hover:border-purple-400/50 transition-all duration-300">
              <h3 className="text-xl font-bold text-slate-900 dark:text-white mb-2 flex items-center gap-2">
                <span className="text-2xl">🔄</span> Smart Coordination
              </h3>
              <p className="text-slate-600 dark:text-slate-400">
                Orchestrator intelligently breaks down tasks and coordinates results
              </p>
            </div>

            <div className="bg-white/70 dark:bg-slate-800/70 backdrop-blur-xl border border-slate-200/50 dark:border-slate-700/50 rounded-xl p-6 hover:border-emerald-400/50 transition-all duration-300">
              <h3 className="text-xl font-bold text-slate-900 dark:text-white mb-2 flex items-center gap-2">
                <span className="text-2xl">📊</span> Detailed Insights
              </h3>
              <p className="text-slate-600 dark:text-slate-400">
                Track agent performance and get detailed metrics for every execution
              </p>
            </div>

            <a href="/playground" className="inline-flex items-center justify-center w-full px-6 py-3 bg-gradient-to-r from-blue-600 to-purple-600 text-white font-semibold rounded-lg hover:shadow-lg hover:shadow-blue-500/50 transition-all duration-200 hover:scale-105 mt-4">
              Try It Now →
            </a>
          </div>
        </div>
      </div>
    </section>
  );
}
