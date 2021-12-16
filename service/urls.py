from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, include
from rest_framework import routers
from . import views
from climbing_center import settings
from climbing_center.settings import DEV
from django.views.decorators.csrf import csrf_exempt

from graphene_django.views import GraphQLView
from service.schema import schema

router = routers.DefaultRouter()

urlpatterns = [
    path('api-auth', include('rest_framework.urls', namespace='rest_framework')),
    path('api/login', views.LoginAuthTokenView.as_view(), name='user_login'),
    path('api/logout', views.LogoutUserView, name='user_logout'),
    path('graphql', csrf_exempt(GraphQLView.as_view(graphiql=True, schema=schema))),
]

#urlpatterns = format_suffix_patterns(urlpatterns)
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if DEV:
    from django.views.decorators.csrf import csrf_exempt
    from proxy.views import proxy_view

    @csrf_exempt
    def proxy(request, path):
        remote_url = 'http://localhost:3001/' + path
        return proxy_view(request, remote_url, {})

    urlpatterns.append(url('(?P<path>icm/public/.*)', proxy))
    urlpatterns.append(url('(?P<path>__vite_ping)', proxy))
    urlpatterns.append(url('(?P<path>@windicss-devtools-update)', proxy))

urlpatterns.append(url('.*', views.index, name='index'))