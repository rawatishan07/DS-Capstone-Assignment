# Social Network Explorer (SNE) - Design & Complexity Report

**Name** - Rishita  
**Roll No.** - 2501010228  
**Course** - Btech CSE Core  
**Section** - A  

---

## Design Decisions

1. **Profiles (`profiles.py`)**:
   - **Data Structure**: A Hash Map (dictionary) is used to store user profiles `users = { username: profile_dict }`.
   - **Reasoning**: This provides O(1) average time complexity for adding, updating, and retrieving a user by their unique username. The list/set structure is used to store interests for flexibility and ease of manipulation.

2. **Network (`graph.py`)**:
   - **Data Structure**: An Adjacency List is implemented using a dictionary of sets `network = { username: set(friends) }`.
   - **Reasoning**: An adjacency list is much more space-efficient than an adjacency matrix for sparse graphs (like social networks). Using a `set` for a user's friends allows O(1) checks for existing friendships and O(1) addition/removal operations.

3. **Discovery & Exploration (`bfs_dfs.py`)**:
   - **BFS (Shortest Path)**: Breadth-First Search is the optimal algorithm for finding the shortest path (degrees of separation) in an unweighted graph. A `deque` from the `collections` module is used for O(1) queue push/pop operations.
   - **DFS (Friends-of-Friends)**: Depth-First Search is naturally suited to explore "depth" (e.g., exploring up to a specific depth `d`). It's implemented recursively and tracks discovered users grouped by depth level.

4. **Recommendations (`sorting.py`)**:
   - **Algorithm**: The recommendation engine uses set intersections to find common interests between a user and all other non-friends.
   - **Data Structures**: Sets are utilized to achieve O(min(len(s1), len(s2))) intersections. Sorting is done dynamically using Python's native Timsort based on a tuple `(common_interests_score, location_match)` to guarantee primary and secondary sorting order (a conceptual implementation of the Sorting and Geo DS bonus).

## Complexity Notes

| Operation | Component | Time Complexity | Space Complexity | Notes |
| :--- | :--- | :--- | :--- | :--- |
| **Add/Get/Update User** | Profiles | O(1) | O(1) | Dictionary access is O(1) average. Total space: O(U) where U is number of users. |
| **Add/Remove Friend** | Network | O(1) | O(1) | Set operations (add/discard) are O(1) average. Total space: O(U + E) where E is number of friendships. |
| **Shortest Path** | BFS | O(V + E) | O(V) | Where V is reachable users and E is connections between them. Visited set takes O(V) space. |
| **Explore Network (Depth d)** | DFS | O(V + E) | O(V) | Bounded by max depth `d`. |
| **Friend Recommendations** | Sorting | O(U * I + U log U) | O(U) | Where U is candidates, I is number of interests. Scoring is O(U * I). Sorting candidate scores is O(U log U). |
