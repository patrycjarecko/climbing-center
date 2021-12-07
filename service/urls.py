from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, include
from rest_framework import routers
from . import views
from climbing_center import settings
from climbing_center.settings import DEV
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

router = routers.DefaultRouter()

schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('api-auth', include('rest_framework.urls', namespace='rest_framework')),
    path('api/register/client', views.RegisterClientView.as_view(), name='register_client'),
    path('api/client', views.ClientListView.as_view(), name='client_list'),
    path('api/client/<int:pk>', views.ClientDetailView.as_view(), name='client_detail'),
    path('api/role', views.RoleListCreateView.as_view(), name='role_create_list'),
    path('api/role/<int:pk>', views.RoleDetailView.as_view(), name='role_detail'),
    path('api/instructor', views.InstructorListCreateView.as_view(), name='instructor_create_list'),
    path('api/instructor/<int:pk>', views.InstructorDetailView.as_view(), name='instructor_detail'),
    path('api/login', views.LoginAuthTokenView.as_view(), name='user_login'),
    path('api/logout', views.LogoutUserView, name='user_logout'),
    path('api/interval', views.IntervalListCreateView.as_view(), name='interval_list_create'),
    path('api/interval/<int:pk>', views.IntervalDetailView.as_view(), name='interval_detail'),
    path('api/pass-type', views.PassTypeListCreateView.as_view(), name='pass_type_list_create'),
    path('api/pass-type/<int:pk>', views.PassTypeDetailView.as_view(), name='pass_type_detail'),
    path('api/section-type', views.SectionTypeListCreateView.as_view(), name='section_type_list_create'),
    path('api/section-type/<int:pk>', views.SectionTypeDetailView.as_view(), name='section_type_detail'),
    path('api/pass', views.PassListCreateView.as_view(), name='pass_list_create'),
    path('api/pass/<int:pk>', views.PassDetailView.as_view(), name='pass_detail'),
    path('api/section', views.SectionListCreateView.as_view(), name='section_list_create'),
    path('api/section/<int:pk>', views.SectionDetailView.as_view(), name='section_detail'),

    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

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