"use client";

import { useRouter } from "next/navigation";
import { useAuth } from "@/contexts/auth-context";
import { WriterCard } from "@/components/writer-card";
import { AgentsList } from "@/components/agents-list";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { BarChart3, Zap, Users, Clock, TrendingUp, ActivitySquare, User, Mail, Shield, Sparkles } from "lucide-react";

export default function DashboardPage() {
  const { user } = useAuth();
  const router = useRouter();

  const stats = {
    totalRequests: 42,
    successRate: 98.5,
    avgResponseTime: 2.3,
    agentsActive: 4,
  };

  const userInitials = user?.displayName
    ?.split(" ")
    .map((n) => n[0])
    .join("")
    .toUpperCase() || "U";

  return (
    <div className="container max-w-7xl px-4 py-12">
      {/* Header with User Info */}
      <div className="mb-12 space-y-8">
        <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-6">
          <div className="space-y-2 flex-1">
            <h1 className="text-4xl font-bold tracking-tight md:text-5xl">
              Welcome back, {user?.displayName?.split(" ")[0] || "User"}!
            </h1>
            <p className="text-lg text-muted-foreground max-w-2xl">
              Your AI agent orchestration studio. Powered by Google Gemini 2.5.
            </p>
          </div>
          <div className="flex-shrink-0">
            <div
              onClick={() => router.push("/profile")}
              className="flex items-center gap-4 bg-gradient-to-br from-blue-50 to-purple-50 dark:from-blue-950/30 dark:to-purple-950/30 rounded-lg p-6 border border-blue-200 dark:border-blue-800 cursor-pointer hover:shadow-lg hover:border-blue-300 dark:hover:border-blue-700 transition-all duration-200"
            >
              {user?.photoURL ? (
                <img
                  src={user.photoURL}
                  alt={user.displayName || "User"}
                  className="h-16 w-16 rounded-full object-cover shadow-lg"
                />
              ) : (
                <div className="h-16 w-16 rounded-full bg-gradient-to-br from-blue-500 to-purple-500 flex items-center justify-center text-white font-bold text-xl shadow-lg">
                  {userInitials}
                </div>
              )}
              <div>
                <h3 className="font-semibold text-foreground">{user?.displayName || "User"}</h3>
                <p className="text-sm text-muted-foreground flex items-center gap-1">
                  <Mail className="h-3 w-3" />
                  {user?.email}
                </p>
                <Badge className="mt-2" variant="secondary">
                  <Shield className="h-3 w-3 mr-1" />
                  Verified
                </Badge>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* User Profile Card */}
      <div className="grid gap-6 mb-12 md:grid-cols-2">
        <Card className="md:col-span-1 border-blue-200 dark:border-blue-800">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <User className="h-5 w-5 text-blue-600" />
              Account Information
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div>
              <p className="text-sm font-medium text-muted-foreground">Full Name</p>
              <p className="text-lg font-semibold">{user?.displayName || "Not set"}</p>
            </div>
            <div>
              <p className="text-sm font-medium text-muted-foreground">Email Address</p>
              <p className="text-lg font-semibold">{user?.email}</p>
            </div>
            <div>
              <p className="text-sm font-medium text-muted-foreground">Account Status</p>
              <div className="flex items-center gap-2 mt-1">
                <span className="h-2 w-2 rounded-full bg-green-500 inline-block"></span>
                <span className="text-sm font-medium">Active</span>
              </div>
            </div>
            <div>
              <p className="text-sm font-medium text-muted-foreground">Email Verification</p>
              <Badge className="mt-1" variant="outline">
                ✓ Verified
              </Badge>
            </div>
          </CardContent>
        </Card>

        <Card className="md:col-span-1 border-purple-200 dark:border-purple-800">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <ActivitySquare className="h-5 w-5 text-purple-600" />
              Quick Stats
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div>
              <p className="text-sm font-medium text-muted-foreground">Session Status</p>
              <div className="text-lg font-semibold flex items-center gap-2">
                <span className="h-2 w-2 rounded-full bg-green-500 animate-pulse inline-block"></span>
                Live
              </div>
            </div>
            <div>
              <p className="text-sm font-medium text-muted-foreground">API Access</p>
              <Badge className="mt-1">Premium Access</Badge>
            </div>
            <div>
              <p className="text-sm font-medium text-muted-foreground">Last Activity</p>
              <p className="text-sm text-muted-foreground">Just now</p>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Advanced Stats Grid */}
      <div className="grid gap-4 md:grid-cols-4 mb-12">
        <Card className="border-blue-100 dark:border-blue-900">
          <CardHeader className="pb-3">
            <div className="flex items-center justify-between">
              <CardTitle className="text-sm font-medium">Total Requests</CardTitle>
              <BarChart3 className="h-4 w-4 text-blue-600" />
            </div>
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold">{stats.totalRequests}</div>
            <p className="text-xs text-muted-foreground mt-1 flex items-center gap-1">
              <TrendingUp className="h-3 w-3 text-green-600" />
              +12% from last week
            </p>
          </CardContent>
        </Card>

        <Card className="border-green-100 dark:border-green-900">
          <CardHeader className="pb-3">
            <div className="flex items-center justify-between">
              <CardTitle className="text-sm font-medium">Success Rate</CardTitle>
              <Zap className="h-4 w-4 text-green-600" />
            </div>
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold">{stats.successRate}%</div>
            <div className="mt-2 w-full bg-gray-200 rounded-full h-1.5 dark:bg-gray-700">
              <div
                className="bg-green-600 h-1.5 rounded-full"
                style={{ width: `${stats.successRate}%` }}
              ></div>
            </div>
          </CardContent>
        </Card>

        <Card className="border-purple-100 dark:border-purple-900">
          <CardHeader className="pb-3">
            <div className="flex items-center justify-between">
              <CardTitle className="text-sm font-medium">Avg Response</CardTitle>
              <Clock className="h-4 w-4 text-purple-600" />
            </div>
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold">{stats.avgResponseTime}s</div>
            <p className="text-xs text-muted-foreground mt-1">Per request</p>
          </CardContent>
        </Card>

        <Card className="border-orange-100 dark:border-orange-900">
          <CardHeader className="pb-3">
            <div className="flex items-center justify-between">
              <CardTitle className="text-sm font-medium">Active Agents</CardTitle>
              <Users className="h-4 w-4 text-orange-600" />
            </div>
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold">{stats.agentsActive}</div>
            <p className="text-xs text-muted-foreground mt-1">Ready to use</p>
          </CardContent>
        </Card>
      </div>

      {/* System Status */}
      <div className="grid gap-4 md:grid-cols-3 mb-12">
        <Card>
          <CardHeader className="pb-3">
            <CardTitle className="text-sm font-medium">API Status</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="flex items-center gap-2 mb-2">
              <div className="h-3 w-3 rounded-full bg-green-500 animate-pulse"></div>
              <span className="text-2xl font-bold">Operational</span>
            </div>
            <p className="text-xs text-muted-foreground">localhost:8001 ✓</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="pb-3">
            <CardTitle className="text-sm font-medium">LLM Provider</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">Gemini 2.5</div>
            <p className="text-xs text-muted-foreground">v2.5-flash</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="pb-3">
            <CardTitle className="text-sm font-medium">Data Storage</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">Firestore</div>
            <p className="text-xs text-muted-foreground">Realtime Database</p>
          </CardContent>
        </Card>
      </div>

      {/* Main Content - Agents Section */}
      <div className="mb-12">
        <h2 className="text-2xl font-bold mb-6 flex items-center gap-2">
          <Sparkles className="h-6 w-6 text-amber-500" />
          Available Agents
        </h2>
        <div className="grid gap-8 lg:grid-cols-3">
          <div className="lg:col-span-2">
            <WriterCard />
          </div>
          <div>
            <AgentsList />
          </div>
        </div>
      </div>

      {/* Features Section */}
      <div className="grid gap-6 md:grid-cols-2 mb-12">
        <Card>
          <CardHeader>
            <CardTitle className="text-lg">🚀 Quick Start</CardTitle>
            <CardDescription>Get started with your first agent request</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="space-y-3">
              <div className="flex gap-3">
                <div className="flex-shrink-0 w-6 h-6 rounded-full bg-blue-600 text-white flex items-center justify-center text-sm font-bold">
                  1
                </div>
                <div>
                  <p className="font-medium">Select an Agent</p>
                  <p className="text-sm text-muted-foreground">Writer, Planner, or Orchestrator</p>
                </div>
              </div>
              <div className="flex gap-3">
                <div className="flex-shrink-0 w-6 h-6 rounded-full bg-purple-600 text-white flex items-center justify-center text-sm font-bold">
                  2
                </div>
                <div>
                  <p className="font-medium">Configure Parameters</p>
                  <p className="text-sm text-muted-foreground">Set temperature, tokens, and options</p>
                </div>
              </div>
              <div className="flex gap-3">
                <div className="flex-shrink-0 w-6 h-6 rounded-full bg-green-600 text-white flex items-center justify-center text-sm font-bold">
                  3
                </div>
                <div>
                  <p className="font-medium">Execute & Analyze</p>
                  <p className="text-sm text-muted-foreground">Get instant AI-powered results</p>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="text-lg">💡 Pro Tips</CardTitle>
            <CardDescription>Maximize your agent performance</CardDescription>
          </CardHeader>
          <CardContent className="space-y-3 text-sm">
            <div>
              <p className="font-medium text-foreground mb-1">Temperature Settings</p>
              <p className="text-muted-foreground">Use 0.0-0.3 for precise outputs, 0.7+ for creative results</p>
            </div>
            <div>
              <p className="font-medium text-foreground mb-1">Chain of Thought</p>
              <p className="text-muted-foreground">Provide reasoning context for better AI responses</p>
            </div>
            <div>
              <p className="font-medium text-foreground mb-1">Token Management</p>
              <p className="text-muted-foreground">Balance response length with API costs</p>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Recent Activity */}
      <Card>
        <CardHeader>
          <CardTitle>Recent Activity</CardTitle>
          <CardDescription>Your latest agent executions</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div className="flex items-center justify-between py-3 border-b last:border-0">
              <div>
                <p className="font-medium">Orchestrator Task Execution</p>
                <p className="text-xs text-muted-foreground">12 minutes ago</p>
              </div>
              <Badge variant="outline" className="bg-green-50 text-green-700 border-green-200">
                Success
              </Badge>
            </div>
            <div className="flex items-center justify-between py-3 border-b last:border-0">
              <div>
                <p className="font-medium">Content Generation Request</p>
                <p className="text-xs text-muted-foreground">45 minutes ago</p>
              </div>
              <Badge variant="outline" className="bg-green-50 text-green-700 border-green-200">
                Success
              </Badge>
            </div>
            <div className="flex items-center justify-between py-3 border-b last:border-0">
              <div>
                <p className="font-medium">System Health Check</p>
                <p className="text-xs text-muted-foreground">2 hours ago</p>
              </div>
              <Badge variant="outline" className="bg-blue-50 text-blue-700 border-blue-200">
                Info
              </Badge>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
