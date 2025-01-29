from django.contrib.contenttypes.models import ContentType
from .models import Actions
import datetime
from django.utils import timezone

# create the action
def create_action(user,verb,target=None):
    #check for the last min duplicate action 
    now = timezone.now()
    last_minute = now - timezone.timedelta(seconds=60)
    similar_actions = Actions.objects.filter(
        user = user,
        verb = verb,
        created__gte = last_minute
    )
    if target:
        target_ct = ContentType.objects.get_for_model(target)
        similar_actions = similar_actions.filter(
            target_ct= target_ct,
            target_id = target.id
        )
    if not similar_actions:
        action = Actions(user=user,verb=verb,target=target)
        action.save()
        return True
    return False
    