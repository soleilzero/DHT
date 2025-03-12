import simpy
from node import Node
from ring import Ring

# Simulation
env = simpy.Environment()
ring = Ring(env)

# Creating and adding nodes to the ring
node1 = Node(env, 10)
node2 = Node(env, 20)
node3 = Node(env, 30)
node4 = Node(env, 40)
node5 = Node(env, 50)

ring.add_node(node1)
ring.add_node(node2)
ring.add_node(node3)
ring.add_node(node4)
ring.add_node(node5)

# Sending messages with routing
print("\n--- Testing message routing ---")
node1.send_message(
    40, "Hello Node 40, this is Node 10!"
)  # Should be routed through the ring
node3.send_message(10, "Hey Node 10, I'm Node 30!")  # Should go counter-clockwise

# Simulating the removal of a node
print("\n--- Removing Node 20 ---")
ring.remove_node(node2)

# Sending another message to check if routing still works after node removal
print("\n--- Testing message routing after node removal ---")
node1.send_message(50, "Hello Node 50, are you still there?")

# Run the simulation
env.run(until=100)
