export type Verdict = "yes" | "partial" | "no";

export interface RequirementMatch { requirement: string; kind: "must" | "nice"; verdict: Verdict; evidence: string }
export interface Score { score: number; must_met: number; must_total: number; nice_met: number; nice_total: number }
export interface Report { matches: RequirementMatch[]; score: Score; summary: string; suggestions: string[] }

export type AgentEvent =
  | { type: "start" | "end"; agent: string }
  | { type: "text"; agent: string; text: string }
  | { type: "tool"; agent: string; tool: string }
  | { type: "result"; data: Report }
  | { type: "error"; message: string };
