def next_node(node_info, new_node):
    node_info[f"node_{len(node_info)}"] = new_node
    return node_info