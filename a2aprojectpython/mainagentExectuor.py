from typing_extensions import override

from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from a2a.utils import new_agent_text_message


class HelloWorlAgent:
    """Hello world Agent"""
    
    async def invoke(self)->str:
        return "Hello welcome to the beautiful world"


class HelloWorldAgentExecutor(AgentExecutor):
    """Test AgentProxy implementation"""
    
    def __init__(self):
        self.agent=HelloWorlAgent()
    
    @override
    async def execute(
        self,
        context: RequestContext,
        event_queue: EventQueue,
    ) -> None:
        result = await self.agent.invoke()
        event_queue.enqueue_event(new_agent_text_message(result))

    @override
    async def cancel(
        self, context: RequestContext, event_queue: EventQueue
    ) -> None:
        raise Exception('cancel not supported')