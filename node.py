from message import Message

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

    def send_message(self, receiver_id, content):
        """Sends a message to a specific node using ring-based routing."""
        message = Message(self, receiver_id, content)
        print(f"Node {self.node_id} is sending a message to Node {receiver_id}: '{content}'")
        self.route_message(message)

    def route_message(self, message):
        """Routes the message through the ring until it reaches the destination."""
        if self.node_id == message.receiver_id:
            print(f"Node {self.node_id} received message: '{message.content}'")
        else:
            # Determine the closest neighbor to forward the message
            clockwise_distance = (message.receiver_id - self.node_id) % 1000
            counter_clockwise_distance = (self.node_id - message.receiver_id) % 1000

            if clockwise_distance < counter_clockwise_distance:
                next_hop = self.right_neighbor
            else:
                next_hop = self.left_neighbor

            print(f"Node {self.node_id} forwarding message to Node {next_hop.node_id}")
            next_hop.route_message(message)

    def __str__(self):
        return f"Node {self.node_id}"