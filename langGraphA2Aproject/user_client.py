from a2a.client import A2AClient
from typing import Any
from uuid import uuid4
from a2a.types import (
    SendMessageResponse,
    GetTaskResponse,
    SendMessageSuccessResponse,
    Task,
    TaskState,
    SendMessageRequest,
    MessageSendParams,
    GetTaskRequest,
    TaskQueryParams,
    SendStreamingMessageRequest,
)
import httpx
import traceback

AGENT_URL = 'http://localhost:9000'


def create_send_message_payloadformat(text:str,task_id:str|None=None,context_id:str|None=None,
                        )->dict[str,Any]:
    """Helper function to create the payload for sending the task"""
    
    payload=dict[str,Any]={
        'message':{
            'role':'user',
            'parts':[{'kind':'text','text':text}],
            'messageId':uuid4().hex,
        }
    
    }
    if task_id:
        payload['message']['taskId']=task_id
    if context_id:
        payload['message']['contextId']=context_id
    return payload
    

def print_json_result_response(response:Any,description:str)->None:
    """Helper method to print the JSON representation of a response"""
    
    print(f'{description}')
    
    if hasattr(response,'root'):
        print(f'{response.root.model_dump_json(exclude_none=True)}\n')
    else:
        print(f'{response.model_dump(mode='json',exclude_none=True)}\n')
        
        
async def run_single_turn_message(client:A2AClient)->None:
    """Runs a single turn message non-streaming"""
    
    send_payload=create_send_message_payloadformat(
        text='How much is 1000 USD in INR?'
    )
    request=SendMessageRequest(params=MessageSendParams(**send_payload))
    print(' Single turn message request.....')
    
    #send message
    send_response:SendMessageResponse=await client.send_message(request)
    print_json_result_response(send_response,'Single Turn  Request Response')
    if not isinstance(send_response.root, SendMessageSuccessResponse):
        print('received non-success response. Aborting get task ')
        return

    if not isinstance(send_response.root.result, Task):
        print('received non-task response. Aborting get task ')
        return

    task_id: str = send_response.root.result.id
    print('---Query Task---')
    # query the task
    get_request = GetTaskRequest(params=TaskQueryParams(id=task_id))
    get_response: GetTaskResponse = await client.get_task(get_request)
    print_json_result_response(get_response, 'Query Task Response')

async def run_streaming_message(client:A2AClient)->None:
    """Run a single-turn streaming test..."""
    
    send_payload=create_send_message_payloadformat(
        text="How much is 1000 JPY in CAD? "
    )
    request=SendStreamingMessageRequest(
        params=MessageSendParams(**send_payload)
    )
    print('...Single Turn Streaming Request...')
    stream_response=client.send_message_streaming(request)
    
    async for chunk in stream_response:
        print_json_result_response(chunk,'Streamining chunk')
        
        
async def run_multi_turn_message(client:A2AClient)->None:
    """Run a multi-turn non-streaming test..."""
    print('....Multi-Turn Request.....')
    
    #First turn
    first_turn_payload=create_send_message_payloadformat(
        text='How much is 1000 USD?'
    )
    request1=SendMessageRequest(
        params=MessageSendParams(**first_turn_payload)
    )
    first_turn_response:SendMessageResponse=await client.send_message(
        request1
    )
    print_json_result_response(first_turn_response,'Multi-turn:First Turn response')
    
    contex_id:str|None=None
    if isinstance(
        first_turn_response.root, SendMessageSuccessResponse
    ) and isinstance(first_turn_response.root.result, Task):
        task: Task = first_turn_response.root.result
        context_id = task.contextId  # Capture context ID

        # --- Second Turn (if input required) ---
        if task.status.state == TaskState.input_required and context_id:
            print('--- Multi-Turn: Second Turn (Input Required) ---')
            second_turn_payload = create_send_message_payloadformat(
                'in EUR', task.id, context_id
            )
            request2 = SendMessageRequest(
                params=MessageSendParams(**second_turn_payload)
            )
            second_turn_response = await client.send_message(request2)
            print_json_result_response(
                second_turn_response, 'Multi-Turn: Second Turn Response'
            )
        elif not context_id:
            print('Warning: Could not get context ID from first turn response.')
        else:
            print(
                'First turn completed, no further input required for this test case.'
            )



async def main()->None:
    """Main function to run the different scenario"""
    print(f'connecting to agent at{AGENT_URL}...')
    
    try:
        async with httpx.AsyncClient() as httpx_client:
            client= A2AClient.get_client_from_agent_card_url(
                httpx_client,AGENT_URL
            )
            print('Connection is successfull')
            
            await run_single_turn_message(client)
            await run_streaming_message(client)
            await run_multi_turn_message(client)
    except Exception as e:
        traceback.print_exc()
        print(f'An Error occurred :{e}')

if __name__=='__main__':
    import asyncio
    asyncio.run(main())