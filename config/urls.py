"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""


# from django.contrib import admin
# from django.urls import path, include

# from drf_spectacular.views import (SpectacularAPIView, SpectacularSwaggerView)

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     # Include your other app URLs here, e.g.:
#     path('example_calculator_app/', include('apps.example_calculator_app.urls')),
#     path('example_greeter_app/', include('apps.example_greeter_app.urls')),

#     # YOUR API SCHEMA AND UI URLS
#     # Schema View: Generates the OpenAPI schema
#     path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
#     # Swagger UI: Renders the schema in a user-friendly interface
#     path('', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

#     # You can also add Redoc if you prefer:
#     # from drf_spectacular.views import SpectacularRedocView
#     # path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
# ]

# config/urls.py
"""
URL configuration for config project.
"""

from django.contrib import admin
from django.urls import path, include

from drf_spectacular.views import (SpectacularAPIView, SpectacularSwaggerView)

urlpatterns = [
    path('admin/', admin.site.urls),

    # API SCHEMA AND UI URLS - It's often good practice to put these first
    # Or at least ensure they don't conflict with your app URLs by their paths.
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Serve Swagger UI at the root ('/')
    # Make sure this doesn't conflict with any app URL pattern that also uses ''
    path('', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),


    # Include your other app URLs here, usually with specific prefixes
    # These paths are explicit, so they won't conflict with the root ('/') swagger UI.
    path('calculator/', include('apps.example_calculator_app.urls')),
    path('greeter/', include('apps.example_greeter_app.urls')),


    # You can also add Redoc if you prefer:
    # from drf_spectacular.views import SpectacularRedocView
    # path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
