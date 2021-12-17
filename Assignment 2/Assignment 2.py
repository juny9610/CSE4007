import math
import copy

#disjoint set
class DisjointSet:
    def __init__(self, n):
        self.data = list(range(n))
        self.size = n

    def find(self, index):
        return self.data[index]
        
    def union(self, x, y):
        x = self.find(x)
        y = self.find(y)

        if x == y: return

        for i in range(self.size):
            if x <= y and self.find(i) == y:
                self.data[i] = x
            elif x > y and self.find(i) == x:
                self.data[i] = y

    def get_list(self, num):
        tmp = self.find(num)
        arr = []
        for i in range(self.size):
            if tmp == self.data[i]:
                arr.append(i)

        return arr 

    def length(self):
        return len(set(self.data))                

#file read 
def file_read(file_name):
    file = open(file_name, "r")
    k, n = map(int, file.readline().split())
    xy = [[0 for x in range(2)] for y in range(n)]

    index = 0
    while True:
        line = file.readline().strip("\n")
        if not line: break
        xy[index] = list(map(int, line.split(",")))
        index += 1

    file_name = file_name[:-4]
    file.close()

    return xy, file_name

#file write
def file_write(file_name, clusters, span, k):
    file = open(file_name + "_output.txt", "a")
    file.write("---\n" + k + "\n" + "clusters: ")
    for i in range(len(clusters)):
        file.write("[" + "," .join(map(str, clusters[i])) + "]")
    file.write("\nspan: {}, {}\n" .format(span[0], span[1]))

    file.close()

#cosine similarity
def cosine_similarity(A, B):
    multiple_xx = 0
    multiple_xy = 0
    multiple_yy = 0
    for i in range(len(A)):
        x = A[i]
        y = B[i]
        multiple_xx += x*x
        multiple_xy += x*y
        multiple_yy += y*y
    
    return multiple_xy / math.sqrt(multiple_xx * multiple_yy)

#single link clustering
def single_link_clustering(xy):
    arr = copy.deepcopy(xy)
    length = len(arr)
    span = [-2, -2]
    clusters = DisjointSet(length)

    while clusters.length() >= 3:
        max_span, obj1, obj2 = 0, 0, 0

        for i in range(len(arr)):
            for j in range(i+1, len(arr)):
                if max_span < arr[i][j]:
                    max_span = arr[i][j]
                    obj1, obj2 = i, j
        span[0] = span[1]
        span[1] = max_span

        if clusters.length() == 3: break
        clusters.union(obj1, obj2)

        for i in range(len(arr)):
            if obj1 != i:
                arr[obj1][i] = max(arr[obj1][i], arr[obj2][i])
                arr[i][obj1] = arr[obj1][i]
            arr[obj2][i] = -2
            arr[i][obj2] = -2

    return clusters, span

#complete link clustering
def complete_link_clustering(xy):
    arr = copy.deepcopy(xy)
    length = len(arr)
    span = [-2, -2]
    clusters = DisjointSet(length)

    while clusters.length() >= 3:
        max_span, obj1, obj2 = -2, 0, 0

        for i in range(len(arr)):
            for j in range(i+1, len(arr)):
                if max_span < arr[i][j]:
                    max_span = arr[i][j]
                    obj1, obj2 = i, j
        span[0] = span[1]
        span[1] = max_span

        if clusters.length() == 3: break
        clusters.union(obj1, obj2)

        arr[obj1][obj2] = -2
        arr[obj2][obj1] = -2

        for i in range(len(arr)):
            if obj1 != i:
                arr[obj1][i] = min(arr[obj1][i], arr[obj2][i])
                arr[i][obj1] = arr[obj1][i]
            arr[obj2][i] = -2
            arr[i][obj2] = -2

    return clusters, span

#group average link clustering
def average_link_clustering(xy):
    arr = [[-2 for x in range(len(xy))] for y in range(len(xy))]
    for i in range(len(xy)):
        for j in range(len(xy)):
            if i == j: continue
            arr[i][j] = cosine_similarity(xy[i], xy[j])

    length = len(xy)
    span = [-2, -2]
    clusters = DisjointSet(length)

    while clusters.length() >= 3:
        max_span, obj1, obj2 = -2, 0, 0

        for i in range(len(arr)):
            for j in range(i+1, len(arr)):
                if max_span < arr[i][j]:
                    max_span = arr[i][j]
                    obj1, obj2 = i, j
        span[0] = span[1]
        span[1] = max_span

        if clusters.length() == 3: break
        clusters.union(obj1, obj2)

        arr[obj1][obj2] = -2
        arr[obj2][obj1] = -2

        for i in range(len(arr)):
            if obj1 != i and arr[obj1][i] != -2:
                if clusters.find(obj1) == clusters.find(i): continue

                list1 = clusters.get_list(obj1)
                list2 = clusters.get_list(i)
                arr[obj1][i] = 0

                for j in list1:
                    for k in list2:
                        arr[obj1][i] += cosine_similarity(xy[j], xy[k])
                arr[obj1][i] = arr[obj1][i] / (len(list1) * len(list2))
                arr[i][obj1] = arr[obj1][i]

            arr[obj2][i] = -2
            arr[i][obj2] = -2

    return clusters, span

#make_xy
def make_xy(clusters, xy):
    obj1, obj2, obj3, count = -1, -1, -1, 0

    for i in set(clusters.data):
        if count == 0: obj1 = i
        elif count == 1: obj2 = i
        elif count == 2: obj3 = i
        count += 1

    arr = [[], [], []]
    for i in range(len(clusters.data)):
        index = 0
        if clusters.data[i] == obj1: index = 0
        elif clusters.data[i] == obj2: index = 1
        elif clusters.data[i] == obj3: index = 2
        arr[index].append((xy[i][0], xy[i][1]))
    
    return arr

#clustering
def clustering(xy, file_name):
    file = open(file_name + "_output.txt", "a")
    k = file_name[file_name.find('_') + 1:]
    file.write(k + '\n')
    file.close()

    arr = [[-2 for x in range(len(xy))] for y in range(len(xy))]
    for i in range(len(xy)):
        for j in range(len(xy)):
            if i == j: continue
            arr[i][j] = cosine_similarity(xy[i], xy[j])

    cluster, span = single_link_clustering(arr)
    clusters = make_xy(cluster, xy)
    file_write(file_name, clusters, span, "single")

    cluster, span = complete_link_clustering(arr)
    clusters = make_xy(cluster, xy)
    file_write(file_name, clusters, span, "complete")

    cluster, span = average_link_clustering(xy)
    clusters = make_xy(cluster, xy)
    file_write(file_name, clusters, span, "average")

#main
for i in range(1,4):
    print("CoordinatePlane_%d..\nLoading..\n" %i)
    xy, file_name = file_read("CoordinatePlane_%d.txt" %i)
    clustering(xy, file_name)
    print("CoordinatePlane_%d is finished\n" %i)