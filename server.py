from aiohttp import web
from settings import config
import sys, traceback
import dict
from typing import List

async def index(request: web.Request)->web.StreamResponse:
    dicts: List[dict.Dictionary] = request.app['dicts']
    word: str = request.query['word']
    output: List[str] = []
    for d in dicts:
        output = await d.lookup(word)
        if (output != None and len(output) > 0):
            return web.Response(text=output[0], content_type='text/html')
    return web.Response(text="can not find definitions", content_type='text/plain')

def setup_routes(app)->None:
    app.router.add_get('/', index)

async def init_dict(app)->None:
    config = app['config']['dict']
    mdict = dict.MDict(config['mdx_file'], config['css_file'])
    app['dicts'] = []
    dicts: List[dict.Dictionary] = app['dicts']
    dicts.append(mdict)
    dicts.append(dict.OLDict())

app = web.Application()
setup_routes(app)
app['config'] = config
app.on_startup.append(init_dict)
web.run_app(app)
