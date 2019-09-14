import asyncio
from aiohttp import web
import functools
import json

from utils import counted, json_response, CountedApplication

@counted
async def handle_post_cocktail(request):
    shortlink = 'aaaaa'
    data = {'status': 'OK', 'shortlink': shortlink}
    return json_response(data=data, status=303, headers={
        'Location': f'/coctails/{shortlink}'})


@counted
async def handle_get_cocktail(request):
    data = {'id': request.match_info.get('cocktail_id')}
    return json_response(data=data)


def create_app(log_rps=False):
    app = CountedApplication()
    app.add_routes(
        [
            web.post('/v1/cocktails', handle_post_cocktail),
            web.get('/v1/cocktails/{cocktail_id}', handle_get_cocktail)
        ])

    if log_rps:
        asyncio.get_event_loop().create_task(app.emit_rps())
    return app


if __name__ == '__main__':
    app = create_app(log_rps=True)
    web.run_app(app)
