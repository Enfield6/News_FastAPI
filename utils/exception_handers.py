from fastapi import HTTPException
from fontTools.varLib.iup import Integral
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from utils.exception import http_exception_handler, integrity_error_handler, sqlalchemy_error_handler, \
    general_exception_handler


def register_exception_handler(app):
    """"
        注册全局异常处理,子类在前，父类在后；具体在前，抽象在后。
    """
    app.add_exception_handler(HTTPException, http_exception_handler) # 业务
    app.add_exception_handler(IntegrityError, integrity_error_handler)
    app.add_exception_handler(SQLAlchemyError, sqlalchemy_error_handler)
    app.add_exception_handler(Exception, general_exception_handler)
