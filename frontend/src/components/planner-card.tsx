"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { useExecuteAgent } from "@/hooks/use-agents";
import { toast } from "sonner";
import { Loader2, Brain } from "lucide-react";

export function PlannerCard() {
  const [task, setTask] = useState("");
  const { mutate: executePlanner, isPending, data: result } = useExecuteAgent();

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
            <div className="mt-6 space-y-2 rounded-lg bg-muted p-4">
              <p className="text-sm font-semibold">Generated Plan:</p>
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
