from aiohttp import web
from settings import config
import sys, traceback
import dict

async def index(request: web.Request)->web.StreamResponse:
    mdict: dict.MDict = request.app['mdict']
    word: str = request.query['word']
    output: str = await mdict.lookup(word)
    return web.Response(text=output[0], content_type='text/html')

def setup_routes(app)->None:
    app.router.add_get('/', index)

async def init_dict(app)->None:
    config = app['config']['dict']
    mdict = dict.MDict(config['mdx_file'], config['css_file'])
    app['mdict'] = mdict

app = web.Application()
setup_routes(app)
app['config'] = config
app.on_startup.append(init_dict)
web.run_app(app)
