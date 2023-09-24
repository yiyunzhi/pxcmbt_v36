import functools
import networkx as nx

_fsm = nx.DiGraph()
_init_state = 's1'
_fsm.add_node('s1')
_fsm.add_node('s2')
_fsm.add_node('s3')

_fsm.add_edge('s3', 's1')
_fsm.add_edge('s3', 's2')
_fsm.add_edge('s2', 's3')
_fsm.add_edge('s1', 's2')
# _fsm.add_edge('s2', 's1')
_srch_path = [list(x) for x in nx.edge_dfs(_fsm, _init_state)]
print('--->srch path fsm1:', _srch_path)


def _g_coverage(t_seqs, g: nx.Graph) -> tuple:
    """
    method get the coverage statistic by given edges sequence on the graph g.
    four float will be calculated.
    percent of visited node,percent of visited edge,redundant of visited node, redundant of visited edges
    @param t_seqs: list
    @param g: nx.Graph
    @return: float,float,float,float
    """
    _all_edges = g.edges()
    _all_nodes = g.nodes()
    if len(_all_nodes) == 0 or len(_all_edges) == 0:
        return 0, 0, 0, 0
    _node_visit_count = dict()
    _edge_visit_count = dict()
    for t_seq in t_seqs:
        for e in t_seq:
            _src, _tgt = e
            _k_e = str(e)
            if _k_e not in _edge_visit_count:
                _edge_visit_count[_k_e] = 1
            else:
                _edge_visit_count[_k_e] += 1
            if _src not in _node_visit_count:
                _node_visit_count[_src] = 1
            else:
                _node_visit_count[_src] += 1
            if _tgt not in _node_visit_count:
                _node_visit_count[_tgt] = 1
            else:
                _node_visit_count[_tgt] += 1
    _node_cvg = 0
    _edge_cvg = 0
    _visited_edges = set(_edge_visit_count.keys())
    _visited_nodes = set(_node_visit_count.keys())
    _sum_node_visit = sum(_node_visit_count.values())
    _sum_edge_visit = sum(_edge_visit_count.values())
    return (round(len(_visited_nodes) / len(_all_nodes), 2),
            round(len(_visited_edges) / len(_all_edges), 2),
            round(_sum_node_visit / len(_visited_nodes), 2),
            round(_sum_edge_visit / len(_visited_edges), 2))


def _merge_pair_paths(pp: list, g: nx.Graph, src_node: str) -> list:
    """
    method to merge the list of pair to lists, which contains the sequence
    tail of previous is the head of next.
    etc. pp=[['s1', 's2'], ['s2', 's3'], ['s3', 's1'], ['s3', 's2']]
    return the result like
        [['s1', 's2'], ['s2', 's3'], ['s3', 's1']]
        [['s1', 's2'], ['s2', 's3'], ['s3', 's2']]

    @param pp: list of list(tuple)
    @param g: nx.Graph
    @param src_node: str
    @return: list

    """
    if not pp:
        return []
    _container = [x for x in pp]
    # first split the tuple not connect to next
    _muster_idx = 0
    _lst = [[_container.pop(_muster_idx)]]
    while _container:
        _next = _container.pop(0)
        if _next[0] != _lst[_muster_idx][-1][-1]:
            _lst.append([_next])
            _muster_idx += 1
        else:
            _lst[_muster_idx].append(_next)
    for x in _lst:
        if x[0][0] != src_node:
            _path_g = nx.path_graph(nx.shortest_path(g, src_node, x[0][0]))
            _edge_lst = list(_path_g.edges())
            _edge_lst = [list(c) for c in _edge_lst]
            if not _edge_lst:
                continue
            _edge_lst.reverse()
            [x.insert(0, c) for c in _edge_lst]
    return _lst


print('-' * 20)
_tsq = _merge_pair_paths(_srch_path, _fsm, _init_state)
for x in _tsq:
    print('-->:', x)
print('cvg:', _g_coverage(_tsq, _fsm))
print('-' * 20)

_fsm2 = nx.DiGraph()
_init_state = 's1'
_fsm2.add_node('s1')
_fsm2.add_node('s2')
_fsm2.add_node('s3')
_fsm2.add_node('s4')
_fsm2.add_node('s5')
_fsm2.add_node('s6')

_fsm2.add_edge('s4', 's4')
_fsm2.add_edge('s4', 's3')
_fsm2.add_edge('s3', 's1')
_fsm2.add_edge('s1', 's5')
_fsm2.add_edge('s3', 's4')
_fsm2.add_edge('s1', 's4')
_fsm2.add_edge('s2', 's4')
_fsm2.add_edge('s2', 's6')
_fsm2.add_edge('s1', 's2')

# _fsm.add_edge('s2', 's1')
_srch_path = [list(x) for x in nx.edge_dfs(_fsm2, _init_state)]
print('--->srch path fsm2:', _srch_path)
_tsq = _merge_pair_paths(_srch_path, _fsm2, _init_state)
for x in _tsq:
    print('-->:', x)
print('cvg:', _g_coverage(_tsq, _fsm2))

# _path = list(nx.shortest_path(_fsm, _init_state, 's3'))
# _path_g = nx.path_graph(_path)
# print('path graph->edges:', _path_g.edges())
# print('testpath of fsm3 directly!--->',list(nx.all_simple_paths(_fsm3._g,_fsm3.init_state,'s2')))
