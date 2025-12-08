"use client";

import { useAgentsList } from "@/hooks/use-agents";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Loader2 } from "lucide-react";

export function AgentsList() {
  const { data: agents, isLoading, error } = useAgentsList();

  if (isLoading) {
    return (
      <Card>
        <CardContent className="flex items-center justify-center p-8">
          <Loader2 className="h-5 w-5 animate-spin text-muted-foreground" />
        </CardContent>
      </Card>
    );
  }

  if (error) {
    return (
      <Card className="border-destructive">
        <CardContent className="p-6 text-destructive">
          Failed to load agents: {(error as Error).message}
        </CardContent>
      </Card>
    );
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>Available Agents</CardTitle>
        <CardDescription>Multi-Agent System Status</CardDescription>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          {agents?.map((agent) => (
            <div key={agent.id} className="rounded-lg border p-4 space-y-2">
              <div className="flex items-center justify-between">
                <h3 className="font-semibold capitalize">{agent.id}</h3>
                <Badge variant="outline">{agent.role}</Badge>
              </div>
              <div className="flex flex-wrap gap-1">
                {agent.capabilities?.map((cap) => (
                  <Badge key={cap} variant="secondary" className="text-xs">
                    {cap}
                  </Badge>
                ))}
              </div>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
}
