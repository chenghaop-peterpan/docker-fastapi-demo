# 🐍 Docker FastAPI 待辦事項與自動化觸發服務

![Build Status](https://github.com/<你的GitHub帳號>/docker-fastapi-demo/actions/workflows/deploy.yml/badge.svg)

這是一個基於 Python FastAPI 的輕量級 RESTful API 容器化練習專案，重點展示如何透過 `Dockerfile` 管理套件依賴、利用快取機制加速建置、使用 `.dockerignore` 縮減映像檔體積，以及透過環境變數（Environment Variables）動態控制容器內的運行模式與金鑰驗證。

---

## 📁 專案結構

```text
docker-fastapi-demo/
├── .github/
│   └── workflows/
│       └── deploy.yml       # GitHub Actions 自動建置並推送至 GHCR
├── .dockerignore            # 排除本機虛擬環境、快取與 Git 紀錄
├── Dockerfile               # Python 3.12-slim 多層快取建置設定
├── main.py                  # FastAPI 核心應用程式
├── requirements.txt         # Python 套件相依清單
└── README.md                # 專案說明文件
```

---

## 🚀 快速開始與部署

### 方式 A：從本機原始碼建置與啟動

1. **建置 Docker Image：**
   ```bash
   docker build -t my-fastapi:v1 .
   ```

2. **啟動容器並注入環境變數：**
   ```bash
   # Linux / macOS / Git Bash
   docker run -d \
     -p 8000:8000 \
     -e APP_ENV="production" \
     -e API_SECRET_KEY="my-super-secret-999" \
     --name api-test \
     my-fastapi:v1

   # Windows PowerShell
   docker run -d -p 8000:8000 -e APP_ENV="production" -e API_SECRET_KEY="my-super-secret-999" --name api-test my-fastapi:v1
   ```

3. **開啟 API 互動文件：**
   瀏覽器前往 `http://localhost:8000/docs` 即可查看 Swagger UI 並直接測試所有端點。

### 方式 B：從 GitHub Container Registry (GHCR) 直接部署

```bash
docker run -d \
  -p 8000:8000 \
  -e APP_ENV="production" \
  -e API_SECRET_KEY="your-custom-key" \
  --name api-test \
  ghcr.io/<你的GitHub帳號>/docker-fastapi-demo:latest
```

---

## ⚙️ 環境變數說明

| 變數名稱 | 預設值 | 說明 |
| :--- | :--- | :--- |
| `APP_ENV` | `development` | 應用程式運行環境標籤（顯示於 `/` 健康檢查端點） |
| `API_SECRET_KEY` | `default-secret-123` | 呼叫 `POST /tasks` 時必須於 Header 帶入的 `X-API-Key` 驗證金鑰 |

---

## 🛠️ 常用 Docker 維運指令速查

### 1. 狀態檢查與日誌監控
* **查看容器狀態與 Port 映射：** `docker ps -a`
* **即時監看 API 請求日誌（按 `Ctrl + C` 離開）：** `docker logs -f api-test`
* **監控即時 CPU 與記憶體用量：** `docker stats api-test`

### 2. 進入容器除錯
* **進入容器內部終端機：**
  ```bash
  docker exec -it api-test bash
  ```
* **驗證容器內的環境變數是否正確注入：**
  ```bash
  docker exec api-test env
  ```

### 3. 停止與環境清理
* **停止容器：** `docker stop api-test`
* **強制停止並刪除容器：** `docker rm -f api-test`
* **刪除本機 Image：** `docker rmi my-fastapi:v1`
* **清理所有無用快取與懸空映像檔：** `docker system prune -f`