from fastapi.responses import JSONResponse

from app.core.enums import ResponseCode


def success(data=None, message='success', status_code=200):
    return JSONResponse(
        status_code=status_code,
        content={
            'data': data,
            'message': message,
            'code': ResponseCode.SUCCESS
        })


def failed(data=None, message='failed', status_code=200):
    return JSONResponse(
        status_code=status_code,
        content={
            'data': data,
            'message': message,
            'code': ResponseCode.ERROR,
        })
