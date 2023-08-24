from fastapi import APIRouter, Depends, BackgroundTasks
from fastapi.responses import StreamingResponse

from chatbot.utils import predict_2


chatbot = APIRouter()


@chatbot.get("/bot_response")
def get_bot_response():
    # print("inside")
    # response, = predict_2(
    #     query)
    return {
        "response": "dlknlknlkn",
    }
