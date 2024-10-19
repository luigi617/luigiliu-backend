from django.urls import path
from . import views
treasure_hunt_urlpatterns = [
    path('add-new-treasure-hunt-game/', views.NewTreasureHuntGameAPIView.as_view(), name='new_treasure_hunt_game'),
    path('start-treasure-hunt-game/', views.StartTreasureHuntGameAPIView.as_view(), name='start_treasure_hunt_game'),
    path('end-treasure-hunt-game/', views.TreasureEndGameAPIView.as_view(), name='end_treasure_hunt_game'),

    path('treasures/', views.GroupTreasureListAPIView.as_view(), name='treasure_list'),
    path('treasures/<int:pk>/', views.TreasureRetrieveAPIView.as_view(), name='treasure_retrieve'),
    path('treasures/<int:pk>/hints/', views.GroupTreasureHintListAPIView.as_view(), name='treasure_hint_list'),


    path('group-treasure/', views.GroupTreasureUpdateAPIView.as_view(), name='update_group_treasure'),
    path('group-treasure-hint/', views.GroupTreasureHintUpdateAPIView.as_view(), name='update_group_treasure_hint'),

    path('treasure-hunt-games/', views.TreasureGameListAPIView.as_view(), name='treasure_hunt_games_list'),
    path('treasure-hunt-games/<int:pk>/', views.TreasureGameRetrieveAPIView.as_view(), name='treasure_hunt_game_retrieve'),
    path('treasure-hunt-game-groups/', views.TreasureGameGroupListUpdateAPIView.as_view(), name='treasure_hunt_game_groups'),
    path('treasure-hunt-games/<int:pk>/treasures/', views.TreasureHuntGameTreasuresAndHintListUpdateAPIView.as_view(), name='treasure_hunt_game_treasures'),
    path('treasure-hunt-games/<int:pk>/delete-treasures-and-hints/', views.TreasureHuntGameTreasuresAndHintDeleteAPIView.as_view(), name='delete_treasures_and_hints'),
    path('treasure-hunt-games/<int:pk>/evidences/', views.TreasureEvidencesAPIView.as_view(), name='treasure_evidences'),

    path('group-treasures-process/', views.GroupTreasureProcessAPIView.as_view(), name='group_treasures_process'),

]