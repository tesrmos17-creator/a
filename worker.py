# worker.py (Murni Native - Tanpa FastAPI / Tanpa Library Eksternal)
from workers import WorkerEntrypoint, Response

class Default(WorkerEntrypoint):
    async def fetch(self, request):
        url = request.url

        # 1. Endpoint Ambil Semua Katalog Film
        if "/api/videos" in url:
            query = "SELECT * FROM Content"
            result = await self.env.DB.prepare(query).all()
            return Response.json(result)

        # 2. Endpoint Simpan Progress Durasi Menonton
        elif "/api/history" in url and request.method == "POST":
            payload = await request.json()
            query = """
                INSERT INTO WatchHistory (episode_id, progress_seconds, updated_at)
                VALUES (?, ?, CURRENT_TIMESTAMP)
            """
            
            await self.env.DB.prepare(query).bind(
                payload.get("episode_id"),
                payload.get("progress_seconds")
            ).run()
            return Response.json({"status": "success"})

        # 3. Tampilan Halaman Utama Default
        return Response("Backend Python Web Streaming Anda Sudah Aktif!")
