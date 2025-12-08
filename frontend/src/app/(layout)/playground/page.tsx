"use client";

import { useState } from "react";
import { WriterCard } from "@/components/writer-card";
import { PlannerCard } from "@/components/planner-card";
import { OrchestratorCard } from "@/components/orchestrator-card";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Sparkles, Zap, Brain } from "lucide-react";

type Agent = "writer" | "planner" | "orchestrator";

export default function PlaygroundPage() {
  const [activeAgent, setActiveAgent] = useState<Agent>("writer");

  const agents = [
    {
      id: "writer" as const,
      label: "Writer",
      icon: Sparkles,
      description: "Generate content and creative text",
      color: "text-amber-500",
      bgColor: "bg-amber-50 dark:bg-amber-950",
    },
    {
      id: "planner" as const,
      label: "Planner",
      icon: Brain,
      description: "Break down tasks into actionable steps",
      color: "text-blue-500",
      bgColor: "bg-blue-50 dark:bg-blue-950",
    },
    {
      id: "orchestrator" as const,
      label: "Orchestrator",
      icon: Zap,
      description: "Coordinate multiple agents for complex tasks",
      color: "text-purple-500",
      bgColor: "bg-purple-50 dark:bg-purple-950",
    },
  ];

  return (
    <div className="container max-w-7xl px-4 py-12">
      <div className="space-y-2 mb-8">
        <h1 className="text-3xl font-bold tracking-tight">Playground</h1>
        <p className="text-muted-foreground">
          Test and experiment with individual agents in real-time.
        </p>
      </div>

      {/* Agent Selection Buttons */}
      <div className="mb-8">
        <p className="text-sm font-semibold mb-4">Select Agent</p>
        <div className="flex flex-wrap gap-3">
          {agents.map((agent) => {
            const Icon = agent.icon;
            return (
              <Button
                key={agent.id}
                onClick={() => setActiveAgent(agent.id)}
                variant={activeAgent === agent.id ? "default" : "outline"}
                className={`gap-2 ${
                  activeAgent === agent.id ? agent.bgColor : ""
                }`}
              >
                <Icon className={`h-4 w-4 ${activeAgent === agent.id ? agent.color : ""}`} />
                {agent.label}
              </Button>
            );
          })}
        </div>
      </div>

      <div className="grid gap-8 lg:grid-cols-3">
        <div className="lg:col-span-2">
          {/* Agent Cards */}
          {activeAgent === "writer" && <WriterCard />}
          {activeAgent === "planner" && <PlannerCard />}
          {activeAgent === "orchestrator" && <OrchestratorCard />}
        </div>

        <div className="space-y-6">
          {/* Agent Info Card */}
          <Card>
            <CardHeader>
              <CardTitle className="text-lg">Current Agent</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              {agents.map((agent) => {
                if (activeAgent !== agent.id) return null;
                const Icon = agent.icon;
                return (
                  <div key={agent.id}>
                    <div className="flex items-center gap-2 mb-2">
                      <Icon className={`h-5 w-5 ${agent.color}`} />
                      <h3 className="font-semibold">{agent.label}</h3>
                    </div>
                    <Badge variant="secondary" className="mb-3">
                      {agent.description}
                    </Badge>
                    <p className="text-xs text-muted-foreground">
                      {activeAgent === "writer" &&
                        "Powered by Gemini AI. Generates creative content, code, and text."}
                      {activeAgent === "planner" &&
                        "Breaks complex tasks into manageable steps with dependencies."}
                      {activeAgent === "orchestrator" &&
                        "Coordinates multiple agents to solve complex multi-step tasks."}
                    </p>
                  </div>
                );
              })}
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="text-lg">Tips & Tricks</CardTitle>
            </CardHeader>
            <CardContent className="text-sm space-y-3 text-muted-foreground">
              <div>
                <p className="font-semibold text-foreground mb-1">Temperature</p>
                <p>Lower values (0-0.3) produce focused, deterministic output.</p>
              </div>
              <div>
                <p className="font-semibold text-foreground mb-1">Max Tokens</p>
                <p>Controls response length. 500 = short, 1000+ = detailed.</p>
              </div>
              <div>
                <p className="font-semibold text-foreground mb-1">Chain of Thought</p>
                <p>Provide reasoning context to improve output quality.</p>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="text-lg">Recent Generations</CardTitle>
              <CardDescription>Your last 5 requests</CardDescription>
            </CardHeader>
            <CardContent>
              <p className="text-xs text-muted-foreground">
                History not yet implemented. Coming soon!
              </p>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}
