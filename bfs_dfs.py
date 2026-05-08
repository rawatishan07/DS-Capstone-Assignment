from collections import deque
from graph import network, get_friends

def bfs_shortest_path(src, dst):
    if src not in network and dst not in network:
        return None, f"Neither '{src}' nor '{dst}' have any connections."
    if src not in network:
        return None, f"'{src}' has no connections."
    if src == dst:
        return [src], 0

    visited = {src}
    queue = deque([(src, [src])])

    while queue:
        current, path = queue.popleft()
        friends, _ = get_friends(current)

        for neighbor in friends:
            if neighbor == dst:
                full_path = path + [neighbor]
                return full_path, len(full_path) - 1
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))

    return None, f"No connection found between '{src}' and '{dst}'."

def dfs_explore(src, max_depth):
    if src not in network:
        return {}, f"'{src}' has no connections."

    visited = {src}
    result = {}

    def _dfs(node, depth):
        if depth > max_depth:
            return
        friends, _ = get_friends(node)
        for neighbor in friends:
            if neighbor not in visited:
                visited.add(neighbor)
                result.setdefault(depth, []).append(neighbor)
                _dfs(neighbor, depth + 1)

    _dfs(src, 1)
    return result, None