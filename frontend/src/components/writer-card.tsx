"use client";

import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { z } from "zod";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { useWriterAgent } from "@/hooks/use-agents";
import { toast } from "sonner";
import { Loader2, Sparkles } from "lucide-react";

const writerSchema = z.object({
  prompt: z.string().min(10, "Prompt must be at least 10 characters"),
  temperature: z.number().min(0).max(1).default(0.7),
  maxTokens: z.number().min(100).max(4000).default(1000),
  chainOfThought: z.string().optional(),
});

type WriterFormData = z.infer<typeof writerSchema>;

export function WriterCard() {
  const { mutate: generateContent, isPending, data: result } = useWriterAgent();
  const { register, handleSubmit, watch, control, formState: { errors } } = useForm<WriterFormData>({
    resolver: zodResolver(writerSchema),
    defaultValues: { temperature: 0.7, maxTokens: 1000 },
  });

  const temperature = watch("temperature");

  const onSubmit = (formData: WriterFormData) => {
    generateContent(
      {
        prompt: formData.prompt,
        temperature: formData.temperature,
        max_tokens: formData.maxTokens,
        chain_of_thought: formData.chainOfThought,
      },
      {
        onSuccess: () => {
          toast.success("Content generated successfully!");
        },
        onError: (error) => {
          toast.error("Failed to generate content: " + (error as Error).message);
        },
      }
    );
  };

  return (
    <Card className="w-full">
      <CardHeader>
        <div className="flex items-center gap-2">
          <Sparkles className="h-5 w-5 text-amber-500" />
          <div>
            <CardTitle>Content Writer</CardTitle>
            <CardDescription>Generate content using Gemini AI</CardDescription>
          </div>
        </div>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
          <div className="space-y-2">
            <Label htmlFor="prompt">Prompt *</Label>
            <Textarea
              id="prompt"
              placeholder="Write a Python hello world program..."
              className="min-h-24"
              {...register("prompt")}
            />
            {errors.prompt && (
              <p className="text-xs text-destructive">{errors.prompt.message}</p>
            )}
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label htmlFor="temperature">Creativity: {temperature.toFixed(1)}</Label>
              <Input
                id="temperature"
                type="range"
                min="0"
                max="1"
                step="0.1"
                {...register("temperature", { valueAsNumber: true })}
              />
              <p className="text-xs text-muted-foreground">
                {temperature < 0.4
                  ? "Deterministic"
                  : temperature < 0.7
                  ? "Balanced"
                  : "Creative"}
              </p>
            </div>

            <div className="space-y-2">
              <Label htmlFor="maxTokens">Max Tokens</Label>
              <Input
                id="maxTokens"
                type="number"
                min="100"
                max="4000"
                step="100"
                {...register("maxTokens", { valueAsNumber: true })}
              />
            </div>
          </div>

          <div className="space-y-2">
            <Label htmlFor="chainOfThought">Chain of Thought (Optional)</Label>
            <Input
              id="chainOfThought"
              placeholder="Reasoning prefix..."
              {...register("chainOfThought")}
            />
          </div>

          <Button type="submit" disabled={isPending} className="w-full">
            {isPending ? (
              <>
                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                Generating...
              </>
            ) : (
              <>
                <Sparkles className="mr-2 h-4 w-4" />
                Generate Content
              </>
            )}
          </Button>

          {result && (
            <div className="mt-6 space-y-2 rounded-lg bg-muted p-4">
              <p className="text-sm font-semibold">Generated Content:</p>
              <p className="whitespace-pre-wrap text-sm">{result.result}</p>
            </div>
          )}
        </form>
      </CardContent>
    </Card>
  );
}
