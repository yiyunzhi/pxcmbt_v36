import anytree
import wx


class TreeModel(object):
    """Class represents a tree structure with hidden root.
    TreeModel is used together with TreeView class to display results in GUI.
    The functionality is not complete, only needed methods are implemented.
    If needed, the functionality can be extended.
    >>> tree = TreeModel(TreeModelDictNode)
    >>> root = tree.root
    >>> n1 = tree.append_node(parent=root, data={"label": "node1"})
    >>> n2 = tree.append_node(parent=root, data={"label": "node2"})
    >>> n11 = tree.append_node(parent=n1, data={"label": "node11", "xxx": 1})
    >>> n111 = tree.append_node(parent=n11, data={"label": "node111", "xxx": 4})
    >>> n12 = tree.append_node(parent=n1, data={"label": "node12", "xxx": 2})
    >>> n21 = tree.append_node(parent=n2, data={"label": "node21", "xxx": 1})
    >>> [node.label for node in tree.search_nodes(key='xxx', value=1)]
    ['node11', 'node21']
    >>> [node.label for node in tree.search_nodes(key='xxx', value=5)]
    []
    >>> tree.get_index_of_node(n111)
    [0, 0, 0]
    >>> tree.get_node_by_index((0,1)).label
    'node12'
    >>> print(tree)
    node1
      * label : node1
      node11
        * label : node11
        * xxx : 1
        node111
          * label : node111
          * xxx : 4
      node12
        * label : node12
        * xxx : 2
    node2
      * label : node2
      node21
        * label : node21
        * xxx : 1
    """

    def __init__(self, node_class):
        """Constructor creates root node.
        :param node_class: class which is used for creating nodes
        """
        self._root = node_class()
        self.nodeClass = node_class

    @property
    def root(self):
        return self._root

    @root.setter
    def root(self, root):
        self._root = root

    def append_node(self, parent, **kwargs):
        """Create node and append it to parent node.
        :param parent: parent node of the new node
        :return: new node
        """
        _node = self.nodeClass(**kwargs)
        # useful for debugging deleting nodes
        # weakref.finalize(node, print, "Deleted node {}".format(label))
        # parent.children.append(node)
        parent.append_children(_node)
        # weakref doesn't work out of the box when deepcopying this class
        # node.parent = weakref.proxy(parent)
        # node.parent = parent
        return _node

    def search_nodes(self, parent=None, **kwargs):
        """Search nodes according to specified attributes."""
        _nodes = []
        parent = parent if parent else self._root
        self._search_nodes(node=parent, found_nodes=_nodes, **kwargs)
        return _nodes

    def _search_nodes(self, node, found_nodes, **kwargs):
        """Helper method for searching nodes."""
        if node.match(**kwargs):
            found_nodes.append(node)
        for child in node.children:
            self._search_nodes(node=child, found_nodes=found_nodes, **kwargs)

    def get_node_by_index(self, index):
        """Method used for communication between view (VirtualTree) and model.
        :param index: index of node, as defined in VirtualTree doc
                      (e.g. root ~ [], second node of a first node ~ [0, 1])
        """
        if len(index) == 0:
            return self._root
        return self._get_node(self._root, index)

    def get_index_of_node(self, node):
        """Method used for communication between view (VirtualTree) and model."""
        _index = []
        return tuple(self._get_index(node, _index))

    def _get_index(self, node, index):
        if node.parent:
            index.insert(0, node.parent.children.index(node))
            return self._get_index(node.parent, index)
        return index

    def get_children_by_index(self, index):
        """Method used for communication between view (VirtualTree) and model."""
        if len(index) == 0:
            return self._root.children
        _node = self._get_node(self._root, index)
        return _node.children

    def _get_node(self, node, index):
        if len(index) == 1:
            return node.children[index[0]]
        else:
            return self._get_node(node.children[index[0]], index[1:])

    def remove_node(self, node):
        """Removes node. If node is root, removes root's children, root is kept."""
        if node.parent:
            node.parent.children.remove(node)
        else:
            # node is root
            del node.children[:]

    def sort_children(self, node):
        """Sorts children with 'natural sort' based on label."""
        if node.children:
            sorted(node.children, key=lambda x: x.label)

    def filtered(self, **kwargs):
        """Filters model based on parameters in kwargs
        that are passed to node's match function.
        Copies tree and returns a filtered copy."""

        def _filter(node):
            if node.children:
                _to_remove = []
                for child in node.children:
                    _match = _filter(child)
                    if not _match:
                        _to_remove.append(child)
                for child in reversed(_to_remove):
                    _f_model.remove_node(child)
                if node.children:
                    return True
            return node.match(**kwargs)

        import copy
        _f_model = copy.deepcopy(self)
        _filter(_f_model.root)

        return _f_model

    def get_leaf_count(self, node):
        """Returns the number of leaves in a node."""
        if node.children:
            _count = 0
            for child in node.children:
                _count += self.get_leaf_count(child)
            return _count
        return 1

    def __str__(self):
        """Print tree."""
        text = []
        for child in self._root.children:
            child.node_print(text)
        return "\n".join(text)


class TreeModelNode:
    def __init__(self):
        self.columns = dict()
        self.label = 'Node'
        self.parent = None
        self.children = list()

    def match(self, key, value):
        raise NotImplemented

    def node_print(self, text, indent=0):
        raise NotImplemented

    def append_children(self, child):
        raise NotImplemented


class TreeModelDictNode(TreeModelNode):
    """Node which has data in a form of dictionary."""

    def __init__(self, data=None):
        """Create node.
        :param data: data as dictionary or None
        """
        super(TreeModelDictNode, self).__init__()
        if not data:
            self.data = {"label": ""}
        else:
            self.data = data
        self._children = []

    def append_children(self, child):
        self._children.append(child)
        child.parent = self

    def node_print(self, text, indent=0):
        text.append(indent * " " + self.label)
        if self.data:
            for key, value in self.data.items():
                text.append(
                    "%(indent)s* %(key)s : %(value)s"
                    % {"indent": (indent + 2) * " ", "key": key, "value": value}
                )

        if self.children:
            for child in self.children:
                child.node_print(text, indent + 2)

    def match(self, key, value):
        """Method used for searching according to given parameters.
        :param value: dictionary value to be matched
        :param key: data dictionary key
        """
        if key in self.data and self.data[key] == value:
            return True
        return False


class TreeModelModuleNode(TreeModelDictNode):
    """Node representing module."""

    def __init__(self, label=None, data=None):
        super(TreeModelModuleNode, self).__init__(data=data)
        self.label = label if label else ""
        if not data:
            self.data = {}

    def match(self, key, value, case_sensitive=False):
        """Method used for searching according to command,
        keywords or description."""
        if not self.data:
            return False
        if isinstance(key, str):
            keys = [key]
        else:
            keys = key

        for key in keys:
            if key not in ("command", "keywords", "description"):
                return False
            try:
                text = self.data[key]
            except KeyError:
                continue
            if not text:
                continue
            if case_sensitive:
                # start supported but unused, so testing last
                if value in text or value == "*":
                    return True
            else:
                # this works fully only for English and requires accents
                # to be exact match (even Python 3 casefold() does not help)
                if value.lower() in text.lower() or value == "*":
                    return True
        return False


class TreeModelAnyTreeNode(TreeModelNode, anytree.NodeMixin):
    def __init__(self, **kwargs):
        TreeModelNode.__init__(self)
        self.icon = kwargs.get('icon', wx.ART_NORMAL_FILE)
        self.label = kwargs.get('label', '')
        self.highlighted = False
        if 'parent' in kwargs:
            self.parent = kwargs.get('parent')

    def append_children(self, child):
        child.parent = self

    def match(self, key, value):
        """Method used for searching according to given parameters.
        :param value: dictionary value to be matched
        :param key: data dictionary key
        """
        if hasattr(self, key):
            return getattr(self, key) == value
        return False

    def node_print(self, text, indent=0):
        text.append(indent * " " + self.label)
        text.append(indent * " " + str(anytree.RenderTree(self)))

    def get_icon_variant(self):
        if self.icon:
            if self.highlighted:
                return '%sH' % self.icon
            else:
                return self.icon
        return wx.ART_NORMAL_FILE
