import { WriterCard } from "@/components/writer-card";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";

export default function PlaygroundPage() {
  return (
    <div className="container max-w-7xl px-4 py-12">
      <div className="space-y-2 mb-8">
        <h1 className="text-3xl font-bold tracking-tight">Playground</h1>
        <p className="text-muted-foreground">
          Test and experiment with individual agents in real-time.
        </p>
      </div>

      <div className="grid gap-8 lg:grid-cols-3">
        <div className="lg:col-span-2">
          <WriterCard />
        </div>

        <div className="space-y-6">
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
