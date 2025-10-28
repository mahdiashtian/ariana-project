from debug_toolbar.toolbar import debug_toolbar_urls

from .base import *

urlpatterns += debug_toolbar_urls()
