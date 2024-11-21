import heapq
import math

# 定義節點類
class Node:
    def __init__(self, x, y, cost=0, heuristic=0, parent=None):
        self.x = x
        self.y = y
        self.cost = cost  # g(n)
        self.heuristic = heuristic  # h(n)
        self.parent = parent
    
    # 兩個節點相等的條件
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    
    # 比較節點優先級（用於優先級隊列）
    def __lt__(self, other):
        return (self.cost + self.heuristic) < (other.cost + other.heuristic)
    
    # 獲取當前節點的 f(n) 值
    def f(self):
        return self.cost + self.heuristic

# A* 演算法主體
def a_star(grid, start, end):
    # 優先級隊列（open list）
    open_list = []
    closed_list = set()  # 已訪問節點
    
    # 初始化起點節點
    start_node = Node(start[0], start[1], 0, heuristic(start, end))
    heapq.heappush(open_list, start_node)
    
    while open_list:
        # 取出當前 f(n) 最小的節點
        current_node = heapq.heappop(open_list)
        
        # 如果到達終點
        if current_node == Node(end[0], end[1]):
            return reconstruct_path(current_node)
        
        # 將當前節點加入 closed list
        closed_list.add((current_node.x, current_node.y))
        
        # 檢查相鄰節點
        neighbors = get_neighbors(current_node, grid)
        for neighbor in neighbors:
            # 如果鄰居節點已在 closed list 中，跳過
            if (neighbor.x, neighbor.y) in closed_list:
                continue
            
            # 計算鄰居節點的 g(n)
            tentative_cost = current_node.cost + 1  # 假設所有移動的代價為1
            
            # 如果鄰居不在 open list 中，或新的 g(n) 更小，則更新
            in_open_list = False
            for open_node in open_list:
                if neighbor == open_node and tentative_cost < open_node.cost:
                    open_list.remove(open_node)
                    in_open_list = True
            
            if not in_open_list:
                neighbor.cost = tentative_cost
                neighbor.heuristic = heuristic((neighbor.x, neighbor.y), end)
                neighbor.parent = current_node
                heapq.heappush(open_list, neighbor)
    
    return None  # 如果找不到路徑

# 計算啟發函數（這裡使用曼哈頓距離）
def heuristic(node, end):
    return abs(node[0] - end[0]) + abs(node[1] - end[1])

# 獲取節點的相鄰節點
def get_neighbors(node, grid):
    neighbors = []
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # 上、右、下、左
    for direction in directions:
        new_x = node.x + direction[0]
        new_y = node.y + direction[1]
        if 0 <= new_x < len(grid) and 0 <= new_y < len(grid[0]) and grid[new_x][new_y] == 0:
            neighbors.append(Node(new_x, new_y))
    return neighbors

# 回溯找到完整路徑
def reconstruct_path(node):
    path = []
    while node:
        path.append((node.x, node.y))
        node = node.parent
    return path[::-1]  # 反轉路徑

# 測試用的網格 (0: 可行走, 1: 障礙)
grid = [
    [0, 1, 0, 0, 0],
    [0, 1, 0, 1, 0],
    [0, 0, 0, 1, 0],
    [0, 1, 1, 1, 0],
    [0, 0, 0, 0, 0]
]

start = (0, 0)  # 起點
end = (4, 4)  # 終點

# 呼叫 A* 演算法
path = a_star(grid, start, end)

# 打印結果
if path:
    print("找到的最短路徑: ", path)
else:
    print("找不到路徑")

#bitch
