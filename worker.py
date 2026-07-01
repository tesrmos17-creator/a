# src/worker.py (atau worker.py)
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Pada versi baru, WorkerEntrypoint langsung dibaca tanpa perlu di-impor
class Default(WorkerEntrypoint):
    async def fetch(self, request):
        return await app.handle_request(request, self.env)

# Model Data untuk menerima Progress Nonton dari Frontend
class ProgressPayload(BaseModel):
    episode_id: int
    progress_seconds: int

# Endpoint API Ambil Semua Katalog Film dari SQLite Cloud D1
@app.get("/api/videos")
async def get_all_videos(env):
    query = "SELECT * FROM Content"
    result = await env.DB.prepare(query).all()
    return Response.json(result)

# Endpoint API Simpan Progress Durasi Nonton Otomatis
@app.post("/api/history")
async def save_watch_progress(payload: ProgressPayload, env):
    query = """
        INSERT INTO WatchHistory (episode_id, progress_seconds, updated_at) 
        VALUES (?, ?, CURRENT_TIMESTAMP)
    """
    await env.DB.prepare(query).bind(
        payload.episode_id, 
        payload.progress_seconds
    ).run()
    
    return Response.json({"status": "success", "message": "Progress berhasil disimpan!"})
