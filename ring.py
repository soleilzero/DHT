class Ring:
    """Class that represents the ring, managing the nodes."""
    
    def __init__(self, env):
        self.env = env  # Simulation environment
        self.nodes = []  # List of nodes in the ring

    def add_node(self, node):
        """Adds a new node to the ring. If the ring is empty, the node points to itself."""
        if not self.nodes:
            # The first node in the ring connects to itself
            node.set_left_neighbor(node)
            node.set_right_neighbor(node)
            self.nodes.append(node)
            print(f"Node {node.node_id} is the first node in the ring.")
        else:
            # Connect the new node to the current last node
            first_node = self.nodes[0]
            last_node = self.nodes[-1]
            last_node.set_right_neighbor(node)
            node.set_left_neighbor(last_node)
            node.set_right_neighbor(first_node)
            first_node.left_neighbor = node
            self.nodes.append(node)
            print(f"Node {node.node_id} joined between Node {last_node.node_id} and {self.nodes[0].node_id}")


    def remove_node(self, node):
        """Removes a node from the ring."""
        if len(self.nodes) > 1:
            node.leave()  # Removes the node and updates the neighbors
            self.nodes.remove(node)
        else:
            print("Cannot remove the last node from the ring.")

