from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder


def success_response(message: str = "success", data = None):
    content = {
        "code": 200,
        "message": message,
        "data": data
    }
    # 目标：把任何的fastapi、Pydantic、ORM对象 都必定按此格式响应
    # 使用jsonable_encoder可以将任何的fastapi、Pydantic、ORM对象 转换为可json序列化的对象
    return JSONResponse(content=jsonable_encoder(content))



