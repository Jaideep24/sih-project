from django import template
from django.utils import timezone
from datetime import datetime, timedelta

register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter
def get_slot_start_iso(slot):
    """Return ISO datetime string for slot's next occurrence (today or next week if in past)."""
    try:
        weekday_map = {'Monday':0,'Tuesday':1,'Wednesday':2,'Thursday':3,'Friday':4,'Saturday':5,'Sunday':6}
        slot_weekday = weekday_map.get(slot.day, None)
        if slot_weekday is None:
            return ''
        now = timezone.localtime()
        today = now.date()
        days_ahead = (slot_weekday - today.weekday()) % 7
        slot_date = today if days_ahead == 0 else today + timedelta(days=days_ahead)
        slot_time = slot.start_time
        slot_datetime = datetime.combine(slot_date, slot_time)
        if slot_datetime < now:
            slot_date = slot_date + timedelta(days=7)
            slot_datetime = datetime.combine(slot_date, slot_time)
        return slot_datetime.isoformat()
    except Exception:
        return ''
