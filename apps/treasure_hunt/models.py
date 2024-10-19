from django.db import models
from django.contrib.postgres.fields import ArrayField


from apps.core.models import TimeStampedModel

import os
from django.utils import timezone
# Create your models here.



def treasure_location(instance, filename):
    folder_name = f'treasure_hunt/treasure/'
    return os.path.join(folder_name, filename)

class Treasure(TimeStampedModel):
    object = models.ImageField(upload_to=treasure_location, null=True, blank=True,)

def treasure_hint_location(instance, filename):
    folder_name = f'treasure_hunt/treasure_hint/'
    return os.path.join(folder_name, filename)

class TreasureHint(TimeStampedModel):
    hint_img = models.ImageField(upload_to=treasure_hint_location, null=True, blank=True,)
    hint =  models.CharField(max_length=255)
    requirement_for_hint = models.CharField(max_length=255)
    treasure = models.ForeignKey(Treasure, related_name="hints", on_delete=models.CASCADE)

class Group(TimeStampedModel):
    name =  models.CharField(max_length=255)
    users = ArrayField(models.IntegerField())



class GroupTreasureStatus:
    NOT_FOUND = 0
    PROCESSING = 1
    FOUND = 2

    CHOICES = (
        (NOT_FOUND, "Not found"),
        (PROCESSING, "Processing"),
        (FOUND, "Found")
    )

def group_treasure_evidence_location(instance, filename):
    folder_name = f'treasure_hunt/group_treasure_evidence/'
    return os.path.join(folder_name, filename)

class GroupTreasure(TimeStampedModel):
    group = models.ForeignKey(Group, related_name="group_treasure", on_delete=models.PROTECT)
    treasure = models.ForeignKey(Treasure, related_name="group_treasure", on_delete=models.PROTECT)
    status = models.IntegerField(choices=GroupTreasureStatus.CHOICES, default=GroupTreasureStatus.NOT_FOUND)
    found_evidence = models.ImageField(upload_to=group_treasure_evidence_location, null=True, blank=True)
    found_time = models.DateTimeField(blank = True, null = True)
    class Meta:
        unique_together = (('group', 'treasure'),)


def group_treasure_hint_evidence_location(instance, filename):
    folder_name = f'treasure_hunt/group_treasure_hint_evidence/'
    return os.path.join(folder_name, filename)

class GroupTreasureHintStatus:
    NOT_ACTIVATE = 0
    PROCESSING = 1
    ACTIVATE = 2

    CHOICES = (
        (NOT_ACTIVATE, "Not activate"),
        (PROCESSING, "Processing"),
        (ACTIVATE, "Activate")
    )

class GroupTreasureHint(TimeStampedModel):
    group = models.ForeignKey(Group, related_name="group_treasure_hint", on_delete=models.PROTECT)
    treasure_hint = models.ForeignKey(TreasureHint, related_name="group_treasure_hint", on_delete=models.PROTECT)
    status = models.IntegerField(choices=GroupTreasureHintStatus.CHOICES, default=GroupTreasureHintStatus.NOT_ACTIVATE)
    activate_evidence = models.ImageField(upload_to=group_treasure_hint_evidence_location, null=True, blank=True)
    activate_time = models.DateTimeField(blank = True, null = True)
    class Meta:
        unique_together = (('group', 'treasure_hint'),)

class TreasureHuntGameManager(models.Manager):
    def get_current_game_and_group_by_user(self, user):
        if user.is_anonymous:
            return None, None
        started_game = self.filter(is_started = True)
        for game in started_game:
            for group in game.groups:
                g = Group.objects.get(pk = group)
                if user.id in g.users:
                    return game, g
        return None, None
    
    

class TreasureHuntGame(TimeStampedModel):
    groups = ArrayField(models.IntegerField())
    treasures = ArrayField(models.IntegerField())
    time_started = models.DateTimeField(blank = True, null = True)
    time_ended = models.DateTimeField(blank = True, null = True)
    is_started = models.BooleanField(default=False)
    
    objects = TreasureHuntGameManager()

    def end_game_if_all_treasures_found(self, forced = False):
        not_found_group_treasure = GroupTreasure.objects.filter(group_id__in = self.groups, treasure_id__in = self.treasures).exclude(status = GroupTreasureStatus.FOUND)
        if not forced:
            if not_found_group_treasure.exists():
                return
        self.time_ended = timezone.now()
        self.is_started = False
        self.save()
