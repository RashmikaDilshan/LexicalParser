import json

class ParseTreeNode:
    """
    Represents a node in the parse tree Can be a non-terminal, terminal, or epsilon
    """
    
    def __init__(self, name, value=None):
        self.name = name
        self.value = value
        self.children = []
        self.node_id = None  # For visualization
    
    def add_child(self, child):
        """Add a child node to this node"""
        if child:
            self.children.append(child)
    
    def is_leaf(self):
        """Check if this is a leaf node"""
        return len(self.children) == 0
    
    def is_epsilon(self):
        """Check if this node represents epsilon"""
        return self.name == 'ε'
    
    def __repr__(self):
        return f"ParseTreeNode({self.name})"
    
    def to_dict(self):
        """
        Convert parse tree to dictionary for JSON serialization
        """
        return {
            'name': self.name,
            'value': self.value,
            'children': [child.to_dict() for child in self.children]
        }
    
    def to_string(self, level=0):
        """
        Convert parse tree to formatted string representation
        """
        indent = "  " * level
        result = f"{indent}{self.name}"
        if self.value:
            result += f" = {self.value}"
        result += "\n"
        
        for child in self.children:
            result += child.to_string(level + 1)
        
        return result
    
    def get_all_nodes(self):
        """
        Get all nodes in the tree (DFS traversal)
        Returns list of (node, level) tuples
        """
        nodes = [(self, 0)]
        for child in self.children:
            if hasattr(child, 'get_all_nodes'):
                child_nodes = child.get_all_nodes()
                nodes.extend([(n, level + 1) for n, level in child_nodes])
        return nodes
    
    def count_nodes(self):
        """Count total number of nodes in the tree"""
        count = 1
        for child in self.children:
            count += child.count_nodes()
        return count
    
    def get_height(self):
        """Get the height of the tree"""
        if self.is_leaf():
            return 1
        return 1 + max(child.get_height() for child in self.children)
    
    def get_leaves(self):
        """Get all leaf nodes"""
        if self.is_leaf():
            return [self]
        leaves = []
        for child in self.children:
            leaves.extend(child.get_leaves())
        return leaves


def visualize_tree_ascii(root):
    """
    Create ASCII art representation of parse tree
    """
    def build_tree_lines(node, prefix="", is_last=True):
        """Recursively build tree lines"""
        lines = []
        
        # Current node
        connector = "└── " if is_last else "├── "
        lines.append(prefix + connector + str(node.name))
        
        # Extension for children
        extension = "    " if is_last else "│   "
        
        # Process children
        for i, child in enumerate(node.children):
            child_is_last = (i == len(node.children) - 1)
            child_lines = build_tree_lines(child, prefix + extension, child_is_last)
            lines.extend(child_lines)
        
        return lines
    
    if not root:
        return "Empty tree"
    
    lines = [str(root.name)]
    for i, child in enumerate(root.children):
        is_last = (i == len(root.children) - 1)
        lines.extend(build_tree_lines(child, "", is_last))
    
    return "\n".join(lines)


def tree_to_graphviz(root):
    """
    Generate Graphviz DOT format for tree visualization
    """
    dot_lines = ["digraph ParseTree {"]
    dot_lines.append('  node [shape=box, style="rounded,filled", fillcolor=lightblue];')
    dot_lines.append('  edge [arrowsize=0.5];')
    
    node_counter = [0]  # Use list to make it mutable in nested function
    
    def add_node(node, parent_id=None):
        """Recursively add nodes to DOT representation"""
        current_id = node_counter[0]
        node_counter[0] += 1
        
        # Node label
        label = node.name
        
        # Set node color based on type
        if node.is_epsilon():
            color = "lightgray"
        elif node.name.startswith('id') or node.name.startswith('num'):
            color = "lightgreen"
        elif node.name in ['+', '-', '*', '/', '%', '**']:
            color = "lightyellow"
        elif node.name in ['(', ')']:
            color = "lightpink"
        else:
            color = "lightblue"
        
        dot_lines.append(f'  node{current_id} [label="{label}", fillcolor={color}];')
        
        # Add edge from parent
        if parent_id is not None:
            dot_lines.append(f'  node{parent_id} -> node{current_id};')
        
        # Process children
        for child in node.children:
            add_node(child, current_id)
    
    if root:
        add_node(root)
    
    dot_lines.append("}")
    return "\n".join(dot_lines)


def serialize_tree(root):
    """
    Serialize parse tree to JSON string
    """
    if not root:
        return json.dumps(None)
    return json.dumps(root.to_dict(), indent=2)


def deserialize_tree(json_str):
    """
    Deserialize parse tree from JSON string
    """
    def dict_to_node(d):
        if d is None:
            return None
        node = ParseTreeNode(d['name'], d.get('value'))
        for child_dict in d.get('children', []):
            node.add_child(dict_to_node(child_dict))
        return node
    
    tree_dict = json.loads(json_str)
    return dict_to_node(tree_dict)