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
        
    def receive_message(self, message):
        print(f"Node {self.node_id} received message from Node {message.sender.node_id}: '{message.content}'")
        message.send()

    def __str__(self):
        return f"Node {self.node_id}"