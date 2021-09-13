import copy

N = int(input("Please input N:"))
C = int(input("Please input C:"))


class LState:  # 左岸状态类
    def __init__(self, m, w, b):
        self.m = m  # 左岸传教士人数(missionary
        self.w = w  # 左岸野人人数(wild
        self.b = b  # 船在左岸为1，在右岸为0
        self.parent = []
        self.son = []

    def equal(self, s):  # 判断状态是否相等
        if self.m == s.m and self.w == s.w and self.b == s.b:
            return True
        else:
            return False

    def number(self):  # 返回状态字符串
        return str(self.m) + str(self.w) + str(self.b)


class Operate:  # 操作类
    def __init__(self, m, w):
        self.m = m
        self.w = w


all_operate = []  # 所有可能的操作


def make_all_operate():  # 生成所有可能的操作
    for i in range(N + 1):
        for j in range(N + 1):
            if i == 0 and j == 0:
                continue
            if i == 0:
                if j <= C:
                    temp = Operate(i, j)
                    all_operate.append(temp)
            else:
                if (i + j) <= C and i >= j:
                    temp = Operate(i, j)
                    all_operate.append(temp)


def safe(s):  # 判断该状态是否安全
    if s.m < 0 or s.m > N or s.w < 0 or s.w > N:
        return False
    else:
        # 左岸和右岸的传教士都要多于野人
        if s.m == N or s.m == 0:
            return True
        if s.m >= s.w and N - s.m >= N - s.w:
            return True
        else:
            return False


def find_next(node):  # 寻找下一个状态
    result = []
    for i in all_operate:
        temp = copy.deepcopy(node)
        temp.parent.clear()
        if node.b == 1:  # 船在左边
            if i.m <= node.m and i.w <= node.w:  # 判断操作是否合理
                temp.m -= i.m
                temp.w -= i.w
                temp.b -= 1
            else:
                continue
        else:  # 船在右边
            if i.m <= N - node.m and i.w <= N - node.w:  # 判断操作是否合理
                temp.m += i.m
                temp.w += i.w
                temp.b += 1
            else:
                continue

        check = 1
        for j in node.parent:  # 去除父节点
            if temp.number() == j.number():
                check = 0
        if safe(temp) and check != 0:  # 生成的节点安全
            result.append(temp)

    return result


def check_back(node, check_node, check):  # 递归检查父节点
    temp_node = node
    if node.equal(check_node):
        check = 1
        return None
    if len(temp_node.parent) != 0:
        if len(temp_node.parent) == 1:
            if temp_node.parent[0].equal(check_node):
                check = 1
                return None
            check_back(temp_node.parent[0], check_node, check)
        else:
            for i in temp_node.parent:
                check_back(i, check_node, check)
    return None


def show_path(node, path):  # 递归展示路径
    temp_node = node
    path.append(node.number())
    if len(temp_node.parent) != 0:
        if len(temp_node.parent) == 1:
            show_path(temp_node.parent[0], path)
        else:
            for i in temp_node.parent:
                temp_path = copy.deepcopy(path)
                show_path(i, temp_path)

    path.reverse()
    if path[0] == str(N) + str(N) + str(1) and path[-1] == "000":
        print("Optimal Procedure:", end="")
        for i in path:
            print(i, end="")
            if i != path[-1]:
                print("->", end="")
            else:
                print()
    return None


def expand_node(open, close, M):  # 扩展节点
    check_right = 0
    for i in open:
        close.append(i)
    open.clear()
    for i in close:
        temp = find_next(i)  # 可生成的合法节点
        for j in temp:
            # 判断可生成的节点是否出现过
            if j.number() not in M:  # 没出现过则加入扩展节点
                i.son.append(j)
                j.parent.append(i)
                if j.m == 0 and j.w == 0 and j.b == 0:  # 000出现
                    path = []
                    show_path(j, path)
                    check_right = 1
                    continue
                else:
                    M[j.number()] = j
                    open.append(j)
            else:
                check = 0  # 判断是否在父节点出现过
                check_back(i, j, check)
                if check != 1:  # 没有在父节点出现
                    # 连接到已出现节点
                    i.son.append(M[j.number()])
                    M[j.number()].parent.append(i)

    close.clear()

    return check_right


def search(start):
    open = [start]  # 用于存放刚生成的节点
    close = []  # 存放扩展节点
    M = {start.number(): start}  # 存放出现过的状态
    flag = False  # 判断有无解标志
    while True:
        if len(open) == 0:
            break
        flag = expand_node(open, close, M)
    print("Successed or Failed?:", end="")
    if not flag:
        print("Failed")
    else:
        print("Successed")


if __name__ == '__main__':
    make_all_operate()
    start = LState(N, N, 1)
    search(start)
