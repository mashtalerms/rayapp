from rest_framework.routers import DefaultRouter

from accounts.views.authentication import Authentication
from accounts.views.profile import Profile

router = DefaultRouter()

router.register('', Authentication)
router.register('profile', Profile)

urlpatterns = router.urls
