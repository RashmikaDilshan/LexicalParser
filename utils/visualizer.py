import json
from io import StringIO


def generate_html_tree(root):
    """
    Generate HTML representation of parse tree with styling
    """
    if not root:
        return "<p>No parse tree available</p>"
    
    html = StringIO()
    html.write('<div class="parse-tree">\n')
    
    def render_node(node, level=0):
        indent = "  " * (level + 1)
        margin = level * 40
        
        # Determine node class based on type
        if node.is_epsilon():
            node_class = "epsilon-node"
        elif node.name.startswith('id') or node.name.startswith('num'):
            node_class = "terminal-node"
        elif node.name in ['+', '-', '*', '/', '%', '**']:
            node_class = "operator-node"
        elif node.name in ['(', ')']:
            node_class = "delimiter-node"
        else:
            node_class = "non-terminal-node"
        
        html.write(f'{indent}<div class="tree-node {node_class}" style="margin-left: {margin}px;">\n')
        html.write(f'{indent}  <span class="node-label">{node.name}</span>\n')
        
        if node.children:
            html.write(f'{indent}  <div class="children">\n')
            for child in node.children:
                render_node(child, level + 1)
            html.write(f'{indent}  </div>\n')
        
        html.write(f'{indent}</div>\n')
    
    render_node(root)
    html.write('</div>\n')
    
    return html.getvalue()


def generate_json_tree(root):
    """
    Generate JSON representation of parse tree
    """
    if not root:
        return json.dumps(None)
    
    return json.dumps(root.to_dict(), indent=2)


def generate_svg_tree(root, width=800, height=600):
    """
    Generate SVG representation of parse tree
    Simple implementation without external dependencies
    """
    if not root:
        return '<svg width="400" height="100"><text x="10" y="50">No parse tree</text></svg>'
    
    svg = StringIO()
    svg.write(f'<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">\n')
    svg.write('  <defs>\n')
    svg.write('    <style>\n')
    svg.write('      .node-rect { fill: #e3f2fd; stroke: #1976d2; stroke-width: 2; }\n')
    svg.write('      .node-text { font-family: monospace; font-size: 14px; fill: #000; }\n')
    svg.write('      .tree-line { stroke: #666; stroke-width: 1.5; fill: none; }\n')
    svg.write('    </style>\n')
    svg.write('  </defs>\n')
    
    # Calculate node positions
    node_positions = {}
    node_counter = [0]
    
    def calculate_positions(node, x, y, h_spacing):
        node_id = node_counter[0]
        node_counter[0] += 1
        node_positions[node_id] = (x, y, node)
        
        if node.children:
            child_spacing = h_spacing / len(node.children)
            start_x = x - (h_spacing / 2) + (child_spacing / 2)
            
            for i, child in enumerate(node.children):
                child_x = start_x + (i * child_spacing)
                calculate_positions(child, child_x, y + 80, child_spacing)
    
    calculate_positions(root, width / 2, 50, width - 100)
    
    # Draw edges
    for node_id, (x, y, node) in node_positions.items():
        for child in node.children:
            # Find child position
            for cid, (cx, cy, cnode) in node_positions.items():
                if cnode == child:
                    svg.write(f'  <line x1="{x}" y1="{y + 20}" x2="{cx}" y2="{cy - 5}" class="tree-line"/>\n')
    
    # Draw nodes
    for node_id, (x, y, node) in node_positions.items():
        text_width = len(node.name) * 8
        rect_width = max(60, text_width + 20)
        svg.write(f'  <rect x="{x - rect_width/2}" y="{y - 15}" width="{rect_width}" height="30" rx="5" class="node-rect"/>\n')
        svg.write(f'  <text x="{x}" y="{y + 5}" text-anchor="middle" class="node-text">{node.name}</text>\n')
    
    svg.write('</svg>\n')
    return svg.getvalue()


def generate_tree_statistics(root):
    """
    Generate statistics about the parse tree
    """
    if not root:
        return {}
    
    stats = {
        'total_nodes': root.count_nodes(),
        'height': root.get_height(),
        'leaf_count': len(root.get_leaves()),
        'non_terminals': 0,
        'terminals': 0,
        'epsilon_count': 0
    }
    
    all_nodes = root.get_all_nodes()
    for node, level in all_nodes:
        if node.is_epsilon():
            stats['epsilon_count'] += 1
        elif node.is_leaf():
            stats['terminals'] += 1
        else:
            stats['non_terminals'] += 1
    
    return stats


def format_tree_ascii(root):
    """
    Format parse tree as ASCII art
    """
    if not root:
        return "No parse tree"
    
    lines = []
    
    def build_lines(node, prefix="", is_last=True):
        # Current node
        connector = "└── " if is_last else "├── "
        lines.append(prefix + connector + node.name)
        
        # Extension for children
        extension = "    " if is_last else "│   "
        
        # Process children
        for i, child in enumerate(node.children):
            child_is_last = (i == len(node.children) - 1)
            build_lines(child, prefix + extension, child_is_last)
    
    lines.append(root.name)
    for i, child in enumerate(root.children):
        is_last = (i == len(root.children) - 1)
        build_lines(child, "", is_last)
    
    return "\n".join(lines)