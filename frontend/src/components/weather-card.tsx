"use client";

import { useMemo, useState } from "react";
import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";
import { Input } from "@/components/ui/input";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { useExecuteAgent } from "@/hooks/use-agents";
import { toast } from "sonner";
import { Cloud, Loader2, Eye, EyeOff } from "lucide-react";

export function WeatherCard() {
  const [location, setLocation] = useState("");
  const [showDetails, setShowDetails] = useState(false);
  const { mutate: executeWeather, isPending, data: result } = useExecuteAgent();

  const forecast = useMemo(() => {
    if (!result) return null;
    const res = (result as any)?.result || result;
    return res;
  }, [result]);

  const daily = useMemo(() => {
    if (!forecast) return [] as any[];
    const days = forecast.daily || [];
    if (Array.isArray(days)) return days;
    return [] as any[];
  }, [forecast]);

  const onSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!location.trim()) {
      toast.error("Please enter a location");
      return;
    }

    executeWeather(
      {
        agentId: "weather",
        task: location,
        parameters: { location },
      },
      {
        onSuccess: () => toast.success("Weather fetched successfully"),
        onError: (err) => toast.error("Failed to fetch weather: " + (err as Error).message),
      }
    );
  };

  return (
    <Card className="w-full">
      <CardHeader>
        <div className="flex items-center gap-2">
          <Cloud className="h-5 w-5 text-sky-500" />
          <div>
            <CardTitle>Weather</CardTitle>
            <CardDescription>Get real 3-day forecast with current conditions</CardDescription>
          </div>
        </div>
      </CardHeader>
      <CardContent>
        <form onSubmit={onSubmit} className="space-y-6">
          <div className="space-y-2">
            <Label htmlFor="location">Location *</Label>
            <Input
              id="location"
              placeholder="e.g., Vienna, Austria"
              value={location}
              onChange={(e) => setLocation(e.target.value)}
            />
          </div>

          <Button type="submit" disabled={isPending} className="w-full">
            {isPending ? (
              <>
                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                Fetching...
              </>
            ) : (
              <>
                <Cloud className="mr-2 h-4 w-4" />
                Get Weather
              </>
            )}
          </Button>

          {forecast && (
            <div className="mt-6 space-y-3 rounded-lg bg-muted p-4">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-semibold">Current Conditions</p>
                  <p className="text-xs text-muted-foreground">{forecast.location || location}</p>
                </div>
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

              <div className="grid grid-cols-3 gap-3 text-sm">
                <div>
                  <p className="text-xs text-muted-foreground">Temp (°C)</p>
                  <p className="font-semibold">{forecast.temperature_c ?? "-"}</p>
                </div>
                <div>
                  <p className="text-xs text-muted-foreground">Precip (mm)</p>
                  <p className="font-semibold">{forecast.precipitation_mm ?? "-"}</p>
                </div>
                <div>
                  <p className="text-xs text-muted-foreground">Wind (km/h)</p>
                  <p className="font-semibold">{forecast.wind_speed_kmh ?? "-"}</p>
                </div>
              </div>

              {daily.length > 0 && (
                <div className="space-y-2">
                  <p className="text-xs font-semibold text-muted-foreground">3-day forecast</p>
                  <div className="space-y-2">
                    {daily.map((day, idx) => (
                      <div key={idx} className="rounded-md bg-background border p-3 text-xs">
                        <div className="flex items-center justify-between">
                          <span className="font-semibold">{day.date}</span>
                          <span>
                            {day.temp_min_c ?? "-"} / {day.temp_max_c ?? "-"} °C
                          </span>
                        </div>
                        <p className="text-muted-foreground">Precip: {day.precip_mm ?? "-"} mm</p>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {showDetails && (
                <div className="rounded-md bg-background p-3 text-xs text-muted-foreground border">
                  <pre className="whitespace-pre-wrap">{JSON.stringify(forecast, null, 2)}</pre>
                </div>
              )}
            </div>
          )}
        </form>
      </CardContent>
    </Card>
  );
}
