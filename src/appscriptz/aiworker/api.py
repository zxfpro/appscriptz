from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException, Depends, Request, Response
from fastapi.responses import JSONResponse
from datetime import datetime
from pydantic import BaseModel, Field, validator
from typing import Literal, Optional
from typing import List, Dict, Any, Optional
from threading import Timer
import traceback
import time
import asyncio
import json
import uuid
import os

import nest_asyncio
nest_asyncio.apply()

from kimi_product import kimi_chat

# 响应结构
def response_info(message:str, code:int):
    return {"message": message, "code":code ,"version":"0.1"}

# 垃圾回收
def check_and_clean_inactive_users():
    current_time = time.time()
    expired_users = []

    for user_id, user_info in user_resources.items():
        last_active_time = user_info["last_active"]
        if current_time - last_active_time > 3600:  # 过期秒数
            expired_users.append(user_id)

    for user_id in expired_users:
        del user_resources[user_id]
        print(f"User {user_id} has been removed due to inactivity.")
    
    Timer(60, check_and_clean_inactive_users).start() # 轮训频率 n秒/次

def update_user_activity(session_id):
    user_resources[session_id]["last_active"] = time.time()  # 记录当前时间戳

app = FastAPI()

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], #TODO 安全组配置
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 用户状态留存与回收
user_resources = {}
request_records: Dict[str, list] = {}
check_and_clean_inactive_users()


@app.post("/api/chat_kimi")
async def chat_kimi(request:Request):
    try:
        data = await request.json()
        prompt = data.get("prompt", "")
        pages = data.get("pages",1)
        result = kimi_chat(prompt,pages)

        return JSONResponse(
            status_code=200,
            content=response_info(result,200)
        )
    except Exception as e:
        error_info = traceback.format_exc()
        return JSONResponse(
            status_code=500,
            content=response_info(f"An unexpected error TODO 获取当前函数名: {error_info}",500)
        )





if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api:app", 
                host="0.0.0.0", 
                port=8078, 
                reload=False, # 开启热更新
                loop="asyncio")

    