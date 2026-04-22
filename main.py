import time
from fastapi import FastAPI, Request
from api import api_router
from fastapi.responses import JSONResponse 


app = FastAPI()

app.include_router(api_router)

# @app.middleware("http")
# async def log_requests(request:Request, call_next):
#     print(f"Request:{request.method} {request.url}, {request.headers}")
#     start_time = time.time()
#     response = await call_next(request)
#     end_time = time.time()
#     print(f"Response:{end_time-start_time} seconds")
#     response.headers["X-Process-Time"] = str(end_time-start_time)
#     return response

# @app.middleware('http')
# async def another_middleware(request: Request, call_next):
#     response = await call_next(request)
#     response.headers["X-App-Version"] = "1.0.0"
#     return response

# @app.middleware('http')
# async def third_middleware(request: Request, call_next):
#     user_agent = request.headers.get("User-Agent")
#     if 'Postman' in user_agent:
#         print
#     response = await call_next(request)
#     return response

@app.middleware('http')
async def third_middleware(request: Request, call_next):
    return JSONResponse(content={"message": "Kechirasiz, serverda texnik ishlar olib borilmoqda. 1 soatdan so'ng urinib ko'ring"}, status_code=403)