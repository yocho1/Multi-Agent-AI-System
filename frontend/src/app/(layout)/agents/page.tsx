import { AgentsList } from "@/components/agents-list";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";

export default function AgentsPage() {
  return (
    <div className="container max-w-7xl px-4 py-12">
      <div className="space-y-2 mb-8">
        <h1 className="text-3xl font-bold tracking-tight">Agents</h1>
        <p className="text-muted-foreground">
          Explore and monitor all available agents in the Multi-Agent System.
        </p>
      </div>

      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
        <AgentsList />

        <Card>
          <CardHeader>
            <CardTitle className="text-lg">Agent Capabilities</CardTitle>
            <CardDescription>What each agent can do</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div>
              <p className="font-semibold text-sm">Orchestrator</p>
              <p className="text-xs text-muted-foreground">
                Coordinates multiple agents to solve complex tasks
              </p>
            </div>
            <div>
              <p className="font-semibold text-sm">Planner</p>
              <p className="text-xs text-muted-foreground">
                Breaks down tasks into actionable steps
              </p>
            </div>
            <div>
              <p className="font-semibold text-sm">Writer</p>
              <p className="text-xs text-muted-foreground">
                Generates content, code, and creative text
              </p>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
