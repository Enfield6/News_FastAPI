from fastapi import FastAPI
from routers import news
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()


# 挂载路由
app.include_router(news.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],    # 允许的域名
    allow_credentials=True, # 允许携带cookie
    allow_methods=["*"],    # 允许的请求方法
    allow_headers=["*"],    # 允许的请求头
)


