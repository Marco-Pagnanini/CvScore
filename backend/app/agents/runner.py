import asyncio
from contextvars import ContextVar

from anthropic import AsyncAnthropic
from mcp import Client

from app.config import settings

# The API sets this queue once; every nested agent inherits it, so sub-agent tokens reach the frontend too.
EVENTS: ContextVar[asyncio.Queue | None] = ContextVar("events", default=None)
MAX_TURNS = 10
TASK_SCHEMA = {"type": "object", "properties": {"task": {"type": "string"}}, "required": ["task"]}
client = AsyncAnthropic()  # reads ANTHROPIC_API_KEY from the env


async def emit(event: dict) -> None:
    if (queue := EVENTS.get()) is not None:
        await queue.put(event)


async def run(name: str, system_prompt: str, allowed_tools: list[str], task: str, sub_agents=None) -> str:
    sub_agents = sub_agents or {}
    async with Client(settings.MCP_URL) as mcp:
        listed = (await mcp.list_tools()).tools
        tools = [{"name": t.name, "description": t.description or "", "input_schema": t.input_schema}
                 for t in listed if t.name in allowed_tools]
        tools += [{"name": n, "description": f"Ask the {n} agent", "input_schema": TASK_SCHEMA}
                  for n in sub_agents if n in allowed_tools]
        messages = [{"role": "user", "content": task}]
        await emit({"type": "start", "agent": name})

        for _ in range(MAX_TURNS):
            async with client.beta.messages.stream(
                model=settings.MODEL,
                max_tokens=16000,
                system=system_prompt,
                tools=tools,
                messages=messages,
                output_config={"effort": "low"},
                betas=["server-side-fallback-2026-07-01"],
                fallbacks="default",
            ) as stream:
                async for text in stream.text_stream:
                    await emit({"type": "text", "agent": name, "text": text})
                response = await stream.get_final_message()

            if response.stop_reason != "tool_use":
                await emit({"type": "end", "agent": name})
                return "".join(b.text for b in response.content if b.type == "text")

            messages.append({"role": "assistant", "content": response.content})
            results = []
            for block in response.content:
                if block.type != "tool_use":
                    continue
                await emit({"type": "tool", "agent": name, "tool": block.name})
                if block.name in sub_agents:
                    text, is_error = await sub_agents[block.name](block.input["task"]), False
                else:
                    r = await mcp.call_tool(block.name, block.input)
                    text = "\n".join(c.text for c in r.content if c.type == "text")
                    is_error = bool(r.is_error)
                results.append({"type": "tool_result", "tool_use_id": block.id,
                                "content": text, "is_error": is_error})
            messages.append({"role": "user", "content": results})

    raise RuntimeError(f"{name}: too many turns")
