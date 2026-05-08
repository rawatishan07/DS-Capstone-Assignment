# recommendations.py
# Data Structures: Hash Map (interest counting) + Sorting
# Suggests friends ranked by number of common interests
# Bonus: also considers same location (geo DS)

from profiles import users, user_exists
from graph import network, get_friends


def recommend_friends(username, top_n=5):
    """
    Recommend friends for a user based on:
      1. Common interests (primary rank)
      2. Same location (secondary rank / bonus)
    Only suggests users who are NOT already friends.

    Time : O(U * I)  where U = users, I = avg interests per user
    Space: O(U)
    Returns: list of (candidate, common_interests_list, location_match)
    """
    if not user_exists(username):
        return None, f"User '{username}' not found."

    profile = users[username]
    my_interests = set(profile["interests"])
    my_location  = profile.get("location", "").lower()

    # friends and self — exclude from recommendations
    current_friends = network.get(username, set())
    exclude = current_friends | {username}

    scores = []  # (score, location_bonus, candidate, common_list)

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
            continue  # no common ground at all, skip

        scores.append((score, int(loc_match), candidate, common))

    # Sort: primary = common interests (desc), secondary = location match (desc)
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