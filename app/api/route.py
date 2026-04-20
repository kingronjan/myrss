from typing import Callable, Coroutine, Any
from functools import partial

from fastapi import Request, Response, APIRouter as _APIRouter
from fastapi.routing import APIRoute
from fastapi.encoders import jsonable_encoder

from app.api import response


class UnifiedAPIRoute(APIRoute):

    def get_route_handler(self) -> Callable[[Request], Coroutine[Any, Any, Response]]:
        raw_handler = super().get_route_handler()

        async def wrapper(request: Request) -> Response:
            resp = await raw_handler(request)
            if isinstance(resp, Response):
                return resp
            return response.success(jsonable_encoder(resp))

        return wrapper


APIRouter = partial(_APIRouter, route_class=UnifiedAPIRoute)
