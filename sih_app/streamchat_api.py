import os
from django.conf import settings
from stream_chat import StreamChat

def get_stream_client():
    return StreamChat(api_key=settings.STREAM_API_KEY, api_secret=settings.STREAM_API_SECRET)

def create_stream_channel(room_id, name, creator_id, member_ids, category):
    client = get_stream_client()
    
    try:
        # First, upsert users to ensure they exist with proper permissions
        users_to_upsert = []
        for user_id in member_ids:
            users_to_upsert.append({
                'id': str(user_id),
                'name': f'Student_{user_id}',
                'role': 'user'  # Explicitly set role
            })
        
        # Add creator if not in member_ids
        if str(creator_id) not in [str(uid) for uid in member_ids]:
            users_to_upsert.append({
                'id': str(creator_id),
                'name': f'Student_{creator_id}',
                'role': 'user'
            })
        
        # Upsert users
        if users_to_upsert:
            print(f"Upserting users: {[u['id'] for u in users_to_upsert]}")
            client.upsert_users(users_to_upsert)
        
        # Use 'messaging' channel type which has better default permissions for regular users
        channel = client.channel(
            "messaging",  # Changed back to "messaging" from "team"
            room_id,
            {
                "name": name,
                "members": [str(uid) for uid in member_ids],
                "category": category
                # Don't set created_by_id here - it's set automatically by create() method
            },
        )
        
        print(f"Creating channel {room_id} with creator {creator_id}")
        # Create the channel with the creator - this automatically sets created_by
        response = channel.create(str(creator_id))
        print(f"Channel created successfully: {response}")
        
        return channel
        
    except Exception as e:
        print(f"Error creating StreamChat channel: {e}")
        raise e

def end_stream_channel(room_id, creator_name="Room Creator"):
    client = get_stream_client()
    channel = client.channel("messaging", room_id)  # Changed from "team" to "messaging"
    
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
    
    # First, upsert the user to ensure they exist with proper permissions
    client.upsert_users([{
        'id': str(user_id),
        'name': user_name if user_name else f'Student_{user_id}',
        'role': 'user'
    }])
    
    channel = client.channel("messaging", room_id)  # Changed from "team" to "messaging"
    
    # Add the user to the channel
    channel.add_members([str(user_id)])
    
    # Send a join notification to all existing members
    # Use valid 'system' type with custom action field
    display_name = user_name if user_name else user_id
    channel.send_message({
        "text": f"👋 {display_name} joined the chat room!",
        "type": "system",
        "action": "user_joined"  # Custom field to identify this specific action
    }, "system")
    
    return channel

def generate_user_token(student_id, student_name=None):
    client = get_stream_client()
    
    # Ensure user exists before generating token
    client.upsert_users([{
        'id': str(student_id),
        'name': student_name if student_name else f'Student_{student_id}',
        'role': 'user'
    }])
    
    return client.create_token(str(student_id))
