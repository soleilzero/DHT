import random

class Ring:
    """Class that represents the ring, managing the nodes."""
    def __init__(self, env):
        self.env = env  # Simulation environment
        self.nodes = []  # List of nodes in the ring

    def add_node(self, node):
        """Adds a new node to the ring. If the ring is empty, the node points to itself."""
        if not self.nodes:
            node.set_left_neighbor(node)
            node.set_right_neighbor(node)
            self.nodes.append(node)
            print(f"Node {node.node_id} is the first node in the ring.")
        else:
            # Find the correct position based on node_id
            self.nodes.append(node)
            self.nodes.sort(key=lambda x: x.node_id)  # Keep nodes sorted by ID

            index = self.nodes.index(node)
            left_neighbor = self.nodes[index - 1]
            right_neighbor = self.nodes[(index + 1) % len(self.nodes)]

            node.set_neighbors(left_neighbor, right_neighbor)
            left_neighbor.set_right_neighbor(node)
            right_neighbor.set_left_neighbor(node)

            print(f"Node {node.node_id} joined between Node {left_neighbor.node_id} and Node {right_neighbor.node_id}.")

    def remove_node(self, node):
        """Removes a node from the ring and updates neighbors."""
        if len(self.nodes) > 1:
            # Antes de remover o nó, replicar os dados para os vizinhos dos vizinhos
            self.replicate_data(node)
            
            left_neighbor = node.left_neighbor
            right_neighbor = node.right_neighbor

            left_neighbor.set_right_neighbor(right_neighbor)
            right_neighbor.set_left_neighbor(left_neighbor)

            self.nodes.remove(node)
            print(f"Node {node.node_id} left. Node {left_neighbor.node_id} is now connected to Node {right_neighbor.node_id}.")
        else:
            print("Cannot remove the last node from the ring.")

    def replicate_data(self, node):
        """Replicate data from node to one of its neighbors (left or right)."""
        # Verifica se o nó tem vizinhos e se há dados para replicar
        if node.left_neighbor is None or node.right_neighbor is None:
            print(f"Node '{node.node_id}' cannot replicate data because it has no neighbors.")
            return

        # Sélectionner aléatoirement le voisin du voisin à qui répliquer
        neighbor_to_replicate = random.choice([
            node.left_neighbor.left_neighbor, 
            node.right_neighbor.right_neighbor
        ])

        for key, value in node.storage.items():
            print(f"Replicating key '{key}' to Node {neighbor_to_replicate.node_id}.")
            neighbor_to_replicate.storage[key] = value

