# -*- coding: utf-8 -*-
from pygraph.classes.digraph import digraph
import math
import random

from email_.PRIterator import PRIterator


class HITSIterator:
    __doc__ = '''计算一张图中的hub,authority值'''

    def __init__(self, dg):
        self.max_iterations = 200  # 最大迭代次数
        self.min_delta = 0.000000001  # 确定迭代是否结束的参数
        self.graph = dg

        self.hub = {}
        self.authority = {}
        for node in self.graph.nodes():
            self.hub[node] = 1
            self.authority[node] = 1

        pr = PRIterator(dg)
        page_ranks = pr.page_rank()
        for (k, v) in page_ranks.items():
            self.authority[k] = v

        print("---------------------------------")
        print(self.hub)
        print(self.authority)

    def hits(self):
        """
        计算每个页面的hub,authority值
        :return:
        """
        if not self.graph:
            return

        flag = False
        for i in range(self.max_iterations):
            change = 0.0  # 记录每轮的变化值
            norm = 0  # 标准化系数
            tmp = {}
            # 计算每个页面的authority值
            tmp = self.authority.copy()
            for node in self.graph.nodes():
                self.authority[node] = 0
                for incident_page in self.graph.incidents(node):  # 遍历所有“入射”的页面
                    self.authority[node] += self.hub[incident_page]
                norm += pow(self.authority[node], 2)
            # 标准化(Standardization)
            norm = math.sqrt(norm)
            for node in self.graph.nodes():
                self.authority[node] /= norm
                change += abs(tmp[node] - self.authority[node])

            # 计算每个页面的hub值
            norm = 0
            tmp = self.hub.copy()
            for node in self.graph.nodes():
                self.hub[node] = 0
                for neighbor_page in self.graph.neighbors(node):  # 遍历所有“出射”的页面
                    self.hub[node] += self.authority[neighbor_page]
                norm += pow(self.hub[node], 2)
            # 标准化(Standardization)
            norm = math.sqrt(norm)
            for node in self.graph.nodes():
                self.hub[node] /= norm
                change += abs(tmp[node] - self.hub[node])

            print("This is NO.%s iteration" % (i + 1))
            print("authority", self.authority)
            print("hub", self.hub)

            if change < self.min_delta:
                flag = True
                break
        if flag:
            print("finished in %s iterations!" % (i + 1))
        else:
            print("finished out of 100 iterations!")

        print("The best authority page: ", max(self.authority.items(), key=lambda x: x[1]))
        print("The best hub page: ", max(self.hub.items(), key=lambda x: x[1]))


def subgraph(dg, user_list):
    dg_dup = digraph()
    # repeat
    dg_dup.add_graph(dg)
    for (_out, _in) in dg.edges():
        if user_list.__contains__(_out):
            try:
                dg_dup.add_edge((_out, _in))
            except Exception:
                pass
    return dg_dup


def filter(dg):
    # 过滤只有出度没有入度的数据
    ins = [_in for (_out, _in) in dg.edges()]
    for (_out, _in) in dg.edges():
        if not ins.__contains__(_out):
            dg.del_edge((_out, _in))


if __name__ == '__main__':
    dg = digraph()

    # dg.add_nodes(["A", "B", "C", "D", "E"])
    # dg.add_edge(("A", "C"))
    # dg.add_edge(("A", "D"))
    # dg.add_edge(("B", "D"))
    # dg.add_edge(("C", "E"))
    # dg.add_edge(("D", "E"))
    # dg.add_edge(("B", "E"))
    # dg.add_edge(("E", "A"))

    # ehits算法实现的数据依赖了digraph,以上是数据输入的方式
    # 以下测试数据是随机生成,可换成真实数据

    user_dict = {}
    user_list = []
    index = 1
    for i in range(1, 5):
        for j in range(1, 1 << i):
            user_dict[index] = "user" + str(i) + str(j)
            index += 1
            user_list.append("user" + str(i) + str(j))

    dg.add_nodes(user_list)

    contact_dict = {}
    for m in range(0, 30000):
        m_from = int(random.random() * 25 + 1)
        m_to = int(random.random() * 25 + 1)
        if m_from == m_to:
            continue
        try:
            u_from = user_dict[m_from]
            u_to = user_dict[m_to]
            if abs(int(str(u_from)[4]) - int(str(u_to)[4])) <= 2 or int(str(u_from)[4]) > int(str(u_to)[4]):
                dg.add_edge((user_dict[m_from], user_dict[m_to]))
        except BaseException:
            a = '';

    print(dg.edges().__len__())

    # 根据subgraph算法扩展数据
    dg_dup = subgraph(dg, user_list)

    # 根据filter算法过滤数据
    filter(dg_dup)

    hits = HITSIterator(dg_dup)

    hits.hits()
