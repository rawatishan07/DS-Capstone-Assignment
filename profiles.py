users = {}

def add_user(username, name, age, interests, location=""):
    if username in users:
        return False, f"User '{username}' already exists."
    users[username] = {
        "name": name,
        "age": age,
        "interests": [i.strip().lower() for i in interests.split(",")],
        "location": location
    }
    return True, f"User '{username}' added successfully!"

def get_profile(username):
    if username not in users:
        return None, f"User '{username}' not found."
    return users[username], None

def update_profile(username, key, value):
    if username not in users:
        return False, f"User '{username}' not found."
    valid_keys = ["name", "age", "interests", "location"]
    if key not in valid_keys:
        return False, f"Invalid field '{key}'. Choose from: {valid_keys}"
    if key == "interests":
        users[username][key] = [i.strip().lower() for i in value.split(",")]
    else:
        users[username][key] = value
    return True, f"Profile updated: '{key}' changed successfully."

def user_exists(username):
    return username in users

def all_users():
    return list(users.keys())

def preload_sample_data():
    samples = [
        ("alice",   "Alice Sharma",   21, "music, travel, coding",          "Delhi"),
        ("bob",     "Bob Mehta",      22, "coding, gaming, music",           "Mumbai"),
        ("carol",   "Carol Singh",    20, "travel, photography, art",        "Delhi"),
        ("dave",    "Dave Rao",       23, "gaming, sports, coding",          "Bangalore"),
        ("eve",     "Eve Kapoor",     21, "music, art, dance",               "Chennai"),
        ("frank",   "Frank Nair",     24, "travel, coding, music",           "Kochi"),
        ("grace",   "Grace Pillai",   22, "photography, travel, art",        "Pune"),
        ("henry",   "Henry Bose",     25, "sports, gaming, coding",          "Kolkata"),
    ]
    for uname, name, age, interests, loc in samples:
        add_user(uname, name, age, interests, loc)