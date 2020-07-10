import csv
import codecs


# 结点类
class vertex:
    def __init__(self, name, tag):
        self.name = name
        self.tag = list()
        self.tag.append(tag)
        self.degree = 0
        self.max_sim = 0        # 最大相似度
        self.link = list()      # 邻接关系
        self.e_in = list()      # 连入
        self.e_out = list()     # 连出
        self.sim = dict()       # 相似点

    def e_in_(self, v):
        self.e_in.append(v.name)
        self.degree += 1
        self.link.extend(v.tag)
        if len(self.link) != 0:
            self.link = list(set(self.link))

    def e_out_(self, v):
        self.e_out.append(v.name)
        self.degree += 1
        # self.link.append(v.tag)
        self.link.extend(v.tag)
        if len(self.link) != 0:
            self.link = list(set(self.link))

    def e_link_(self, v):
        self.e_out.append(v.name)
        self.e_in.append(v.name)
        self.degree += 1
        # self.link.append(v.tag)
        list(set(self.link) | set(v.tag))

    def sim_(self, v, val):
        self.sim[v.name] = val
        self.max_sim = max(zip(self.sim.values(), self.sim.keys()))[0]


Verts1 = dict()
Verts2 = dict()
with open('../[.csv','r') as f:
    # 读取G1结点信息，保存在Vertex1 包含所有给出相似点的点
    data = csv.reader(f)
    vs = [row[1] for row in data]
    for ver in vs:
        try:
            Verts1[ver]
        except:
            # Verts[ver] = vertex(ver,len(Verts))
            Verts1[ver] = vertex(ver, len(Verts1))
    # data = csv.reader(f)

'''with open('[1_Callgraph.csv', 'r') as f:      
    # 读取G1结点信息，保存在Vertex1
    reader = csv.reader(f)
    # print(type(reader))
    for row in reader:
        try:
            Verts1[row[0]]
        except:
            Verts1[row[0]] = vertex(row[0], len(Verts1))
        try:
            Verts1[row[1]]
        except:
            Verts1[row[1]] = vertex(row[1], len(Verts1))
        ver = Verts1[row[0]]
        ver1 = Verts1[row[1]]
        ver.e_out_(ver1)
        ver1.e_in_(ver)'''      # 忽略孤立点

with open('../[.csv', 'r') as f:
    # 读取G1、G2相似关系
    data = csv.reader(f)
    for row in data:
        # print(row)
        try:
            Verts1[row[1]]
            for i in range(3, len(row) - 1, 3):
                try:
                    Verts2[row[i]]
                    Verts2[row[i]].tag.append(Verts1[row[1]].tag[0])
                except:
                    Verts2[row[i]] = vertex(row[i], Verts1[row[1]].tag[0])
                Verts1[row[1]].sim_(Verts2[row[i]], row[i+1])
                # Verts2[row[i]].tag = Verts1[row[1]].tag
        except:
            pass


with open('../[1_Callgraph.csv', 'r') as f:
    # 读取G1连通关系
    reader = csv.reader(f)
    # print(type(reader))
    for row in reader:
        ver = Verts1[row[0]]
        ver1 = Verts1[row[1]]
        ver.e_out_(ver1)
        # ver.e_link_(ver1)
        # ver1.e_link_(ver)
        ver1.e_in_(ver)

with open('../[2_Callgraph.csv', 'r') as f:
    # 读取G2结点信息，连通关系，保存在Vertex2
    reader = csv.reader(f)
    # print(type(reader))
    for row in reader:
        try:
            Verts2[row[0]]
            # Verts2[row[0]].tag.append()
        except:
            Verts2[row[0]] = vertex(row[0], 'NAN')
        try:
            Verts2[row[1]]
        except:
            Verts2[row[1]] = vertex(row[1], 'NAN')
        ver = Verts2[row[0]]
        ver1 = Verts2[row[1]]
        ver.e_out_(ver1)
        ver1.e_in_(ver)

'''lines = list()
for k, ver in Verts1.items():
    e_in = ';'.join(ver.e_in)
    e_out = ';'.join(ver.e_out)
    sim = list()
    for key, val in ver.sim.items():
        sim.append(key+':'+val)
    sim = ';'.join(sim)
    lines.append([ver.name, ver.tag, ver.degree, ver.max_sim, e_in, e_out, sim])
write_csv(lines, 'G1.csv')

lines = list()
for k, ver in Verts2.items():
    e_in = ';'.join(ver.e_in)
    e_out = ';'.join(ver.e_out)
    sim = list()
    for key, val in ver.sim.items():
        sim.append(key+':'+val)
    sim = ';'.join(sim)
    lines.append([ver.name, ver.tag, ver.degree, ver.max_sim, e_in, e_out, sim])
write_csv(lines, 'G2.csv')'''        # write vertex info


def step_in(Verts1, v1, v2):
    # 查找v1到v2满足最大相似度割边
    # ver_a = v1[0]
    # ver_e = Verts1[v1[0]].e_out[0]
    max_sim = 0
    for ver1 in v1:
        # print(ver1.e_out & v2)
        # ver_outs = ver1.e_out & v2
        Ver2 = [ver2 for ver2 in Verts1[ver1].e_out if ver2 in v2]      # 可行域
        if len(Ver2) == 0:      # 可行域为空
            continue
        for ver2 in Ver2:       # 可行域不为空遍历可行域求相似度最大值
            sim = Verts1[ver2].max_sim
            if float(sim) > max_sim:
                ver_a = ver1
                ver_e = ver2
                max_sim = float(sim)
    try:
        ver_e
        return ver_e, ver_a
    except:     # 可行域为空
        # print('find no suitable edge!')
        return 0, 0
        # ver_e = Ver2[0]
        # ver_a = ver1
    # max_sim = max(zip([v.max_sim for v in v2], [v.name for v in v2]))
    # (ver_e, cost) = max(zip(v1[max_sim[1]].sim.values(), v1[max_sim[1]].sim.keys()))


def sub_tree_gen(Verts1, Edg1, v2, root):
    # 最大子树生成
    v1 = list([root])
    v2.remove(v2[v2.index(root)])
    # v2 = list([v.name for (k, v) in Verts1.items()].pop('main'))
    while( len(v2)!= 0):
        ver_e, ver_a = step_in(Verts1, v1, v2)
        if ver_a == ver_e == 0:
            break
        v1.append(ver_e)        # 更新集合
        v2.remove(v2[v2.index(ver_e)])
        # Verts1[ver_a].e_out.remove(Verts1[ver_a].e_out[Verts1[ver_a].e_out.index(ver_e)])
        Edg1[Edg1.index([ver_a, ver_e, 0])][2] = 1
        # print(ver_a, '-->', ver_e)
    return Edg1, v1


all_trees = list()      # 子树结点集列表
Verts3 = dict()         # 单次迭代子树结点字典
for k, ver in Verts1.items():
    v2 = list()
    for key, v in Verts1.items():
        v2.append(v.name)
    Edg1 = list()
    with open('../[1_Callgraph.csv', 'r') as f:
        data = csv.reader(f)
        for row in data:
            Edg1.append([row[0], row[1], 0])
    Edg, v1 = sub_tree_gen(Verts1, Edg1, v2, ver.name)
    Edg2 = [li for li in Edg if li[2] == 1]     # 树边列表
    for row in Edg2:
        try:
            Verts3[row[0]]
        except:
            Verts3[row[0]] = vertex(row[0], (Verts1[row[0]].tag)[0])
            Verts3[row[0]].sim = Verts1[row[0]].sim
            Verts3[row[0]].max_sim = Verts1[row[0]].max_sim
        try:
            Verts3[row[1]]
        except:
            Verts3[row[1]] = vertex(row[1], (Verts1[row[1]].tag)[0])
            # erts3[row[1]] = Verts1[row[1]]
            Verts3[row[1]].sim = Verts1[row[1]].sim
            Verts3[row[1]].max_sim = Verts1[row[1]].max_sim
        ver = Verts3[row[0]]
        ver1 = Verts3[row[1]]
        ver.e_out_(ver1)
        ver1.e_in_(ver)
    all_trees.append(Verts3)        # 所有子树字典列表
    Verts3 = dict()
    # all.append([row[2] for row in Edg])
# write_csv(all, '../tree_edge1.csv')
'''while(len(v2) != 0):
    Edg, v1, v2 = sub_tree_gen(Verts1, Edg1, v2, v2[0])
    blank = [[' ']]
    write_csv(blank, 'tree_edge.csv')
    write_csv(Edg, 'tree_edge.csv')'''

v1 = vertex
v2 = vertex
cv1 = vertex
cv2 = vertex
vr = vertex

'''比较'''
def compare(v1,v2):
    #v2点度小于v1直接结束返回0
    if v2.degree < v1.degree:
        return 0

    tag1 = v1.tag[0]
    tags2 = v2.tag
    #v2点不和v1相似返回0
    if tag1 not in tags2:
        return 0
    mark = 0
    for v in v1.link:
        if v not in v2.link:
            mark += 1
            # return 0
    if mark > 0:
        return 0
    return 1

def gogogo(v1,v2,num):
    # flag_sim = 0
    for eo1 in v1.e_out:
        cv1 = all_trees[num][eo1]
        for eo2 in v2.e_out:
            cv2 = Verts2[eo2]
            if compare(cv1, cv2) == 1:
                if Verts5.__contains__(cv2.name):
                    continue
                else:
                    cv11 = vertex(cv1.name, cv1.tag[0])
                    cv11.e_in.append(v1.name)
                    cv11.degree += 1
                    cv22 = vertex(cv2.name, cv1.tag[0])
                    cv22.e_in.append(v2.name)
                    cv22.degree += 1
                    Verts4[cv11.name] = cv11
                    Verts5[cv22.name] = cv22
                    Verts4[v1.name].e_out.append(cv11.name)
                    Verts4[v1.name].degree += 1
                    Verts5[v2.name].e_out.append(cv22.name)
                    Verts5[v2.name].degree += 1
                    gogogo(cv1, cv2, num)
                    break
            # cv1和cv2分别为子树


Verts4 = dict()
Verts5 = dict()
sub_trees1 = list()
sub_trees2 = list()


all_tree_edges1 = list()     # G1所有匹配树边并集
all_tree_edges2 = list()     # G2所有匹配树边并集

for i, t1 in enumerate(all_trees):
    if len(t1) < 10:
        continue
    #print(i,t1)
    # print(Ver_list[i])
    vr = Verts1[vs[i]]
    for v in vr.sim:
        v2 = Verts2[v]
        if compare(vr, v2) == 1:
            vrr = vertex(vr.name, vr.tag[0])
            v22 = vertex(v2.name, vr.tag[0])
            Verts4[vr.name] = vrr
            Verts5[v2.name] = v22
            gogogo(vr, v2, i)  #根相同就向下迭代
            break
    sub_trees1.append(Verts4)
    sub_trees2.append(Verts5)
    for k4, v4 in Verts4.items():
        for v4_out in v4.e_out:
            if [v4.name, v4_out] not in all_tree_edges1:
                all_tree_edges1.append([v4.name, v4_out])
    for k5, v5 in Verts5.items():
        for v5_out in v5.e_out:
            if [v5.name, v5_out] not in all_tree_edges2:
                all_tree_edges2.append([v5.name, v5_out])
    Verts4 = dict()
    Verts5 = dict()

wr = 0
l_o_vs = list()     # 匹配结点映射关系表
for i, t in enumerate(sub_trees1):
    # cmp mismatch check
    l1 = [v.name for k1, v in t.items()]
    l2 = [v.name for k2, v in sub_trees2[i].items()]
    for j, p in enumerate(l1):
        if ([l1[j], l2[j]] not in l_o_vs) and ([l2[j], l1[j]] not in l_o_vs):
            l_o_vs.append([l1[j], l2[j]])


'''Accuracy cal'''
test = 0        # number of mismatch
print('匹配结点数：', len(l_o_vs))
print('错误匹配结果：')
for val in l_o_vs:
    if val[0] != val[1]:
        test += 1
        print(val)
print('结点匹配准确率:\n', (1-(test/len(l_o_vs)))*100, '%')     # acc


def write_csv(Lis, filename):
    # 写嵌套列表到csv文件
    file_csv = codecs.open(filename, 'w+', 'utf-8')
    writer = csv.writer(file_csv, delimiter=',', quotechar=' ', quoting=csv.QUOTE_MINIMAL)
    for row in Lis:
        writer.writerow(row)
# print(sub_trees1)
# print(sub_trees2)
'''uni_trees1 = dict()
uni_trees2 = dict()
for tt in sub_trees1:
    uni_trees1 = dict(uni_trees1, **tt)
for tt in sub_trees2:
    uni_trees2 = dict(uni_trees2, **tt)

Vs1 = len(uni_trees1) #子图1点数
Vs2 = len(uni_trees2) #子图2点数
print(Vs1)
print(Vs2)
print(wr/Vs1)
print(wr/Vs2)
# print(uni_trees1)
# print(uni_trees2)'''

write_csv(l_o_vs, '../match_vertex.csv')        # 匹配结点映射关系
write_csv(all_tree_edges1, '../match_edge_G1.csv')      # G1匹配子图边表
write_csv(all_tree_edges2, '../match_edge_G2.csv')      # G1匹配子图边表
