import os
from django.conf import settings
from stream_chat import StreamChat

def get_stream_client():
    return StreamChat(api_key=settings.STREAM_API_KEY, api_secret=settings.STREAM_API_SECRET)

def create_stream_channel(room_id, name, creator_id, member_ids, category):
    client = get_stream_client()
    
    # Use 'team' channel type which has more open permissions by default
    channel = client.channel(
        "team",  # Changed from "messaging" to "team" for better permissions
        room_id,
        {
            "name": name,
            "members": member_ids,
            "category": category,
            # Don't set created_by_id here - it's set automatically by create() method
        },
    )
    
    # Create the channel with the creator - this automatically sets created_by
    response = channel.create(creator_id)
    
    return channel

def end_stream_channel(room_id, creator_name="Room Creator"):
    client = get_stream_client()
    channel = client.channel("team", room_id)
    
    # Send a special system message to notify all users that the room has ended
    # Use valid 'system' type with custom action field
    channel.send_message({
        "text": f"🔴 This chat room has been ended by {creator_name}. You will be redirected to the peer chat lobby.",
        "type": "system",
        "action": "room_ended"  # Custom field to identify this specific action
    }, "system")
    
    # Update channel status
    channel.update({"status": "ended"})
    
    return channel

def add_user_to_channel(room_id, user_id, user_name=None):
    client = get_stream_client()
    channel = client.channel("team", room_id)
    
    # Add the user to the channel
    channel.add_members([user_id])
    
    # Send a join notification to all existing members
    # Use valid 'system' type with custom action field
    display_name = user_name if user_name else user_id
    channel.send_message({
        "text": f"👋 {display_name} joined the chat room!",
        "type": "system",
        "action": "user_joined"  # Custom field to identify this specific action
    }, "system")
    
    return channel

def generate_user_token(student_id):
    client = get_stream_client()
    return client.create_token(student_id)
