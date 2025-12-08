"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { useExecuteAgent } from "@/hooks/use-agents";
import { toast } from "sonner";
import { Loader2, Zap } from "lucide-react";

export function OrchestratorCard() {
  const [task, setTask] = useState("");
  const { mutate: executeOrchestrator, isPending, data: result } = useExecuteAgent();

  const onSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!task.trim()) {
      toast.error("Please enter a task");
      return;
    }

    executeOrchestrator(
      {
        agentId: "orchestrator",
        task,
        parameters: {},
      },
      {
        onSuccess: () => {
          toast.success("Task executed successfully!");
        },
        onError: (error) => {
          toast.error("Failed to execute task: " + (error as Error).message);
        },
      }
    );
  };

  return (
    <Card className="w-full">
      <CardHeader>
        <div className="flex items-center gap-2">
          <Zap className="h-5 w-5 text-purple-500" />
          <div>
            <CardTitle>Orchestrator</CardTitle>
            <CardDescription>Coordinate multiple agents for complex tasks</CardDescription>
          </div>
        </div>
      </CardHeader>
      <CardContent>
        <form onSubmit={onSubmit} className="space-y-6">
          <div className="space-y-2">
            <Label htmlFor="task">Complex Task *</Label>
            <Textarea
              id="task"
              placeholder="Describe a complex task that requires multiple agents to solve..."
              className="min-h-24"
              value={task}
              onChange={(e) => setTask(e.target.value)}
            />
          </div>

          <div className="rounded-lg bg-muted p-3">
            <p className="text-xs text-muted-foreground">
              <span className="font-semibold">How it works:</span> The Orchestrator will analyze
              your task, coordinate the Planner and Writer agents, and synthesize their outputs
              into a comprehensive solution.
            </p>
          </div>

          <Button type="submit" disabled={isPending} className="w-full">
            {isPending ? (
              <>
                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                Executing...
              </>
            ) : (
              <>
                <Zap className="mr-2 h-4 w-4" />
                Execute Task
              </>
            )}
          </Button>

          {result && (
            <div className="mt-6 space-y-2 rounded-lg bg-muted p-4">
              <p className="text-sm font-semibold">Orchestration Result:</p>
              <div className="whitespace-pre-wrap text-sm">
                {typeof result === "string" ? result : JSON.stringify(result, null, 2)}
              </div>
            </div>
          )}
        </form>
      </CardContent>
    </Card>
  );
}
