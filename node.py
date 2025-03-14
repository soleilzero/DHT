from message import Message
import hashlib


class Node:
    def __init__(self, env, node_id):
        self.env = env
        self.node_id = node_id
        self.left_neighbor = None
        self.right_neighbor = None
        self.storage = {}
        self.routing_table = {} #new for part4.1

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
        print(
            f"Node {self.node_id} is sending a message to Node {receiver_id}: '{content}'"
        )
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

    def put_data(self, key, value):
        """Store a key-value pair in the appropriate node using consistent hashing."""
        if self.left_neighbor == None or self.right_neighbor == None:
            print(f"Node '{self.node_id}' is not in the ring")
            return
        target_node = self.find_responsible_node(key)
        print(f"Storing key '{key}' in Node {target_node.node_id}")
        target_node.storage[key] = value  # Store the value

    def get_data(self, key):
        if self.left_neighbor == None or self.right_neighbor == None:
            print(f"Node '{self.node_id}' is not in the ring")
            return
        """Retrieve a value from the appropriate node."""
        target_node = self.find_responsible_node(key)
        if key in target_node.storage:
            print(
                f"Key '{key}' found in Node {target_node.node_id} with value: {target_node.storage[key]}"
            )
            return target_node.storage[key]
        else:
            print(f"Key '{key}' not found in the ring.")
            return None

    def find_responsible_node(self, key):
        """Find the node responsible for a given key using hashing."""
        key_hash = (
            int(hashlib.sha256(key.encode()).hexdigest(), 16) % 1000
        )  # Hash to a number in range

        # Check if there's a long link that directly maps to this key
        if key_hash in self.routing_table:
            return self.routing_table[key_hash]

        current = self
        print(key, "was hashed to", key_hash)
        # Traverse the ring to find the node with the closest larger ID
        while current.right_neighbor.node_id != self.node_id:
            if current.node_id >= key_hash:
                return current
            current = current.right_neighbor

        return current  # Default to last node if none found

    def add_long_link(self, distant_node):
        """Adds a long link to the routing table."""
        self.routing_table[distant_node.node_id] = distant_node

    def route_message(self, message):
        """Routes the message through the ring until it reaches the destination."""
        if self.node_id == message.receiver_id:
            print(f"Node {self.node_id} received message: '{message.content}'")
        else:
            # Check if there's a long link for faster routing
            if message.receiver_id in self.routing_table:
                next_hop = self.routing_table[message.receiver_id]
                print(f"Node {self.node_id} sending message directly to Node {next_hop.node_id} via long link")
                next_hop.route_message(message)
            else:
                # Standard ring routing if no long link is available
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
