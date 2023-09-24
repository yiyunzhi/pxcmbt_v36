import networkx as nx

from mbt.workbenches.workbench_model.application.class_fsm import GraphBasedFSM
from mbt.workbenches.workbench_test.application.class_tc_generator_srch_base import GraphSearchBasedVisitor


class EdgeBasedSeqTourVisitor:
    def __init__(self):
        self._nextNode = None

    def visit(self, sequence: list, graph: nx.Graph):
        for src, dst in sequence:
            if self._nextNode is not None:
                self._nextNode.on_enter()
                self._nextNode.on_exit()
            else:
                src.on_enter()
                pass
                src.on_exit()
            _ed = graph.get_edge_data(src, dst)
            _ed['user_object'].exe()
            self._nextNode = dst
        if self._nextNode is not None:
            self._nextNode.on_enter()
            self._nextNode.on_exit()
        self._nextNode = None


class TGraphNode:
    def __init__(self, **kwargs):
        self.name = kwargs.get('name')

    def __repr__(self):
        return '{}'.format(self.name)

    def on_enter(self):
        print('%s on_enter' % self.name)

    def on_exit(self):
        print('%s on_exit' % self.name)


# todo: if sub graph? parallel sequences generation use product??

class TGraphEdge:
    def __init__(self, **kwargs):
        self.name = kwargs.get('name')

    def __repr__(self):
        return '{}'.format(self.name)

    def exe(self):
        print('%s on_exe' % self.name)

# todo: fsm->graph (make it plainful)
# todo: whatever is necessary,that convert FSM/STC/FUNC to graph.
# todo: TGraphNode could any type. since the graph is not node type relative.
# todo: GraphBasedFSM used in prototype node only.
_fsmg = GraphBasedFSM()
_init_state = TGraphNode(name='s1')
_state2 = TGraphNode(name='s2')
_state3 = TGraphNode(name='s3')
_fsmg.add_state(_init_state)
_fsmg.add_state(_state2)
_fsmg.add_state(_state3)
# todo: edge object
_fsmg.add_transition(_state3, _init_state, 's3->s144', TGraphEdge(name='s3->s1'))
_fsmg.add_transition(_state3, _state2, 's3->s2', TGraphEdge(name='s3->s2'))
_fsmg.add_transition(_state2, _state3, 's2->s3', TGraphEdge(name='s2->s3'))
_fsmg.add_transition(_init_state, _state2, 's1->s2', TGraphEdge(name='s1->s2'))
_fsmg.add_transition(_state2, _init_state, 's2->s1', TGraphEdge(name='s2->s1'))

gen = GraphSearchBasedVisitor()
_seq1 = gen.generate_tour(_fsmg, _init_state)
print('*' * 20 + 'sequence' + '*' * 20)
for x in _seq1:
    print(x)
print('*' * 20 + 'coverage' + '*' * 20)
print(gen.get_coverage(_seq1, _fsmg))
print('*' * 20 + 'seq walk' + '*' * 20)
_sw = EdgeBasedSeqTourVisitor()
for x in _seq1:
    _sw.visit(x, _fsmg)
    print('--' * 20)
# _seq2 = gen.generate_tour_use_edge_graph(_fsmg, _init_state)
# for x in _seq2:
#     print(x)
# print(gen.get_coverage(_seq2, _fsmg))
