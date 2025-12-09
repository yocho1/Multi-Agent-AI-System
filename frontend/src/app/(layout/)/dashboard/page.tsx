import { WriterCard } from "@/components/writer-card";
import { AgentsList } from "@/components/agents-list";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";

export default function DashboardPage() {
  return (
    <div className="container max-w-7xl px-4 py-12">
      {/* Hero Section */}
      <div className="mb-12 space-y-4">
        <div className="space-y-2">
          <h1 className="text-4xl font-bold tracking-tight md:text-5xl">
            Multi-Agent Studio
          </h1>
          <p className="text-lg text-muted-foreground max-w-2xl">
            Orchestrate Planners, Writers, and Tools with AI. Powered by Google Gemini 2.5.
          </p>
        </div>
      </div>

      {/* Stats Grid */}
      <div className="grid gap-4 md:grid-cols-3 mb-12">
        <Card>
          <CardHeader className="pb-3">
            <CardTitle className="text-sm font-medium">Active Agents</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">3</div>
            <p className="text-xs text-muted-foreground">Orchestrator, Planner, Writer</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="pb-3">
            <CardTitle className="text-sm font-medium">API Status</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="flex items-center gap-2">
              <div className="h-3 w-3 rounded-full bg-green-500"></div>
              <span className="text-2xl font-bold">Live</span>
            </div>
            <p className="text-xs text-muted-foreground">localhost:8001</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="pb-3">
            <CardTitle className="text-sm font-medium">LLM Model</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">Gemini</div>
            <p className="text-xs text-muted-foreground">v2.5-flash</p>
          </CardContent>
        </Card>
      </div>

      <div className="grid gap-8 lg:grid-cols-3">
        <div className="lg:col-span-2">
          <WriterCard />
        </div>
        <div>
          <AgentsList />
        </div>
      </div>
    </div>
  );
}
