import simpy
import random

class Node:
    
    def __init__(self, env, node_id):
        self.env = env  
        self.node_id = node_id  
        self.left_neighbor = None  
        self.right_neighbor = None  

    def set_left_neighbor(self, other_node):
        self.left_neighbor = other_node

    def set_right_neighbor(self, other_node):
        self.right_neighbor = other_node

    def set_neighbors(self, left_neighbor, right_neighbor):
        self.left_neighbor = left_neighbor
        self.right_neighbor = right_neighbor

    def set_left_neighbor_of_right_neighbor(self, other_node):
        self.right_neighbor.set_left_neighbor(other_node)

    def set_right_neighbor_of_left_neighbor(self, other_node):
        self.left_neighbor.set_right_neighbor(other_node)

    def join(self, other_node):
        """The node joins the ring by connecting to an existing node."""
        print(f"Node {self.node_id} is joining the ring.")
        # The node connects to the node on the right of the other node
        self.set_neighbors(other_node, other_node.right_neighbor)
        # Updates the neighbors of the other nodes
        other_node.set_left_neighbor_of_right_neighbor(self)
        other_node.set_right_neighbor(self)
        print(f"Node {self.node_id} joined between Node {other_node.node_id} and Node {other_node.right_neighbor.node_id}.")

    def leave(self):
        """The node leaves the ring and updates its neighbors."""
        if self.left_neighbor and self.right_neighbor:
            print(f"Node {self.node_id} is leaving the ring.")
            self.set_right_neighbor_of_left_neighbor(self.right_neighbor)
            self.set_left_neighbor_of_right_neighbor(self.left_neighbor)
            print(f"Node {self.node_id} left. Node {self.left_neighbor.node_id} is now connected to Node {self.right_neighbor.node_id}.")
        else:
            print(f"Node {self.node_id} has no neighbors to leave.")
            
    def receive_message(self, message):
        
        print(f"Node {self.node_id} received message from Node {message.sender.node_id}: '{message.content}'")
        message.send()

    def __str__(self):
        return f"Node {self.node_id}"

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

