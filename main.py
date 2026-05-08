import sys
from profiles import add_user, get_profile, update_profile, all_users, preload_sample_data, user_exists
from graph import add_friend, remove_friend, get_friends, preload_sample_connections
from bfs_dfs import bfs_shortest_path, dfs_explore
from sorting import recommend_friends

W = 52

def divider():
    print("─" * W)

def header():
    print("\n" + "=" * W)
    print("      SOCIAL NETWORK EXPLORER  (SNE)")
    print("=" * W)

def menu():
    divider()
    print("  PROFILES")
    print("   1. Add User")
    print("   2. View Profile")
    print("   3. Update Profile")
    print("   4. List All Users")
    print("  NETWORK")
    print("   5. Add Friendship")
    print("   6. Remove Friendship")
    print("   7. Show Friends of a User")
    print("  ALGORITHMS")
    print("   8. BFS — Shortest Path")
    print("   9. DFS — Explore Friends-of-Friends")
    print("  DISCOVERY")
    print("  10. Friend Recommendations")
    print("   0. Exit")
    divider()

def ask(prompt):
    try:
        return input(f"  {prompt}: ").strip()
    except (EOFError, KeyboardInterrupt):
        print("\n\n  Goodbye!")
        sys.exit(0)

def handle_add_user():
    print("\n  [ ADD USER ]")
    username  = ask("Username")
    name      = ask("Full name")
    age       = ask("Age")
    interests = ask("Interests (comma-separated)")
    location  = ask("Location (optional, press Enter to skip)")
    ok, msg = add_user(username, name, age, interests, location)
    print(f"\n  {'✅' if ok else '❌'} {msg}")

def handle_view_profile():
    print("\n  [ VIEW PROFILE ]")
    username = ask("Username")
    profile, err = get_profile(username)
    if err:
        print(f"\n  ❌ {err}")
        return
    friends, _ = get_friends(username)
    print(f"\n  {'─'*30}")
    print(f"  👤  {profile['name']}  (@{username})")
    print(f"  {'─'*30}")
    print(f"  Age       : {profile['age']}")
    print(f"  Location  : {profile['location'] or '—'}")
    print(f"  Interests : {', '.join(profile['interests'])}")
    print(f"  Friends   : {', '.join(friends) if friends else 'None yet'}")
    print(f"  {'─'*30}")

def handle_update_profile():
    print("\n  [ UPDATE PROFILE ]")
    username = ask("Username")
    print("  Fields: name | age | interests | location")
    key   = ask("Field to update")
    value = ask("New value")
    ok, msg = update_profile(username, key, value)
    print(f"\n  {'✅' if ok else '❌'} {msg}")

def handle_list_users():
    print("\n  [ ALL USERS ]")
    users = all_users()
    if not users:
        print("  No users yet.")
        return
    print(f"\n  Total users: {len(users)}")
    divider()
    for i, u in enumerate(users, 1):
        p, _ = get_profile(u)
        print(f"  {i:2}. @{u:<10}  {p['name']}")

def handle_add_friend():
    print("\n  [ ADD FRIENDSHIP ]")
    u1 = ask("User 1")
    u2 = ask("User 2")
    ok, msg = add_friend(u1, u2)
    print(f"\n  {'✅' if ok else '❌'} {msg}")

def handle_remove_friend():
    print("\n  [ REMOVE FRIENDSHIP ]")
    u1 = ask("User 1")
    u2 = ask("User 2")
    ok, msg = remove_friend(u1, u2)
    print(f"\n  {'✅' if ok else '❌'} {msg}")

def handle_show_friends():
    print("\n  [ SHOW FRIENDS ]")
    username = ask("Username")
    friends, err = get_friends(username)
    if err and not friends:
        print(f"\n  ❌ {err}")
        return
    print(f"\n  Friends of @{username} ({len(friends)} total):")
    divider()
    for f in friends:
        p, _ = get_profile(f)
        label = p['name'] if p else f
        print(f"    • @{f:<12}  {label}")

def handle_bfs():
    print("\n  [ BFS — SHORTEST PATH ]")
    src = ask("Source user")
    dst = ask("Destination user")

    if not user_exists(src):
        print(f"\n  ❌ User '{src}' not found.")
        return
    if not user_exists(dst):
        print(f"\n  ❌ User '{dst}' not found.")
        return

    print(f"\n  🔍 Finding shortest path: @{src} → @{dst} ...")
    path, result = bfs_shortest_path(src, dst)

    if path is None:
        print(f"\n  ❌ {result}")
        return

    arrow_path = "  →  ".join([f"@{u}" for u in path])
    print(f"\n  Path   : {arrow_path}")
    print(f"  Degrees of separation : {result}")

def handle_dfs():
    print("\n  [ DFS — FRIENDS-OF-FRIENDS EXPLORATION ]")
    src   = ask("Starting user")
    depth = ask("Exploration depth (e.g. 2 or 3)")

    if not user_exists(src):
        print(f"\n  ❌ User '{src}' not found.")
        return

    try:
        depth = int(depth)
        if depth < 1:
            raise ValueError
    except ValueError:
        print("\n  ❌ Depth must be a positive integer.")
        return

    result, err = dfs_explore(src, depth)

    if err:
        print(f"\n  ❌ {err}")
        return

    total = sum(len(v) for v in result.values())
    print(f"\n  🌐 DFS from @{src} (depth={depth}):")
    divider()

    if not result:
        print("  No users discovered within this depth.")
        return

    for d in range(1, depth + 1):
        users_at_d = result.get(d, [])
        label = f"  Depth {d}"
        if users_at_d:
            print(f"{label} : {', '.join(['@' + u for u in users_at_d])}")
        else:
            print(f"{label} : (none)")

    divider()
    print(f"  Total users discovered : {total}")

def handle_recommendations():
    print("\n  [ FRIEND RECOMMENDATIONS ]")
    username = ask("Username")

    if not user_exists(username):
        print(f"\n  ❌ User '{username}' not found.")
        return

    recs, err = recommend_friends(username)

    if err:
        print(f"\n  ❌ {err}")
        return

    print(f"\n  💡 Recommendations for @{username}:")
    divider()

    if not recs:
        print("  No recommendations available right now.")
        return

    for i, r in enumerate(recs, 1):
        common_str = ", ".join(r["common"]) if r["common"] else "none"
        loc_tag    = "  📍 same city" if r["location_match"] else ""
        print(f"  {i}. @{r['username']:<12} {r['name']}")
        print(f"       Common interests ({r['score']}): {common_str}{loc_tag}")

    divider()

def main():
    header()
    print("\n  Loading sample data...")
    preload_sample_data()
    preload_sample_connections()
    print("  ✅ 8 users and 10 friendships loaded.\n")

    actions = {
        "1":  handle_add_user,
        "2":  handle_view_profile,
        "3":  handle_update_profile,
        "4":  handle_list_users,
        "5":  handle_add_friend,
        "6":  handle_remove_friend,
        "7":  handle_show_friends,
        "8":  handle_bfs,
        "9":  handle_dfs,
        "10": handle_recommendations,
    }

    while True:
        menu()
        choice = ask("Enter choice")
        if choice == "0":
            print("\n  Goodbye! 👋\n")
            break
        elif choice in actions:
            actions[choice]()
        else:
            print("\n  ❌ Invalid choice. Please enter a number from the menu.")

        input("\n  Press Enter to continue...")

if __name__ == "__main__":
    main()