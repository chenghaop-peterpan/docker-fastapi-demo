import os
from datetime import datetime
from typing import List, Optional
from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel

# 從環境變數讀取設定（若未傳入則使用預設值）
APP_ENV = os.getenv("APP_ENV", "development")
API_SECRET_KEY = os.getenv("API_SECRET_KEY", "default-secret-123")

app = FastAPI(
    title="Docker FastAPI 練習服務",
    description=f"目前運行環境模式：{APP_ENV}",
    version="1.0.0",
)

# 模擬記憶體資料庫
tasks_db = [
    {"id": 1, "title": "完成 Docker 專案 1 (Nginx)", "completed": True},
    {"id": 2, "title": "完成 Docker 專案 2 (FastAPI)", "completed": False},
]


class TaskCreate(BaseModel):
    title: str
    completed: Optional[bool] = False


# 1. 健康檢查與環境變數驗證端點（公開）
@app.get("/")
def health_check():
    return {
        "status": "healthy",
        "environment": APP_ENV,
        "server_time": datetime.now().isoformat(),
        "message": "FastAPI 正在 Docker 容器中運行！",
    }


# 2. 取得所有待辦事項（公開）
@app.get("/tasks")
def get_tasks():
    return {"total": len(tasks_db), "items": tasks_db}


# 3. 新增待辦事項 / 觸發任務（需要透過 Header 驗證環境變數傳入的 API_SECRET_KEY）
@app.post("/tasks", status_code=201)
def create_task(task: TaskCreate, x_api_key: Optional[str] = Header(None)):
    if x_api_key != API_SECRET_KEY:
        raise HTTPException(status_code=401, detail="無效的 API Key，請檢查 X-API-Key Header 或容器環境變數設定")

    new_id = max([t["id"] for t in tasks_db], default=0) + 1
    new_task = {"id": new_id, "title": task.title, "completed": task.completed}
    tasks_db.append(new_task)
    return {"message": "任務建立成功", "task": new_task}