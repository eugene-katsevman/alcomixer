from aiohttp import web
import asyncio
import functools
import json


def counted(function):
    @functools.wraps(function)
    async def _wrapper(request):
        request.app.rps += 1
        return await function(request)
    return _wrapper


def json_response(data=None, status=200,
                  headers=None) -> web.Response:
    data = data or {}
    return web.Response(body=json.dumps(data),
                        content_type='application/json',
                        status=status,
                        headers=headers)


class CountedApplication(web.Application):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rps = 0

    async def emit_rps(self):
        print(f'{self.rps} rps')
        self.rps = 0
        await asyncio.sleep(1)
        asyncio.get_event_loop().create_task(self.emit_rps())


