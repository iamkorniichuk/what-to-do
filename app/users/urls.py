from .routers import UserRouter
from .viewsets import UserViewSet


app_name = "users"

router = UserRouter()
router.register("", UserViewSet, "user")

urlpatterns = router.urls
