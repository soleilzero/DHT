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


    def put_data(self, key, value):
        """Store a key-value pair in the responsible node and replicate to two neighbors."""
        if self.left_neighbor is None or self.right_neighbor is None:
            print(f"Node '{self.node_id}' is not in the ring")
            return

        target_node = self.find_responsible_node(key)
        
        # Store data in the responsible node
        print(f"Storing key '{key}' in Node {target_node.node_id}")
        target_node.storage[key] = value  

        # Replicate data to left and right neighbors
        left_replica = target_node.left_neighbor
        right_replica = target_node.right_neighbor
        
        left_replica.storage[key] = value
        right_replica.storage[key] = value
        
        print(f"Replicated key '{key}' to Node {left_replica.node_id} and Node {right_replica.node_id}")

    def get_data(self, key):
        """Retrieve a value from the responsible node or its neighbors in case of failure."""
        if self.left_neighbor is None or self.right_neighbor is None:
            print(f"Node '{self.node_id}' is not in the ring")
            return None

        target_node = self.find_responsible_node(key)

        # Check responsible node
        if key in target_node.storage:
            print(f"Key '{key}' found in Node {target_node.node_id} with value: {target_node.storage[key]}")
            return target_node.storage[key]

        # If not found, check the replicas (left and right neighbors)
        left_replica = target_node.left_neighbor
        right_replica = target_node.right_neighbor

        if key in left_replica.storage:
            print(f"Key '{key}' found in replica Node {left_replica.node_id} with value: {left_replica.storage[key]}")
            return left_replica.storage[key]

        if key in right_replica.storage:
            print(f"Key '{key}' found in replica Node {right_replica.node_id} with value: {right_replica.storage[key]}")
            return right_replica.storage[key]

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
            self.receive_message(message)
        else:
            message.visited_nodes.append(self)
            # Check if there's a long link for faster routing
            if message.receiver_id in self.routing_table:
                self.long_link_message(message)

            # Standard ring routing if no long link is available
            else:
                self.hop_message(message)

    def receive_message(self, message):
        print(f"Node {self.node_id} received message: '{message.content}'")
        if message.sender not in self.routing_table:
            self.add_long_link(message.sender)
        for node in message.visited_nodes:
            if node not in self.routing_table:
                self.add_long_link(node)

    def long_link_message(self, message):
        next_hop = self.routing_table[message.receiver_id]
        print(f"Node {self.node_id} sending message directly to Node {next_hop.node_id} via long link")
        next_hop.route_message(message)

    def hop_message(self, message):
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
