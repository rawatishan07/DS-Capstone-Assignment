import sys
sys.path.insert(0, ".")

from profiles import add_user, get_profile, update_profile, preload_sample_data, users
from graph    import add_friend, remove_friend, get_friends, preload_sample_connections, network
from bfs_dfs  import bfs_shortest_path, dfs_explore
from sorting import recommend_friends

PASS = "✅ PASS"
FAIL = "❌ FAIL"

passed = 0
failed = 0

def check(label, condition):
    global passed, failed
    if condition:
        print(f"  {PASS}  {label}")
        passed += 1
    else:
        print(f"  {FAIL}  {label}")
        failed += 1

def section(title):
    print(f"\n{'─'*50}")
    print(f"  {title}")
    print(f"{'─'*50}")

preload_sample_data()
preload_sample_connections()

section("1. PROFILES — add / get / update")

ok, _ = add_user("zara", "Zara Khan", 20, "coding, art", "Delhi")
check("Add new user 'zara'", ok)

ok2, _ = add_user("zara", "Duplicate", 20, "coding", "")
check("Duplicate user rejected", not ok2)

profile, err = get_profile("alice")
check("Get existing profile (alice)", profile is not None and err is None)

_, err2 = get_profile("ghost")
check("Get non-existent profile returns error", err2 is not None)

ok3, _ = update_profile("alice", "age", "22")
check("Update alice's age", ok3)
check("Alice age is now 22", users["alice"]["age"] == "22")

ok4, _ = update_profile("alice", "interests", "music, dance, coding")
check("Update alice's interests", ok4)
check("Interests stored as list", isinstance(users["alice"]["interests"], list))

_, err3 = update_profile("ghost", "age", "25")
check("Update non-existent user returns error", err3 is not None)

section("2. GRAPH — add / remove / list friendships")

ok, _ = add_friend("zara", "alice")
check("Add friendship zara-alice", ok)

friends, _ = get_friends("zara")
check("Zara's friends include alice", "alice" in friends)

friends_alice, _ = get_friends("alice")
check("Friendship is undirected (alice has zara)", "zara" in friends_alice)

ok2, _ = add_friend("alice", "alice")
check("Self-friendship rejected", not ok2)

ok3, _ = add_friend("alice", "bob")
check("Duplicate friendship rejected", not ok3)

ok_rm, _ = remove_friend("alice", "carol")
check("Remove alice-carol friendship", ok_rm)

friends_after, _ = get_friends("alice")
check("Carol no longer in alice's friends", "carol" not in friends_after)

_, err_rm = remove_friend("alice", "carol")
check("Remove non-existent friendship returns error", err_rm is not None)

section("3. BFS — Shortest Path")

path, deg = bfs_shortest_path("alice", "bob")
check("BFS: alice to bob (direct friend)", path is not None and deg == 1)
check("BFS path starts at alice, ends at bob",
      path is not None and path[0] == "alice" and path[-1] == "bob")

path2, deg2 = bfs_shortest_path("alice", "dave")
check("BFS: alice to dave (2 hops)", path2 is not None and deg2 == 2)

path3, deg3 = bfs_shortest_path("alice", "henry")
check("BFS: alice to henry (3 hops)", path3 is not None and deg3 == 3)

path4, deg4 = bfs_shortest_path("bob", "bob")
check("BFS: same src and dst returns 0 degrees", deg4 == 0)

path5, _ = bfs_shortest_path("zara", "henry")
check("BFS: zara to henry via alice chain", path5 is not None)

section("4. DFS — Friends-of-Friends Exploration")

result, err = dfs_explore("alice", 1)
check("DFS depth=1 returns alice's direct friends", err is None and 1 in result)

depth1_users = result.get(1, [])
check("DFS depth=1 includes bob", "bob" in depth1_users)

result2, _ = dfs_explore("alice", 2)
depth2_users = result2.get(2, [])
check("DFS depth=2 discovers deeper users", len(depth2_users) > 0)

result3, _ = dfs_explore("alice", 3)
total = sum(len(v) for v in result3.values())
check("DFS depth=3 discovers more users than depth=2",
      total > sum(len(v) for v in result2.values()))

_, err2 = dfs_explore("nobody", 2)
check("DFS on unknown user returns error", err2 is not None)

section("5. RECOMMENDATIONS — ranked by common interests")

recs, err = recommend_friends("alice")
check("Recommendations returned for alice", err is None and recs is not None)
check("At least 1 recommendation", len(recs) > 0)

direct_friends, _ = get_friends("alice")
rec_names = [r["username"] for r in recs]
check("Alice not in her own recommendations", "alice" not in rec_names)
check("Direct friends excluded from recs",
      all(f not in rec_names for f in direct_friends))

scores = [r["score"] for r in recs]
check("Recommendations sorted by common interests (desc)",
      scores == sorted(scores, reverse=True))

if recs:
    r = recs[0]
    check("Rec entry has all required keys",
          all(k in r for k in ["username", "name", "common", "score", "location_match"]))

_, err2 = recommend_friends("nobody")
check("Recs for unknown user returns error", err2 is not None)

print(f"\n{'='*50}")
print(f"  RESULTS:  {passed} passed   {failed} failed   "
      f"({passed}/{passed+failed})")
print(f"{'='*50}\n")