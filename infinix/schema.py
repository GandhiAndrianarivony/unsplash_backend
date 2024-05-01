import strawberry
from strawberry_django.optimizer import DjangoOptimizerExtension

from apps.users.schema import schemas as user_schema
from apps.images.schema import schemas as image_schema
from apps.authentications.schema import schemas as authentication_schema
from apps.user_profiles.schema import schemas as user_profile_schema


@strawberry.type
class Query(
    user_schema.Query,
    image_schema.Query,
):
    pass


@strawberry.type
class Mutation(
    user_schema.Mutation,
    image_schema.Mutation,
    authentication_schema.Mutation,
    user_profile_schema.Mutation,
):
    pass


schema = strawberry.Schema(
    query=Query,
    mutation=Mutation,
    extensions=[DjangoOptimizerExtension],
)
