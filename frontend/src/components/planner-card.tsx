"use client";

import { useMemo, useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { useExecuteAgent } from "@/hooks/use-agents";
import { toast } from "sonner";
import { Loader2, Brain, Eye, EyeOff } from "lucide-react";

export function PlannerCard() {
  const [task, setTask] = useState("");
  const [showDetails, setShowDetails] = useState(false);
  const { mutate: executePlanner, isPending, data: result } = useExecuteAgent();

  const parsedSteps = useMemo(() => {
    if (!result) return [] as string[];
    const steps = (result as any)?.result?.steps || (result as any)?.steps || [];
    if (Array.isArray(steps)) return steps;
    return [] as string[];
  }, [result]);

  const planDetails = useMemo(() => {
    if (!result) return "";
    return (result as any)?.result?.plan_details || (result as any)?.plan_details || "";
  }, [result]);

  const onSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!task.trim()) {
      toast.error("Please enter a task");
      return;
    }

    executePlanner(
      {
        agentId: "planner",
        task,
        parameters: {},
      },
      {
        onSuccess: () => {
          toast.success("Plan generated successfully!");
        },
        onError: (error) => {
          toast.error("Failed to generate plan: " + (error as Error).message);
        },
      }
    );
  };

  return (
    <Card className="w-full">
      <CardHeader>
        <div className="flex items-center gap-2">
          <Brain className="h-5 w-5 text-blue-500" />
          <div>
            <CardTitle>Task Planner</CardTitle>
            <CardDescription>Break down tasks into actionable steps</CardDescription>
          </div>
        </div>
      </CardHeader>
      <CardContent>
        <form onSubmit={onSubmit} className="space-y-6">
          <div className="space-y-2">
            <Label htmlFor="task">Task *</Label>
            <Textarea
              id="task"
              placeholder="Describe a complex task you want to break down into steps..."
              className="min-h-24"
              value={task}
              onChange={(e) => setTask(e.target.value)}
            />
          </div>

          <Button type="submit" disabled={isPending} className="w-full">
            {isPending ? (
              <>
                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                Planning...
              </>
            ) : (
              <>
                <Brain className="mr-2 h-4 w-4" />
                Generate Plan
              </>
            )}
          </Button>

          {result && (
            <div className="mt-6 space-y-3 rounded-lg bg-muted p-4">
              <div className="flex items-center justify-between">
                <p className="text-sm font-semibold">Generated Plan</p>
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

              {parsedSteps.length > 0 ? (
                <ul className="list-disc pl-5 space-y-1 text-sm">
                  {parsedSteps.map((step, idx) => (
                    <li key={idx}>{step}</li>
                  ))}
                </ul>
              ) : (
                <p className="text-sm text-muted-foreground">No steps returned.</p>
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
