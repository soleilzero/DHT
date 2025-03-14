import simpy
from node import Node
from ring import Ring

# Simulation
env = simpy.Environment()
ring = Ring(env)

# Creating and adding nodes to the ring
node1 = Node(env, 100)
node2 = Node(env, 250)
node3 = Node(env, 500)
node4 = Node(env, 750)
node5 = Node(env, 1000)

ring.add_node(node1)
ring.add_node(node2)
ring.add_node(node3)
ring.add_node(node4)
ring.add_node(node5)

# Test: Display the routing tables of all nodes
for node in ring.nodes:
    print(f"Node {node.node_id} routing table: {node.routing_table}")

# Store data
node1.put_data("user1", {"prenom": "Daniel", "x": "123", "y": "123"})
node1.put_data("user2", {"prenom": "Sol", "x": "123", "y": "123"})

# Retrieve data
print(node1.get_data("user1"))
print(node1.get_data("user2"))

# Test: Send a message from node1 to node5
print("\nSending message from Node 100 to Node 1000:")
message = type('Message', (object,), {"content": "Hello from Node 100!", "receiver_id": 1000})()
node1.route_message(message)

# Run the simulation
env.run(until=100)
