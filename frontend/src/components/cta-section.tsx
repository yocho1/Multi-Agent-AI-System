"use client";

import { ArrowUpRight } from "lucide-react";
import { useAuth } from "@/contexts/auth-context";

export function CTASection() {
  const { user } = useAuth();

  return (
    <section className="py-24 relative overflow-hidden">
      <div className="absolute inset-0 bg-gradient-to-br from-blue-600 via-purple-600 to-pink-600" />
      <div className="absolute inset-0 opacity-20 bg-grid-pattern" />

      <div className="relative container max-w-4xl px-4 text-center">
        <h2 className="text-4xl md:text-5xl font-bold text-white mb-6 leading-tight">
          {user ? "Start Building Intelligent Workflows" : "Ready to Build Intelligent AI Agents?"}
        </h2>
        <p className="text-xl text-white/90 mb-8 max-w-2xl mx-auto">
          {user 
            ? "Explore our agents and create custom workflows for your needs."
            : "Start experimenting with our multi-agent platform. No complicated setup required."
          }
        </p>

        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          {user ? (
            <>
              <a
                href="/playground"
                className="inline-flex items-center justify-center px-8 py-4 bg-white text-blue-600 font-bold rounded-lg hover:bg-slate-100 transition-all duration-200 hover:scale-105 shadow-xl"
              >
                Launch Playground
                <ArrowUpRight className="ml-2 h-5 w-5" />
              </a>
              <a
                href="/agents"
                className="inline-flex items-center justify-center px-8 py-4 bg-white/20 border-2 border-white text-white font-bold rounded-lg hover:bg-white/30 transition-all duration-200"
              >
                Explore Agents
              </a>
            </>
          ) : (
            <>
              <a
                href="/register"
                className="inline-flex items-center justify-center px-8 py-4 bg-white text-blue-600 font-bold rounded-lg hover:bg-slate-100 transition-all duration-200 hover:scale-105 shadow-xl"
              >
                Create Free Account
                <ArrowUpRight className="ml-2 h-5 w-5" />
              </a>
              <a
                href="/login"
                className="inline-flex items-center justify-center px-8 py-4 bg-white/20 border-2 border-white text-white font-bold rounded-lg hover:bg-white/30 transition-all duration-200"
              >
                Sign In
              </a>
            </>
          )}
        </div>
      </div>

      <style>{`
        .bg-grid-pattern {
          background-image: 
            linear-gradient(0deg, transparent 24%, rgba(255, 255, 255, 0.1) 25%, rgba(255, 255, 255, 0.1) 26%, transparent 27%, transparent 74%, rgba(255, 255, 255, 0.1) 75%, rgba(255, 255, 255, 0.1) 76%, transparent 77%, transparent),
            linear-gradient(90deg, transparent 24%, rgba(255, 255, 255, 0.1) 25%, rgba(255, 255, 255, 0.1) 26%, transparent 27%, transparent 74%, rgba(255, 255, 255, 0.1) 75%, rgba(255, 255, 255, 0.1) 76%, transparent 77%, transparent);
          background-size: 50px 50px;
        }
      `}</style>
    </section>
  );
}
