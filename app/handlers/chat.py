from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import JSONResponse
from app.models.conversation import ConversationManager
from app.handlers.response_handler import process_ai_response

chat_router = APIRouter()

@chat_router.post("/chat")
async def handle_chat(
    request: Request,
    message: str = Form(...),
    conv_manager: ConversationManager = Depends(ConversationManager)
):
    conversation = conv_manager.get_conversation(request)
    conversation.add_message("user", message)
    
    ai_response = await process_ai_response(message, conversation.context)
    conversation.add_message("assistant", ai_response)
    
    return JSONResponse({
        "response": ai_response,
        "conversation_id": conversation.id
    })

@chat_router.post("/new_chat")
async def new_chat(
    request: Request,
    conv_manager: ConversationManager = Depends(ConversationManager)
):
    old_conv_id = conv_manager.get_conversation(request).id
    conv_manager.conversations.pop(old_conv_id, None)
    new_conv = conv_manager.get_conversation(request)
    
    return JSONResponse({
        "status": "success",
        "new_conversation_id": new_conv.id
    })