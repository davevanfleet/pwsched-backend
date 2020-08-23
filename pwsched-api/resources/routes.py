from .shift import ShiftApi, ShiftsApi


def initialize_routes(api):
    api.add_resource(ShiftsApi, '/shifts')
    api.add_resource(ShiftApi, '/shifts/<id>')
