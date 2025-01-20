from django.urls import path
from . import queue_views, plain_text_views

open_api_url = [
   path('queues/', queue_views.QueueListAPIView.as_view(), name='queue_list'),
   path('queues/create/', queue_views.QueueCreateAPIView.as_view(), name='queue_creation'),
   path('queues/<int:queue_id>/', queue_views.QueueInfoAPIView.as_view(), name='queue_info'),
   path('queues/<int:queue_id>/add_waiter/', queue_views.QueueAddWaiterAPIView.as_view(), name='queue_add_waiter'),
   path('queues/<int:queue_id>/process_waiter/<int:waiter_id>/', queue_views.QueueProcessWaiterAPIView.as_view(), name='queue_process_waiter'),
   path('queues/<int:queue_id>/process_next_waiter/', queue_views.QueueProcessNextWaiterAPIView.as_view(), name='queue_process_next_waiter'),
   path('queues/<int:queue_id>/finish_processing_waiter/<int:waiter_id>/', queue_views.QueueFinishProcessingWaiterAPIView.as_view(), name='queue_finish_processing_waiter'),
   path('queues/<int:queue_id>/expected_waiting_time/', queue_views.QueueExpectedWaitingTimeAPIView.as_view(), name='queue_expected_waiting_time'),
   path('queues/<int:queue_id>/expected_waiting_time/<int:waiter_id>/', queue_views.QueueWaiterExpectedWaitingTimeAPIView.as_view(), name='queue_waiter_expected_waiting_time'),
   path('queues/<int:queue_id>/expected_processing_time/', queue_views.QueueExpectedProcessingTimeAPIView.as_view(), name='queue_expected_processing_time'),
]

text_page_api_url = [
   path('text_page/', plain_text_views.GetAllTextPageAPIView.as_view(), name='text_page_list'),
   path('text_page/create/', plain_text_views.CreateTextPageAPIView.as_view(), name='text_page_creation'),
   path('text_page/<int:text_page_id>/', plain_text_views.TextPageInfoAPIView.as_view(), name='text_page_info'),
   path('text_page/<int:text_page_id>/text/', plain_text_views.TextPageAPIView.as_view(), name='text_page_text'),
]

