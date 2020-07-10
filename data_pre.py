import csv
import codecs


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


# data=csv.reader('../[1_Callgraph.csv')
# Verts=list()


Verts1 = dict()
Verts2 = dict()

with open('../[.csv','r') as f:     # 读取G1结点信息，保存在Vertex1 包含所有给出相似点的点
    data = csv.reader(f)
    vs = [row[1] for row in data]
    for ver in vs:
        try:
            Verts1[ver]
        except:
            # Verts[ver] = vertex(ver,len(Verts))
            Verts1[ver] = vertex(ver, len(Verts1))
    # data = csv.reader(f)

'''with open('../[1_Callgraph.csv', 'r') as f:      # 读取G1结点信息，保存在Vertex1
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

with open('../[.csv', 'r') as f:   # 读取G1、G2相似关系
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


with open('../[1_Callgraph.csv', 'r') as f:     # 读取G1连通关系
    reader = csv.reader(f)
    # print(type(reader))
    for row in reader:
        ver = Verts1[row[0]]
        ver1 = Verts1[row[1]]
        ver.e_out_(ver1)
        # ver.e_link_(ver1)
        # ver1.e_link_(ver)
        ver1.e_in_(ver)

with open('../[2_Callgraph.csv', 'r') as f:     # 读取G2结点信息，连通关系，保存在Vertex2
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
write_csv(lines, '../G1.csv')

lines = list()
for k, ver in Verts2.items():
    e_in = ';'.join(ver.e_in)
    e_out = ';'.join(ver.e_out)
    sim = list()
    for key, val in ver.sim.items():
        sim.append(key+':'+val)
    sim = ';'.join(sim)
    lines.append([ver.name, ver.tag, ver.degree, ver.max_sim, e_in, e_out, sim])
write_csv(lines, '../G2.csv')'''        # write vertex info


def step_in(Verts1, v1, v2):
    # 子树生成子函数，查找v1到v2最大相似度新边
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
        v1.append(ver_e)
        v2.remove(v2[v2.index(ver_e)])
        # Verts1[ver_a].e_out.remove(Verts1[ver_a].e_out[Verts1[ver_a].e_out.index(ver_e)])
        Edg1[Edg1.index([ver_a, ver_e, 0])][2] = 1
        # print(ver_a, '-->', ver_e)
    return Edg1, v1


def write_csv(Lis, filename):
    file_csv = codecs.open(filename, 'w+', 'utf-8')
    writer = csv.writer(file_csv, delimiter=',', quotechar=' ', quoting=csv.QUOTE_MINIMAL)
    for row in Lis:
        writer.writerow(row)


'''Ept = list()
for k, ve in Verts1.items():
    for v in ve.link:
        if v not in Verts2[ve.name].link:
            if len(ve.e_out) != 0:
                if len(ve.e_in) != 0:
                    Ept.append(ve.name)
    Ept = list(set(Ept))
print(Ept, '\n', len(Ept))'''

Edg_G2 = list()     # G2边集
with open('../[2_Callgraph.csv', 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        row.append(0)
        Edg_G2.append(row)

exp_mark = list()
all_trees = list()      # 子树结点集列表
Verts3 = dict()     # 子树结点集
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
    # print(type(reader))
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
            Verts3[row[1]] = Verts1[row[1]]
            Verts3[row[1]].sim = Verts1[row[1]].sim
            Verts3[row[0]].max_sim = Verts1[row[0]].max_sim
        ver = Verts3[row[0]]
        ver1 = Verts3[row[1]]
        ver.e_out_(ver1)
        ver1.e_in_(ver)
    '''Ept = list()
    for k, ve in Verts3.items():
        for v in ver.link:
            if v not in Verts2[ve.name].link:
                Ept.append(ve.name)'''
    all_trees.append(Verts3)        # 所有子树字典列表
    '''if len(Ept) == 0:
        exp_mark.append(1)
    else:
        exp_mark.append(0)'''
    Verts3 = dict()
    # all.append([row[2] for row in Edg])
# write_csv(all, '../tree_edge1.csv')
'''while(len(v2) != 0):
    Edg, v1, v2 = sub_tree_gen(Verts1, Edg1, v2, v2[0])
    blank = [[' ']]
    write_csv(blank, '../tree_edge.csv')
    write_csv(Edg, '../tree_edge.csv')'''
# print(exp_mark)


def vert_cmp(Verts2, v3, Verts3):
    children = v3.e_out
    match = list()
    for child in children:
        pos_v = [name for name, val in Verts3[child].sim.items()]
        pos_v = [x for x in pos_v if x in Verts2[v3.name].e_out]
        print(child, pos_v)
        if len(pos_v)!=0:
            max_sim = Verts3[child].sim[pos_v[0]]
            mpv = pos_v[0]
            for pv in pos_v:
                if Verts3[child].sim[pv] > max_sim:
                    max_sim = Verts3[child].sim[pv]
                    mpv = pv
            match.append(mpv)
        # else:
    return match


def tree_cmp(Verts2,root, Verts3):
    # root = 'main'
    v_match = list([root])
    mchild = vert_cmp(Verts2, Verts3[root], Verts3)
    v_match.extend(mchild)
    return v_match


def cmp(Verts2, root, Verts3):
    v_match = list([root])
    if len(Verts3[root].e_out) == 0:
        print(v_match)
        return v_match
    else:
        for root1 in Verts3[root].e_out:
            child_cmp = tree_cmp(Verts2, root1, Verts3)
            v_match.extend(child_cmp)
    return v_match


cmp_result = cmp(Verts2, 'eval', all_trees[6])
print('Done!')


