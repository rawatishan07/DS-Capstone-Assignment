from profiles import users, user_exists
from graph import network, get_friends

def recommend_friends(username, top_n=5):
    if not user_exists(username):
        return None, f"User '{username}' not found."

    profile = users[username]
    my_interests = set(profile["interests"])
    my_location  = profile.get("location", "").lower()

    current_friends = network.get(username, set())
    exclude = current_friends | {username}

    scores = []

    for candidate, cdata in users.items():
        if candidate in exclude:
            continue

        common = list(my_interests & set(cdata["interests"]))
        loc_match = (
            my_location != "" and
            my_location == cdata.get("location", "").lower()
        )
        score = len(common)
        if score == 0 and not loc_match:
            continue

        scores.append((score, int(loc_match), candidate, common))

    scores.sort(key=lambda x: (x[0], x[1]), reverse=True)

    result = []
    for score, loc, candidate, common in scores[:top_n]:
        result.append({
            "username":      candidate,
            "name":          users[candidate]["name"],
            "common":        sorted(common),
            "score":         score,
            "location_match": bool(loc)
        })

    return result, None
