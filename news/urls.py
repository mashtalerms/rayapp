from rest_framework.routers import DefaultRouter

from news.views.comments import CommentsViewSet
from news.views.news import NewsViewSet

router = DefaultRouter()

router.register('news', NewsViewSet)
router.register('comments', CommentsViewSet)

urlpatterns = router.urls
