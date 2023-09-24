# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                                                            --
#                PHOENIX CONTACT GmbH & Co., D-32819 Blomberg                --
#                                                                            --
# ------------------------------------------------------------------------------
# Project       : 
# Sourcefile(s) : class_tc_generator_srch_base.py
# ------------------------------------------------------------------------------
#
# File          : class_tc_generator_srch_base.py
#
# Author(s)     : Gaofeng Zhang
#
# Status        : in work
#
# Description   : siehe unten
#
#
# ------------------------------------------------------------------------------
import networkx as nx


class GraphSearchBasedVisitor:
    def __init__(self):
        self._g = None

    @staticmethod
    def get_transition_vertex_graph(graph: nx.DiGraph, start_node):
        """
        method to get the graph, whose edges as vertex. the edge of graph must have
        Attributes named label for identify the name.
        Args:
            graph: nx.DiGraph
            start_node: any

        Returns: nx.DiGraph

        """
        _g = nx.DiGraph()
        _init_ts = set()
        for x in graph.edges:
            _g.add_node(graph.get_edge_data(*x)['label'], node=(x[0], x[1]))
        for x in graph.nodes:
            for s_src, s_tgt in graph.out_edges(x):
                _src_label = graph.get_edge_data(s_src, s_tgt)['label']
                if s_src == start_node:
                    _init_ts.add(_src_label)
                for ss_src, ss_tgt in graph.out_edges(s_tgt):
                    _dst_label = graph.get_edge_data(ss_src, ss_tgt)['label']
                    _g.add_edge(_src_label, _dst_label, label='%s_%s' % (_src_label, _dst_label))
        return _g, _init_ts

    def draw(self, graph, subplot_ind=212):
        # plt.subplot(subplot_ind)
        pos = nx.planar_layout(graph)
        nx.draw_networkx_nodes(graph, pos)
        nx.draw_networkx_edges(graph, pos, edgelist=graph.edges, edge_color='b', width=2)
        nx.draw_networkx_edge_labels(graph, pos, edge_labels=nx.get_edge_attributes(graph, 'label'), label_pos=0.3)
        nx.draw_networkx_labels(graph, pos)
    # todo: rename to generate_tour_use_edge_graph
    def generate_tour_use_edge_graph(self, graph: nx.DiGraph, start_node: any):
        _g, _init_ts = self.get_transition_vertex_graph(graph, start_node)
        if not _init_ts:
            raise ValueError()
        _path = list()
        _node_attr_map = nx.get_node_attributes(_g, 'node')
        for x in _init_ts:
            _p = list()
            for p in nx.edge_dfs(_g, x):
                _p.append(p)
            _ol = self._merge_pair_paths(_p, _g, x)
            for p in _ol:
                _kl = list()
                for idx, sd in enumerate(p):
                    if idx == 0:
                        _kl.append(sd[0])
                        _kl.append(sd[1])
                    else:
                        _kl.append(sd[1])
                _path.append([_node_attr_map[x] for x in _kl])
        return _path

    def generate_tour(self, graph: nx.DiGraph, init_node):
        _srch_path = [list(x) for x in nx.edge_dfs(graph, init_node)]
        return self._merge_pair_paths(_srch_path, graph, init_node)

    @staticmethod
    def get_coverage(seqs: list, g: nx.Graph) -> tuple:
        """
        method get the coverage statistic by given edges sequence on the graph g.
        four float will be calculated.
        percent of visited node,percent of visited edge,redundant of visited node, redundant of visited edges
        @param seqs: list
        @param g: nx.Graph
        @return: float,float,float,float
        """
        _all_edges = g.edges()
        _all_nodes = g.nodes()
        if len(_all_nodes) == 0 or len(_all_edges) == 0:
            return 0, 0, 0, 0
        _node_visit_count = dict()
        _edge_visit_count = dict()
        for t_seq in seqs:
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

    @staticmethod
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
