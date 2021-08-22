from starlette.endpoints import HTTPEndpoint
from starlette.responses import JSONResponse
from starlette.routing import Route

from ipproject.core.database import db
from ipproject.core.services.models import ServiceModel
from ipproject.core.permissions.models import PermissionAction
from ipproject.core.utils import (
    make_error, Permissions, jwt_required, make_response,
    GinoQueryHelper, make_list_response,
    NO_CONTENT, with_transaction, validation
)

permissions = Permissions(app_name='services')


class Services(HTTPEndpoint):
    @staticmethod
    @jwt_required
    @permissions.required(action=PermissionAction.GET)
    async def get(request):
        current_query = ServiceModel.query
        total_query = db.select([db.func.count(ServiceModel.id)])

        query_params = request.query_params

        if 'search' in query_params:
            current_query, total_query = GinoQueryHelper.search(
                ServiceModel.service_name,
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
                    'id': ServiceModel.id,
                    'service_name': ServiceModel.service_name,
                    'prise': ServiceModel.price,
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
            'service_name': {
                'required': True,
                'type': str,
                'min_length': 4,
                'max_length': 50,
            },
            'prise': {
                'required': True,
                'type': int,
                'prise': True,
            }
        })
        async def post(self, data):
            new_service = await ServiceModel.create(
                service_name=data['service_name'],
                prise=data['prise'],
            )
            return make_response({'id': new_service.id})


class Service(HTTPEndpoint):
    @staticmethod
    @jwt_required
    @permissions.required(action=PermissionAction.GET)
    async def get(request):
        service_id = request.path_params['service_id']
        service = await ServiceModel.get(service_id)
        if service:
            return JSONResponse(service.jsonify())
        return make_error(description='Service not found', status_code=404)

    @with_transaction
    @jwt_required
    @permissions.required(action=PermissionAction.UPDATE)
    @validation(schema={
        'service_name': {
            'required': False,
            'type': str,
            'min_length': 4,
            'max_length': 50,
        },
        'prise': {
            'required': True,
            'type': int,
            'prise': True,
        }
    })
    async def patch(self, request, data):
        service_id = request.path_params['service_id']
        service = await ServiceModel.get(service_id)
        if not service:
            return make_error(
                f'Услуга с идентификатором {service_id} не найдена',
                status_code=404
            )
        values = {
            'service_name': data['name']if 'service_name' in data else None,
            'prise': data['prise'] if 'prise' in data else None,
        }
        values = dict(filter(lambda item: item[1] is not None, values.items()))
        await Services.update(**values).apply()
        return NO_CONTENT


@jwt_required
async def get_actions(request, user):
    return make_response(await permissions.get_actions(user.role_id))


routes = [
    Route('/', Services),
    Route('/{service_id:int}', Service),
    Route('/actions', get_actions, methods=['GET']),
]
