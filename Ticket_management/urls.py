from django.urls import path, include
from rest_framework.routers import SimpleRouter
from rest_framework_nested.routers import NestedDefaultRouter
from . import views

router = SimpleRouter()
router.register('tickets', views.TicketViewSet, basename='tickets')
ticket_router=NestedDefaultRouter(router, 'tickets', lookup='tickets')
ticket_router.register('worklogs', views.WorklogViewSet, basename='worklogs')
router.register('assignment', views.AssignmentViewSet, basename='assignment')


urlpatterns =[
    path('',include(router.urls)),
    path('',include(ticket_router.urls)),
    path(
        'tickets/<int:ticket_pk>/ai-summary/',
        views.AiSummarry.as_view(),
        name='ticket-ai-summary'
    ),
]