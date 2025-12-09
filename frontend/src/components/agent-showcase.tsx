"use client";

import { useState } from "react";
import { Zap, Eye, EyeOff } from "lucide-react";

const agents = [
  {
    name: "Orchestrator Agent",
    emoji: "👑",
    description: "Coordinates all agents",
    status: "Online",
    capabilities: ["Task Decomposition", "Agent Coordination", "Result Aggregation"],
  },
  {
    name: "Flight Agent",
    emoji: "✈️",
    description: "Finds and books flights",
    status: "Online",
    capabilities: ["Flight Search", "Booking Management", "Price Comparison"],
  },
  {
    name: "Weather Agent",
    emoji: "🌤️",
    description: "Checks global weather",
    status: "Online",
    capabilities: ["Weather Forecast", "Location Detection", "Real-time Data"],
  },
  {
    name: "Code Agent",
    emoji: "💻",
    description: "Writes & executes code",
    status: "Online",
    capabilities: ["Code Generation", "Execution", "Debugging"],
  },
  {
    name: "Writer Agent",
    emoji: "📝",
    description: "Creates content",
    status: "Online",
    capabilities: ["Content Generation", "Editing", "Formatting"],
  },
  {
    name: "Planner Agent",
    emoji: "📋",
    description: "Breaks down tasks",
    status: "Online",
    capabilities: ["Task Planning", "Step Generation", "Timeline Creation"],
  },
];

export function AgentShowcase() {
  const [hoveredAgent, setHoveredAgent] = useState<number | null>(null);
  const [expandedAgent, setExpandedAgent] = useState<number | null>(null);

  return (
    <section className="py-24 relative overflow-hidden">
      <div className="absolute inset-0 bg-gradient-to-br from-slate-50 to-white dark:from-slate-900 dark:to-slate-950" />

      <div className="relative container max-w-7xl px-4">
        <div className="text-center mb-16">
          <h2 className="text-4xl md:text-5xl font-bold mb-4 bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
            Meet Your AI Team
          </h2>
          <p className="text-lg text-slate-600 dark:text-slate-400 max-w-2xl mx-auto">
            Six specialized agents working together to tackle any challenge
          </p>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {agents.map((agent, idx) => (
            <div
              key={idx}
              className="group relative"
              onMouseEnter={() => setHoveredAgent(idx)}
              onMouseLeave={() => setHoveredAgent(null)}
              onClick={() => setExpandedAgent(expandedAgent === idx ? null : idx)}
            >
              {/* Glow background */}
              <div className={`absolute inset-0 bg-gradient-to-br from-blue-500/20 to-purple-500/20 rounded-2xl opacity-0 group-hover:opacity-100 blur-xl transition-all duration-300 ${hoveredAgent === idx ? "opacity-100" : ""}`} />

              {/* Card */}
              <div className="relative bg-white/70 dark:bg-slate-800/70 backdrop-blur-xl border border-slate-200/50 dark:border-slate-700/50 rounded-2xl p-6 hover:border-blue-400/50 dark:hover:border-purple-500/50 transition-all duration-300 h-full hover:shadow-2xl">
                {/* Header */}
                <div className="flex items-start justify-between mb-4">
                  <div className="flex items-center gap-3">
                    <div className="text-4xl">{agent.emoji}</div>
                    <div>
                      <h3 className="font-bold text-slate-900 dark:text-white">{agent.name}</h3>
                      <p className="text-sm text-slate-600 dark:text-slate-400">{agent.description}</p>
                    </div>
                  </div>
                  <button
                    className="p-2 hover:bg-slate-100 dark:hover:bg-slate-700 rounded-lg transition-colors"
                    onClick={(e) => {
                      e.stopPropagation();
                      setExpandedAgent(expandedAgent === idx ? null : idx);
                    }}
                  >
                    {expandedAgent === idx ? (
                      <EyeOff className="h-4 w-4 text-slate-600 dark:text-slate-400" />
                    ) : (
                      <Eye className="h-4 w-4 text-slate-600 dark:text-slate-400" />
                    )}
                  </button>
                </div>

                {/* Status */}
                <div className="flex items-center gap-2 mb-4">
                  <div className="h-2 w-2 bg-green-500 rounded-full animate-pulse" />
                  <span className="text-sm font-medium text-green-600 dark:text-green-400">{agent.status}</span>
                </div>

                {/* Capabilities */}
                <div className="space-y-2">
                  <p className="text-xs font-semibold text-slate-700 dark:text-slate-300 uppercase tracking-wide">Capabilities</p>
                  <div className="flex flex-wrap gap-2">
                    {agent.capabilities.slice(0, 2).map((cap, idx) => (
                      <span
                        key={idx}
                        className="inline-flex items-center gap-1 px-2 py-1 bg-blue-100 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300 text-xs font-medium rounded-full"
                      >
                        <Zap className="h-3 w-3" />
                        {cap}
                      </span>
                    ))}
                  </div>
                </div>

                {/* Expanded view */}
                {expandedAgent === idx && (
                  <div className="mt-4 pt-4 border-t border-slate-200 dark:border-slate-700">
                    <p className="text-sm text-slate-600 dark:text-slate-400 mb-3">All Capabilities:</p>
                    <div className="flex flex-wrap gap-2">
                      {agent.capabilities.map((cap, idx) => (
                        <span
                          key={idx}
                          className="inline-flex items-center gap-1 px-3 py-1 bg-purple-100 dark:bg-purple-900/30 text-purple-700 dark:text-purple-300 text-xs font-medium rounded-full"
                        >
                          ✓ {cap}
                        </span>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
