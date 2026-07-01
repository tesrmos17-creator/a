# src/worker.py
from workers import Response, WorkerEntrypoint
from fastapi import FastAPI

app = FastAPI()

class Default(WorkerEntrypoint):
    async def fetch(self, request):
        # Menyambungkan FastAPI ke runtime Workers
        return await app.handle_request(request, self.env)

@app.get("/api/videos")
async def get_all_videos(env):
    # 'DB' adalah nama binding Cloudflare D1 (SQLite) Anda
    # Mengambil data langsung dengan perintah SQL standar
    result = await env.DB.prepare("SELECT * FROM Content").all()
    return Response.json(result)

@app.post("/api/history")
async def save_progress(video_id: int, progress: int, env):
    # Menyimpan progress durasi nonton ke SQLite
    await env.DB.prepare(
        "INSERT INTO WatchHistory (video_id, progress_seconds) VALUES (?, ?)"
    ).bind(video_id, progress).run()
    return Response.json({"status": "success"})
