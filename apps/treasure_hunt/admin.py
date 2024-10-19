from django.contrib import admin

# Register your models here.
from apps.treasure_hunt.models import *

admin.site.register(Treasure)
admin.site.register(TreasureHint)
admin.site.register(Group)
admin.site.register(GroupTreasure)
admin.site.register(GroupTreasureHint)
admin.site.register(TreasureHuntGame)