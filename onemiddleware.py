# -*- coding : utf-8 -*-
# @Auther    : Careslten
# @time      : 2021/10/13 12:02
# @File      : onemiddleware.py
# @SoftWare  : onespro

from django.utils.deprecation import MiddlewareMixin
import logging
Middleware = logging.getLogger(__name__)
class Mlmlogging(MiddlewareMixin):
    def process_request(self, request):
        Middleware.info(request.body)
