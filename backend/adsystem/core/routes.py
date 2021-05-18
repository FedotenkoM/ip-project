from starlette.routing import Route, Mount
from starlette.responses import JSONResponse

from adsystem.core.users.resources import routes as user_routes
from adsystem.core.roles.resources import routes as roles_routes
from adsystem.core.permissions.resources import get_apps


async def ping(request):
    return JSONResponse({'onPing': 'wePong'})

routes = [
    Route('/ping', ping),
    Route('/apps', get_apps, methods=['GET']),
    Mount('/users', routes=user_routes),
    Mount('/roles', routes=roles_routes),
]
