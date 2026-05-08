from profiles import user_exists

network = {}

def _ensure_node(username):
    if username not in network:
        network[username] = set()

def add_friend(user1, user2):
    if not user_exists(user1):
        return False, f"User '{user1}' not found."
    if not user_exists(user2):
        return False, f"User '{user2}' not found."
    if user1 == user2:
        return False, "A user cannot befriend themselves."
    _ensure_node(user1)
    _ensure_node(user2)
    if user2 in network[user1]:
        return False, f"'{user1}' and '{user2}' are already friends."
    network[user1].add(user2)
    network[user2].add(user1)
    return True, f"Friendship added between '{user1}' and '{user2}'."

def remove_friend(user1, user2):
    if user1 not in network or user2 not in network[user1]:
        return False, f"'{user1}' and '{user2}' are not friends."
    network[user1].discard(user2)
    network[user2].discard(user1)
    return True, f"Friendship removed between '{user1}' and '{user2}'."

def get_friends(username):
    if username not in network:
        return [], f"'{username}' has no connections yet."
    return sorted(network[username]), None

def get_network():
    return network

def preload_sample_connections():
    connections = [
        ("alice", "bob"),
        ("alice", "carol"),
        ("bob",   "dave"),
        ("bob",   "eve"),
        ("carol", "grace"),
        ("carol", "frank"),
        ("dave",  "henry"),
        ("eve",   "frank"),
        ("frank", "grace"),
        ("grace", "henry"),
    ]
    for u1, u2 in connections:
        add_friend(u1, u2)