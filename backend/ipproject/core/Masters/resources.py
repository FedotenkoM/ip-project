from starlette.endpoints import HTTPEndpoint
from starlette.responses import JSONResponse
from starlette.routing import Route

from ipproject.core.database import db
from ipproject.core.Masters.models import MasterModel
from ipproject.core.permissions.models import PermissionAction
from ipproject.core.utils import (
    make_error, Permissions, jwt_required, make_response,
    GinoQueryHelper, make_list_response,
    NO_CONTENT, with_transaction, validation
)
permissions = Permissions(app_name='masters')


class Masters(HTTPEndpoint):
    @staticmethod
    @jwt_required
    @permissions.required(action=PermissionAction.GET)
    async def get(request):
        current_query = MasterModel.query
        total_query = db.select([db.func.count(MasterModel.id)])

        query_params = request.query_params

        if 'search' in query_params:
            current_query, total_query = GinoQueryHelper.search(
                MasterModel.username,
                query_params['search'],
                current_query,
                total_query
            )

        current_query = GinoQueryHelper.pagination(
            query_params, current_query
        )
        current_query = GinoQueryHelper.order(
            query_params,
            current_query, {
                'id': MasterModel.id,
                'username': MasterModel.username,
                'phone': MasterModel.phone,
                }
        )

        total = await total_query.gino.scalar()
        items = await current_query.gino.all()

        return make_list_response(
            [item.jsonify() for item in items],
            total
        )

    @with_transaction
    @jwt_required
    @permissions.required(action=PermissionAction.CREATE)
    @validation(schema={
        'username': {
            'required': True,
            'type': str,
            'min_length': 4,
            'max_length': 50,
        },
        'phone': {
            'required': True,
            'type': str,
            'min_length': 11,
            'max_length': 11,
        }
    })
    async def post(self, data):
        new_master = await MasterModel.create(
            username=data['username'],
            phone=data['phone'],
        )
        return make_response({'id': new_master.id})


class Master(HTTPEndpoint):
    @staticmethod
    @jwt_required
    @permissions.required(action=PermissionAction.GET)
    async def get(request):
        master_id = request.path_params['master_id']
        master = await MasterModel.get(master_id)
        if master:
            return JSONResponse(master.jsonify())
        return make_error(description='Master not found', status_code=404)

    @with_transaction
    @jwt_required
    @permissions.required(action=PermissionAction.UPDATE)
    @validation(schema={
        'username': {
            'required': False,
            'type': str,
            'min_length': 4,
            'max_length': 50,
        },
        'phone': {
            'required': False,
            'type': str,
            'min_length': 11,
            'max_length': 11,
        }
    })
    async def patch(self, request, data):
        master_id = request.path_params['master_id']
        master = await MasterModel.get(master_id)
        if not master:
            return make_error(
                f'Мастер с идентификатором {master_id} не найден',
                status_code=404
            )
        values = {
            'username': data['name'] if 'username' in data else None,
            'phone': data['phone'] if 'phone' in data else None,
        }
        values = dict(filter(lambda item: item[1] is not None, values.items()))
        await Master.update(**values).apply()
        return NO_CONTENT


async def ping(request):
    return JSONResponse({'onPing': 'wePong'})

routes = [
    Route('/', Masters),
    Route('/{master_id:int}', Master),
    Route('/ping', ping, methods=['GET'])
]
