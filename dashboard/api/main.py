from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/status")
def status():
    return JSONResponse({"status": "Coexum online"})

def serve_dashboard():
    import uvicorn
    uvicorn.run("dashboard.api.main:app", host="0.0.0.0", port=8000, reload=True)
