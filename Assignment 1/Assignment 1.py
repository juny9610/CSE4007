#Heap
class Heap:    
    def __init__(self):
        self.h = []
        self.size = 0

    def build(self, node):
        m = node
        if 2*node+1 < self.size and self.h[2*node+1][0] < self.h[m][0]:
            m = 2*node+1
        if 2*node+2 < self.size and self.h[2*node+2][0] < self.h[m][0]:
            m = 2*node+2
        if m != node:       
            self.h[node], self.h[m] = self.h[m], self.h[node]
            self.build(m)

    def insert(self, hu, x, y, depth): 
        self.h.append((hu,x,y,depth))
        cursize = self.size
        self.size += 1
        while (cursize-1)//2 >= 0 and self.h[cursize][0] < self.h[(cursize-1)//2][0]:
            temp = self.h[(cursize-1)//2]
            self.h[(cursize-1)//2] = self.h[cursize]
            self.h[cursize] = temp
            cursize = (cursize-1)//2

    def delete(self):
        cursize = self.size
        self.h[0] = self.h[cursize-1]
        self.size -= 1
        del self.h[cursize-1]
        self.build(0)

#distance
def distance(nx, ny, gx, gy):
    return abs(nx-gx) + abs(ny-gy)

#goal_xy
def goal_xy(goal):
    for i in range(int(m)):
        for j in range(int(n)):
            if arr[i][j] == goal:
                return (i,j)

#bfs
def bfs(x, y, goal):
    global arr, bfs_arr, dx, dy
    bfs_backtrack = [[0 for x in range(int(n))] for y in range(int(m))]
    for i in range(int(m)):
        for j in range(int(n)):
            bfs_backtrack[i][j] = -1

    queue = []
    queue.append((x,y))
    time = 0
    bfs_backtrack[x][y] = 4

    while len(queue) > 0:
        x = queue[0][0]
        y = queue[0][1]
        if arr[x][y] == goal:
            break
        del queue[0]
        time += 1

        for i in range(4):
            nx = x + dx[i]
            ny = y + dy[i]
            if nx < 0 or ny < 0 or nx >= int(m) or ny >= int(n):
                continue
            if (arr[nx][ny] == 2 or arr[nx][ny] == goal) and bfs_backtrack[nx][ny] == -1:
                queue.append((nx,ny))
                bfs_backtrack[nx][ny] = i

    rx = x
    ry = y
    length = 0
    while bfs_backtrack[rx][ry] < 4:
        length += 1
        bfs_arr[rx][ry] = 5
        for i in range(4):
            if bfs_backtrack[rx][ry] == i:
                rx = rx - dx[i]
                ry = ry - dy[i]
                break

    if goal == 4:
        bfs_arr[x][y] = goal
    return (x, y, time, length)

#ids
def ids(x, y, goal):
    global arr, ids_arr, dx, dy
    ids_backtrack = [[0 for x in range(int(n))] for y in range(int(m))]
    time = 0
    limit = 0

    while True:
        is_goal = 0
        stack = []
        stack.append((x,y,0))
        for i in range(int(m)):
            for j in range(int(n)):
                ids_backtrack[i][j] = -1
        ids_backtrack[x][y] = 4

        while len(stack) > 0:
            last = len(stack) - 1
            ix = stack[last][0]
            iy = stack[last][1]
            depth = stack[last][2]

            if arr[ix][iy] == goal:
                is_goal = 1
                break
            del stack[last]
            if depth == limit:
                continue
            time += 1

            for i in range(4):
                nx = ix + dx[i]
                ny = iy + dy[i]
                if nx < 0 or ny < 0 or nx >= int(m) or ny >= int(n):
                    continue
                if (arr[nx][ny] == 2 or arr[nx][ny] == goal) and ids_backtrack[nx][ny] == -1:
                    stack.append((nx,ny,depth+1))
                    ids_backtrack[nx][ny] = i

        if is_goal == 1:
            break
        limit += 1

    rx = ix
    ry = iy
    while ids_backtrack[rx][ry] < 4:
        ids_arr[rx][ry] = 5
        for i in range(4):
            if ids_backtrack[rx][ry] == i:
                rx = rx - dx[i]
                ry = ry - dy[i]
                break

    if goal == 4:
        ids_arr[ix][iy] = goal
    return (ix, iy, time, depth)

#gbfs
def gbfs(x, y, goal):
    global arr, gbfs_arr, dx, dy
    gbfs_backtrack = [[0 for x in range(int(n))] for y in range(int(m))]
    for i in range(int(m)):
        for j in range(int(n)):
            gbfs_backtrack[i][j] = -1

    heap = Heap()
    g_xy = goal_xy(goal)
    h = distance(x,y,g_xy[0],g_xy[1])
    heap.insert(h,x,y,0)
    time = 0
    gbfs_backtrack[x][y] = 4

    while heap.size > 0:
        x = heap.h[0][1]
        y = heap.h[0][2]
        depth = heap.h[0][3]
        if arr[x][y] == goal:
            break
        time += 1
        heap.delete()

        for i in range(4):
            nx = x + dx[i]
            ny = y + dy[i]
            if nx < 0 or ny < 0 or nx >= int(m) or ny >= int(n):
                continue
            if (arr[nx][ny] == 2 or arr[nx][ny] == goal) and gbfs_backtrack[nx][ny] == -1: 
                heap.insert(distance(nx,ny,g_xy[0],g_xy[1]),nx,ny,depth+1)
                gbfs_backtrack[nx][ny] = i

    rx = x
    ry = y
    while gbfs_backtrack[rx][ry] < 4:
        gbfs_arr[rx][ry] = 5
        for i in range(4):
            if gbfs_backtrack[rx][ry] == i:
                rx = rx - dx[i]
                ry = ry - dy[i]
                break

    if goal == 4:
        gbfs_arr[x][y] = goal
    return (x, y, time, depth)

#a_star
def a_star(x, y, goal):
    global arr, a_star_arr, dx, dy
    a_star_backtrack = [[0 for x in range(int(n))] for y in range(int(m))]
    for i in range(int(m)):
        for j in range(int(n)):
            a_star_backtrack[i][j] = -1

    heap = Heap()
    g_xy = goal_xy(goal)
    h = distance(x,y,g_xy[0],g_xy[1])
    heap.insert(0+h,x,y,0)
    time = 0
    a_star_backtrack[x][y] = 4

    while heap.size > 0:
        x = heap.h[0][1]
        y = heap.h[0][2]
        depth = heap.h[0][3]
        if arr[x][y] == goal:
            break
        time += 1
        heap.delete()

        for i in range(4):
            nx = x + dx[i]
            ny = y + dy[i]
            if nx < 0 or ny < 0 or nx >= int(m) or ny >= int(n):
                continue
            if (arr[nx][ny] == 2 or arr[nx][ny] == goal) and a_star_backtrack[nx][ny] == -1:
                heap.insert(distance(nx,ny,g_xy[0],g_xy[1])+depth,nx,ny,depth+1)
                a_star_backtrack[nx][ny] = i

    rx = x
    ry = y
    while a_star_backtrack[rx][ry] < 4:
        a_star_arr[rx][ry] = 5
        for i in range(4):
            if a_star_backtrack[rx][ry] == i:
                rx = rx - dx[i]
                ry = ry - dy[i]
                break

    if goal == 4:
        a_star_arr[x][y] = goal
    return (x,y,time,depth)

#maze_print
def maze_print(k, time, length, algorithm, arr):
    file = open("Maze_%d_" %int(k) + algorithm +"_output.txt", "w")
    
    for i in range(int(m)):
        for j in range(int(n)):
            file.write(str(arr[i][j]))
        file.write('\n')      

    file.write('---\n' )
    file.write('length=%d\n' %length)
    file.write('time=%d\n' %time)
    file.close()
    
#main
maze_number = int(input("Input Maze's Number : "))
file = open("Maze_%d.txt" %maze_number, "r")
k,m,n = file.readline().split()
maze_input = file.readlines()
file.close()
print("program start")
print("loading...")

global arr, bfs_arr, ids_arr, gbfs_arr, a_star_arr, dx, dy
arr = [[0 for x in range(int(n))] for y in range(int(m))]
bfs_arr = [[0 for x in range(int(n))] for y in range(int(m))]
ids_arr = [[0 for x in range(int(n))] for y in range(int(m))]
gbfs_arr = [[0 for x in range(int(n))] for y in range(int(m))]
a_star_arr = [[0 for x in range(int(n))] for y in range(int(m))]
dx = [1,-1,0,0]
dy = [0,0,1,-1]

i = 0
for x in maze_input:
    j = 0
    for y in x:
        if y != '\n':
            arr[i][j] = int(y)
        j += 1
    i += 1

for i in range(int(m)):
    for j in range(int(n)):
        bfs_arr[i][j] = arr[i][j]
        ids_arr[i][j] = arr[i][j]
        gbfs_arr[i][j] = arr[i][j]
        a_star_arr[i][j] = arr[i][j]

for i in range(int(m)):
    for j in range(int(n)):
        if arr[i][j] == 3:
            #bfs
            print("bfs start")
            bfs_key = bfs(i,j,6)
            bfs_time = bfs_key[2]
            bfs_length = bfs_key[3]

            bfs_goal = bfs(bfs_key[0], bfs_key[1], 4)
            bfs_time += bfs_goal[2]
            bfs_length += bfs_goal[3]
            print("bfs end")

            #ids
            print("ids start")
            ids_key = ids(i, j, 6)
            ids_time = ids_key[2]
            ids_length = ids_key[3]

            ids_goal = ids(ids_key[0], ids_key[1], 4)
            ids_time += ids_goal[2]
            ids_length += ids_goal[3]
            print("ids end")

            #gbfs
            print("gbfs start")
            gbfs_key = gbfs(i, j, 6)
            gbfs_time = gbfs_key[2]
            gbfs_length = gbfs_key[3]

            gbfs_goal = gbfs(gbfs_key[0], gbfs_key[1], 4)
            gbfs_time += gbfs_goal[2]
            gbfs_length += gbfs_goal[3]
            print("gbfs end")

            #a_star
            print("a_star start")
            a_star_key = a_star(i, j, 6)
            a_star_time = a_star_key[2]
            a_star_length = a_star_key[3]

            a_star_goal = a_star(a_star_key[0], a_star_key[1], 4)
            a_star_time += a_star_goal[2]
            a_star_length += a_star_goal[3]
            print("a_star end")
            
            print("program end")
            break
    
    maze_print(k, bfs_time, bfs_length, "BFS", bfs_arr)
    maze_print(k ,ids_time, ids_length, "IDS", ids_arr)
    maze_print(k, gbfs_time, gbfs_length, "GBFS", gbfs_arr)
    maze_print(k, a_star_time, a_star_length, "A_star", a_star_arr)
