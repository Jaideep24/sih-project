import os
from django.conf import settings
from stream_chat import StreamChat

def get_stream_client():
    return StreamChat(api_key=settings.STREAM_API_KEY, api_secret=settings.STREAM_API_SECRET)

def create_stream_channel(room_id, name, creator_id, member_ids, category):
    client = get_stream_client()
    channel = client.channel(
        "messaging",
        room_id,
        {
            "name": name,
            "members": member_ids,
            "category": category,
        },
    )
    channel.create(creator_id)
    return channel

def end_stream_channel(room_id):
    client = get_stream_client()
    channel = client.channel("messaging", room_id)
    channel.update({"status": "ended"})
    return channel

def add_user_to_channel(room_id, user_id):
    client = get_stream_client()
    channel = client.channel("messaging", room_id)
    channel.add_members([user_id])
    return channel

def generate_user_token(student_id):
    client = get_stream_client()
    return client.create_token(student_id)
