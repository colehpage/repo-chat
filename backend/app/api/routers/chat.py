import json
import logging
import time
from typing import List

from fastapi.responses import StreamingResponse

from app.utils.json import json_to_model
from app.utils.index import get_index
from fastapi import APIRouter, Depends, HTTPException, Request, status
from llama_index import VectorStoreIndex
from llama_index.llms.base import ChatMessage
from pydantic import BaseModel

chat_router = r = APIRouter()


class _Message(BaseModel):
    # role: MessageRole
    content: str


class _ChatData(BaseModel):
    messages: List[_Message]

@r.post("")
async def chat(
    request: Request,
    # Note: To support clients sending a JSON object using content-type "text/plain",
    # we need to use Depends(json_to_model(_ChatData)) here
    data: _ChatData = Depends(json_to_model(_ChatData)),
    index: VectorStoreIndex = Depends(get_index),
):
    logger = logging.getLogger("uvicorn")
    
    # check preconditions and get last message
    if len(data.messages) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No messages provided",
        )
    lastMessage = data.messages.pop()
    # if lastMessage.role != MessageRole.USER:
    #     raise HTTPException(
    #         status_code=status.HTTP_400_BAD_REQUEST,
    #         detail="Last message must be from user",
    #     )
    # convert messages coming from the request to type ChatMessage
    messages = [
        ChatMessage(
            # role=m.role,
            content=m.content,
        )
        for m in data.messages
    ]

    # query chat engine
    chat_engine = index.as_chat_engine()
    
    start_time = time.time()
    response = chat_engine.stream_chat(lastMessage.content, messages)
    
    metadata_headers = ''
    
    filenames = {source_node.node.extra_info["file_name"] for source_node in response.source_nodes}
    
    metadata_headers = {
        "Custom-Metadata": ','.join(str(filename) for filename in filenames)
    }

    logger.info(f"Chat response: {response}")
    # stream response
    async def event_generator():
        token_count = 0
                
        for token in response.response_gen:
            # If client closes connection, stop sending events
            if await request.is_disconnected():
                break
            token_count += 1
            yield token
            
        logger.info(f"Files used: {filenames}")
    
        time_elapsed = time.time() - start_time
        tokens_per_second = token_count / time_elapsed
        logger.info(f"Chat response: {response}")
        logger.info(f"Tokens per second: {tokens_per_second}")
        logger.info(f"Total tokens: {token_count}")
        logger.info(f"Time elapsed: {time_elapsed}")
        logger.info(f"Streamed output at {tokens_per_second} tokens/s")
        


    return StreamingResponse(event_generator(), headers=metadata_headers, media_type="text/plain")
