"""API Routes"""

from rest_framework.routers import DefaultRouter
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from strawberry.django.views import AsyncGraphQLView, GraphQLView

from apps.images.views import ImageViewset
from .schema import schema


router = DefaultRouter()

# Register routes
router.register(r"image", ImageViewset, basename="image")


urlpatterns = [
    path(
        "graphql",
        csrf_exempt(GraphQLView.as_view(schema=schema, graphql_ide="graphiql")),
    )
]

urlpatterns += router.urls
