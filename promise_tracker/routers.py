from rest_framework import routers
from promise_tracker.views import PromiseViewSet
 
router = routers.SimpleRouter()
 
router.register('promise', PromiseViewSet)
 
urlpatterns = [
   *router.urls,
] 