<div align="center">

# 🌐 Social Network Explorer (SNE)
**A comprehensive Python-based command-line social network simulator with graph search algorithms and a friend recommendation system.**

[![Python](https://img.shields.io/badge/Python-3.x-blue.svg)](https://python.org)
[![Project](https://img.shields.io/badge/Project-Social_Network_Explorer-purple.svg)]()
[![Status](https://img.shields.io/badge/Status-Completed-success.svg)]()

</div>

---

## 👨‍🎓 Student Profile

| Attribute | Details |
| :--- | :--- |
| **Name** | Harsh Dev Jha |
| **Roll No.** | 2501010168 |
| **Course** | Btech CSE Core |
| **Section** | A |

---

## 📑 Table of Contents
- [Project Overview](#-project-overview)
- [Key Features](#-key-features)
- [System Architecture](#-system-architecture)
- [Project Structure](#-project-structure)
- [How to Run](#-how-to-run)
- [Testing & Validation](#-testing--validation)
- [Complexity Analysis](#-complexity-analysis)

---

## 🌐 Project Overview
The **Social Network Explorer (SNE)** is a command-line tool designed to model a social network graph. It allows users to register, update, and manage profiles, add and remove connections (undirected friendships), search degrees of separation using BFS, explore deeper networks recursively with DFS, and get tailored friends recommendations powered by shared interests and geographic closeness.

---

## 🚀 Key Features

### 👤 1. Profile Management
- **Add User:** Register new users with detailed profile information (Full Name, Age, Interests, Location).
- **View Profile:** Look up profile details along with their current friends list.
- **Update Profile:** Dynamically update fields such as age, location, and interests.

### 👥 2. Network Topology (Graph)
- **Establish Friendships:** Form undirected, unweighted links between users.
- **Remove Friendships:** Remove links dynamically.
- **Efficient Adjacency List:** Graph implementation leverages Python `dict` of `set` structures for $O(1)$ lookup and modification.

### 🔍 3. Network Search & Exploration (BFS & DFS)
- **Shortest Path (BFS):** Find the minimum degrees of separation and trace the path of connection between any two users.
- **Bounded Exploration (DFS):** Recursively crawl the network from a starting node to discover friends-of-friends up to a user-specified depth $d$.

### 💡 4. Smart Recommendation Engine
- **Interest and Location Matching:** Generates tailored recommendations by excluding current friends and scoring potential matches based on set intersections of common interests and geographic proximity.
- **Timsort Ranking:** Candidates are ranked using Python's highly optimized Timsort, ensuring that users with the highest shared affinity appear first.

---

## 📂 Project Structure

```text
ds-capstone_Social-Network-Explorer/
├── main.py              # CLI interactive menu application
├── graph.py             # Network topology operations (Adjacency List)
├── profiles.py          # Hash-map based user profile storage
├── bfs_dfs.py           # Breadth-First & Depth-First Search algorithms
├── sorting.py           # Multi-criteria recommendation sorting engine
├── recommendations.py   # Recommendation scoring core logic
├── test_cases.py        # Comprehensive test runner suite
├── output.txt           # Console output record of passing tests
└── report.md            # Concept design and complexity report
```

---

## 💻 How to Run

### Interactive Console App
Run the interactive CLI application to manually add profiles, create connections, search paths, and see recommendations in real-time:
```bash
python main.py
```
*A preloaded sample of 8 users and 10 friendships will be imported automatically upon startup.*

---

## 🧪 Testing & Validation

The project is backed by a robust suite of 35 test cases validating every system boundary (adding duplicates, edge BFS/DFS traversal bounds, and recommendation scoring).

To execute the tests:
```bash
python test_cases.py
```

### Expected Output
Upon successful execution, you should see the following console output confirming a 100% pass rate:
```text
──────────────────────────────────────────────────
  1. PROFILES — add / get / update
──────────────────────────────────────────────────
  ✅ PASS  Add new user 'zara'
  ✅ PASS  Duplicate user rejected
  ✅ PASS  Get existing profile (alice)
  ✅ PASS  Get non-existent profile returns error
  ✅ PASS  Update alice's age
  ✅ PASS  Alice age is now 22
  ✅ PASS  Update alice's interests
  ✅ PASS  Interests stored as list
  ✅ PASS  Update non-existent user returns error

──────────────────────────────────────────────────
  2. GRAPH — add / remove / list friendships
──────────────────────────────────────────────────
  ✅ PASS  Add friendship zara-alice
  ✅ PASS  Zara's friends include alice
  ✅ PASS  Friendship is undirected (alice has zara)
  ✅ PASS  Self-friendship rejected
  ✅ PASS  Duplicate friendship rejected
  ✅ PASS  Remove alice-carol friendship
  ✅ PASS  Carol no longer in alice's friends
  ✅ PASS  Remove non-existent friendship returns error

──────────────────────────────────────────────────
  3. BFS — Shortest Path
──────────────────────────────────────────────────
  ✅ PASS  BFS: alice to bob (direct friend)
  ✅ PASS  BFS path starts at alice, ends at bob
  ✅ PASS  BFS: alice to dave (2 hops)
  ✅ PASS  BFS: alice to henry (3 hops)
  ✅ PASS  BFS: same src and dst returns 0 degrees
  ✅ PASS  BFS: zara to henry via alice chain

──────────────────────────────────────────────────
  4. DFS — Friends-of-Friends Exploration
──────────────────────────────────────────────────
  ✅ PASS  DFS depth=1 returns alice's direct friends
  ✅ PASS  DFS depth=1 includes bob
  ✅ PASS  DFS depth=2 discovers deeper users
  ✅ PASS  DFS depth=3 discovers more users than depth=2
  ✅ PASS  DFS on unknown user returns error

──────────────────────────────────────────────────
  5. RECOMMENDATIONS — ranked by common interests
──────────────────────────────────────────────────
  ✅ PASS  Recommendations returned for alice
  ✅ PASS  At least 1 recommendation
  ✅ PASS  Alice not in her own recommendations
  ✅ PASS  Direct friends excluded from recs
  ✅ PASS  Recommendations sorted by common interests (desc)
  ✅ PASS  Rec entry has all required keys
  ✅ PASS  Recs for unknown user returns error

==================================================
  RESULTS:  35 passed   0 failed   (35/35)
==================================================
```

---

## 📝 Complexity Analysis

| Operation | Component | Time Complexity | Space Complexity | Notes |
| :--- | :--- | :--- | :--- | :--- |
| **Add/Get/Update User** | `profiles.py` | $O(1)$ | $O(1)$ | Dictionary access is $O(1)$ average. Total space: $O(U)$ where $U$ is number of users. |
| **Add/Remove Friend** | `graph.py` | $O(1)$ | $O(1)$ | Set operations (add/discard) are $O(1)$ average. Total space: $O(U + E)$ where $E$ is number of friendships. |
| **Shortest Path** | `bfs_dfs.py` (BFS) | $O(V + E)$ | $O(V)$ | Where $V$ is reachable users and $E$ is connections between them. Visited set takes $O(V)$ space. |
| **Explore Network (Depth d)** | `bfs_dfs.py` (DFS) | $O(V + E)$ | $O(V)$ | Bounded recursively by max depth $d$. |
| **Friend Recommendations** | `sorting.py` | $O(U \cdot I + U \log U)$ | $O(U)$ | Where $U$ is candidates, $I$ is number of interests. Scoring is $O(U \cdot I)$. Sorting candidate scores is $O(U \log U)$. |

---

*This project is completed and ready for evaluation.*
