from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.duckduckgo import DuckDuckGoTools

agent = Agent(
    model=OpenAIChat(id="gpt-4o"),
    description="You are an enthusiastic, loveable dating coach can you suugest some gifts from Amazon, walmart, Target. Also get the link of thosse gifts. Range of the gifts can be anywhere from 0-1000 USD",
    tools=[DuckDuckGoTools()],
    show_tool_calls=True,
    markdown=True
)
agent.print_response("What should I gift my girlfriend", stream=True)

# You are an enthusiastic, loveable dating coach can you suugest some gifts from Amazon, walmart, Target. Also get the link of thosse gifts. Range of the gifts can be anywhere from 0-1000 USD