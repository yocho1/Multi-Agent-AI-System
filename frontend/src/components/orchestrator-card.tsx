"use client";

import { useMemo, useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { useExecuteAgent } from "@/hooks/use-agents";
import { toast } from "sonner";
import { Loader2, Zap, Eye, EyeOff } from "lucide-react";

export function OrchestratorCard() {
  const [task, setTask] = useState("");
  const [showDetails, setShowDetails] = useState(false);
  const { mutate: executeOrchestrator, isPending, data: result } = useExecuteAgent();

  const planSteps = useMemo(() => {
    if (!result) return [] as string[];
    const steps = (result as any)?.result?.plan?.steps || (result as any)?.plan?.steps || [];
    if (Array.isArray(steps)) return steps;
    return [] as string[];
  }, [result]);

  const planDetails = useMemo(() => {
    if (!result) return "";
    return (result as any)?.result?.plan?.plan_details || (result as any)?.plan?.plan_details || "";
  }, [result]);

  const synthesis = useMemo(() => {
    if (!result) return "";
    return (result as any)?.result?.synthesis || (result as any)?.synthesis || "";
  }, [result]);

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
            <div className="mt-6 space-y-3 rounded-lg bg-muted p-4">
              <div className="flex items-center justify-between">
                <p className="text-sm font-semibold">Orchestration Result</p>
                <Button
                  type="button"
                  size="sm"
                  variant="ghost"
                  className="gap-2 px-2"
                  onClick={() => setShowDetails((prev) => !prev)}
                >
                  {showDetails ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                  {showDetails ? "Hide details" : "Show details"}
                </Button>
              </div>

              {synthesis ? (
                <div className="text-sm whitespace-pre-wrap">{synthesis}</div>
              ) : (
                <p className="text-sm text-muted-foreground">No synthesis returned.</p>
              )}

              {planSteps.length > 0 && (
                <div className="space-y-2">
                  <p className="text-xs font-semibold text-muted-foreground">Plan Steps</p>
                  <ul className="list-disc pl-5 space-y-1 text-sm">
                    {planSteps.map((step, idx) => (
                      <li key={idx}>{step}</li>
                    ))}
                  </ul>
                </div>
              )}

              {showDetails && planDetails && (
                <div className="rounded-md bg-background p-3 text-xs text-muted-foreground whitespace-pre-wrap border">
                  {planDetails}
                </div>
              )}
            </div>
          )}
        </form>
      </CardContent>
    </Card>
  );
}
