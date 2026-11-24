# 1. 使用官方輕量級 Python 基底映像檔 (slim 版本約 130MB，比完整版 1GB 小很多)
FROM python:3.12-slim

# 2. 設定環境變數：避免 Python 產生 .pyc 檔，並讓 console log 即時輸出（方便 docker logs 查看）
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# 3. 設定容器內的工作目錄
WORKDIR /app

# 4. 【關鍵最佳實踐】先單獨複製 requirements.txt 並安裝套件
# 只要套件清單沒改，之後修改 main.py 重新 build 時就會直接沿用快取，省下重新下載的時間
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. 複製其餘程式碼到工作目錄
COPY . .

# 6. 宣告服務監聽的 Port
EXPOSE 8000

# 7. 容器啟動時執行的預設指令（綁定 0.0.0.0 才能讓外部透過 Port 映射連入）
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]