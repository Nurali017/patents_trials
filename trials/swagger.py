from drf_yasg.inspectors import SwaggerAutoSchema


class NoFilterAutoSchema(SwaggerAutoSchema):
    def get_filter_parameters(self):
        return []

    def get_paginator_parameters(self, paginator):
        return []



