FROM python:3.13-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt \
    && useradd --uid 1000 --create-home chess \
    && mkdir /data && chown chess:chess /data
COPY server.py .
COPY dist ./dist
ENV PORT=3000 HOST=0.0.0.0 CHESS_DB=/data/rooms.sqlite3 PYTHONUNBUFFERED=1
USER chess
EXPOSE 3000
CMD ["python", "server.py", "--no-browser"]
