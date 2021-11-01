# -*- coding: utf-8 -*-
"""
Tencent is pleased to support the open source community by making BK-ITSM 蓝鲸流程服务 available.

Copyright (C) 2021 THL A29 Limited, a Tencent company.  All rights reserved.

BK-ITSM 蓝鲸流程服务 is licensed under the MIT License.

License for BK-ITSM 蓝鲸流程服务:
--------------------------------------------------------------------
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial
portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT
LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN
NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

from config import RUN_VER, BK_PAAS_HOST, OPEN_VER  # noqa

if RUN_VER == "open":
    from blueapps.patch.settings_open_saas import *  # noqa
else:
    from blueapps.patch.settings_paas_services import *  # noqa

# 正式环境
RUN_MODE = "PRODUCT"

# 只对正式环境日志级别进行配置，可以在这里修改
LOG_LEVEL = "ERROR"
RIO_TOKEN = "bd8f7c983a3e462486b177091733ce93"

# V2
# import logging
# logging.getLogger('root').setLevel('INFO')
# V3
# import logging
# logging.getLogger('app').setLevel('INFO')


# 正式环境数据库可以在这里配置

DATABASES.update(
    {
        "default": {
            "ENGINE": "django.db.backends.mysql",
            "NAME": os.environ.get("DB_NAME"),
            "USER": os.environ.get("DB_USER"),
            "PASSWORD": os.environ.get("DB_PASSWORD"),
            "HOST": os.environ.get("DB_HOST"),
            "PORT": os.environ.get("DB_PORT"),
        },
    }
)


# ===============================================================================
# CSRF SETTINGS
# ===============================================================================
ALLOW_CSRF = os.environ.get("BKAPP_ALLOW_CSRF", None) == "1"
if ALLOW_CSRF:
    # 根据环境变量选择性开启跨域功能
    MIDDLEWARE = ("corsheaders.middleware.CorsMiddleware", "common.middlewares.DisableCSRFCheck",) + MIDDLEWARE

    CORS_ALLOW_CREDENTIALS = True
    # CORS_ORIGIN_WHITELIST = CSRF_WHITELIST
    CORS_ORIGIN_ALLOW_ALL = True

# disable web browsable api in production
# http://masnun.com/2016/04/20/django-rest-framework-remember-to-disable-web-browsable-api-in-production.html
REST_FRAMEWORK.update({"DEFAULT_RENDERER_CLASSES": ("rest_framework.renderers.JSONRenderer",)})

MEDIA_URL = "%smedia/" % SITE_URL
BK_STATIC_URL = '/static'
# ==============================================================================
# 加载环境差异化配置
# ==============================================================================
ver_settings = importlib.import_module('adapter.config.sites.%s.ver_settings' % RUN_VER)
for _setting in dir(ver_settings):
    if _setting.upper() == _setting:
        locals()[_setting] = getattr(ver_settings, _setting)

BK_IAM_RESOURCE_API_HOST = os.getenv(
    "BKAPP_IAM_RESOURCE_API_HOST", urljoin(BK_PAAS_INNER_HOST, "/o/{}".format(APP_CODE))
)
