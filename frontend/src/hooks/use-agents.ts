import { useMutation, useQuery } from "@tanstack/react-query";
import { api } from "@/lib/api";
import { WriterRequest, WriterResponse, AgentListResponse } from "@/types/api";

const AGENTS_KEY = ["agents"];
const WRITER_KEY = ["agents", "writer"];

export function useAgentsList() {
  return useQuery({
    queryKey: AGENTS_KEY,
    queryFn: async () => {
      const { data } = await api.get<AgentListResponse[]>("/agents");
      return data;
    },
  });
}

export function useWriterAgent() {
  return useMutation({
    mutationFn: async (request: WriterRequest) => {
      const { data } = await api.post<WriterResponse>("/agents/writer", request, {
        headers: { "X-API-Key": "demo-key-12345" },
      });
      return data;
    },
  });
}

export function useExecuteAgent() {
  return useMutation({
    mutationFn: async ({
      agentId,
      task,
      parameters,
    }: {
      agentId: string;
      task: string;
      parameters?: Record<string, any>;
    }) => {
      const { data } = await api.post("/agents/execute", {
        agent_id: agentId,
        task,
        parameters,
      });
      return data;
    },
  });
}
