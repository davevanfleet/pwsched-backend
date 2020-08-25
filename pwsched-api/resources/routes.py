from .shift import ShiftApi, ShiftsApi
from .congregation import CongregationApi, CongregationsApi
from .user import UserApi, UsersApi


def initialize_routes(api):
    api.add_resource(ShiftsApi, '/shifts')
    api.add_resource(ShiftApi, '/shifts/<id>')
    api.add_resource(CongregationsApi, '/congregations')
    api.add_resource(CongregationApi, '/congregation/<id>')
    api.add_resource(UsersApi, '/users')
    api.add_resource(UserApi, '/users/<id>')
