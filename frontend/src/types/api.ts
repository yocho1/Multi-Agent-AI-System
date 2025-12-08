export interface Agent {
  id: string;
  name: string;
  role: string;
  capabilities: string[];
  status?: "idle" | "running" | "error";
}

export interface WriterRequest {
  prompt: string;
  temperature?: number;
  max_tokens?: number;
  chain_of_thought?: string;
}

export interface WriterResponse {
  agent_id: string;
  prompt: string;
  status: "completed" | "error";
  result: string;
}

export interface PlannerRequest {
  task: string;
  parameters?: Record<string, any>;
}

export interface PlannerResponse {
  agent_id: string;
  task: string;
  status: "completed" | "error";
  result: string;
}

export interface OrchestratorRequest {
  task: string;
  parameters?: Record<string, any>;
}

export interface OrchestratorResponse {
  agent_id: string;
  task: string;
  status: "completed" | "error";
  result: string;
}

export interface AgentListResponse {
  id: string;
  role: string;
  capabilities: string[];
}
