import json
from random import random
from fastapi import FastAPI, Request, Response
from starlette.responses import StreamingResponse
from core.qna_entry import handle
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def handle_user_query(user_query, session_id):
    yield "[STATUS]", "思考中..."
    type, content = handle(user_query, session_id)
    yield type, content
    yield "[END]", None


@app.get("/chat")
async def query(request: Request, response: Response):
    # 从查询字符串中获取 session ID
    session_id = request.query_params.get("session_id")
    user_query = request.query_params.get("query")

    if not session_id:
        session_id = random.randint(1000000, 9999999)

    if not user_query:
        return Response(content="Missing query", status_code=400)

    results = handle_user_query(user_query, session_id)

    async def event_generator():
        for response_type, content in results:
            data = {
                "type": response_type,
                # if content is dict, convert it to json string
                "content": json.dumps(content) if isinstance(content, dict) else content
            }                
            yield f"data: {json.dumps(data)}\n\n"

    response.headers["Content-Type"] = "application/json"
    response.headers["Cache-Control"] = "no-cache"
    response.headers["Connection"] = "keep-alive"
    return StreamingResponse(event_generator(), media_type="text/event-stream")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)