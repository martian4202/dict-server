from aiohttp import web
from settings import config
import sys, traceback
import mdict
from typing import List


async def search_dict(request: web.Request) -> web.StreamResponse:
    dicts: List[mdict.Dict] = request.app['dicts']
    word: str = request.query['word']
    output: List[str] = []
    for d in dicts:
        output = await d.lookup(word)
        if output is not None and len(output) > 0:
            return web.Response(text=output[0], content_type='text/html')
    return web.Response(text="can not find definitions", content_type='text/plain')


def setup_routes(app) -> None:
    app.router.add_get('/', search_dict)


async def init_dict(app) -> None:
    configs = app['config']['dict']
    dicts: List[mdict.Dict] = []
    for c in configs.values():
        md = mdict.Dict(mdx=c.get('mdx'), style=c.get('css'))
        dicts.append(md)
    app['dicts'] = dicts

if __name__ == '__main__':
    app = web.Application()
    setup_routes(app)
    app['config'] = config
    app.on_startup.append(init_dict)
    web.run_app(app)
