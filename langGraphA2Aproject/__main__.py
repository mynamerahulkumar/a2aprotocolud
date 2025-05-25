import os
import sys

import click
import httpx

from exchangeagent import CurrencyConversionAgent  # type: ignore[import-untyped]
from exchangeagentexector import CurrencyExchangeExecutor  # type: ignore[import-untyped]
from dotenv import load_dotenv

from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore, InMemoryPushNotifier
from a2a.types import AgentCapabilities, AgentCard, AgentSkill
load_dotenv()

@click.command()
@click.option('--host','host',default='localhost')
@click.option('--port','port',default=9000)
def main(host:str,port:int):
    if not os.getenv('GEMINI_API_KEY'):
        print('Gemini API key is missing in env')
        sys.exit(1)
    
    client=httpx.AsyncClient()
    request_handler=DefaultRequestHandler(
        agent_executor=CurrencyConversionAgent(),
        task_store=InMemoryTaskStore(),
        push_notifier=InMemoryPushNotifier(client)
    )
    server=A2AStarletteApplication(
        agent_card=get_agent_card_details(host,port),
        http_handler=request_handler
    )
    
    import uvicorn
    
    uvicorn.run(server.build(),host=host,port=port)


def get_agent_card_details(host:str,port:int):
    """Return the Agent card for the currency exchange Agent"""
    
    capabilites=AgentCapabilities(streaming=True,pushNotification=True)
    
    skill=AgentSkill(
        id='convert_currency',
        name='Currency Exchange Rates tool',
        description='It helps with the exchange values between various currencies',
        tags=['currency conversion','currency exchanges'],
        examples=['What is exchange rate between USD and INR?'],
        
    )
    return AgentCard(
        name='Currency exchange Agent',
        description='Helps with exchange rates for currencies',
        url=f'http://{host}:{port}/',
        version='1.0.1',
        defaultInputModes=CurrencyConversionAgent.SUPPORTED_CONTENT_TYPES,
        defaultOutputModes=CurrencyConversionAgent.SUPPORTED_CONTENT_TYPES,
        capabilites=capabilites,
        skill=[skill]
    )
    
    
if __name__=='__main__':
    main()
    
