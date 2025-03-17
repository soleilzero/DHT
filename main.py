import simpy
from node import Node
from ring import Ring


def main():

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

    display_routing_table_of_all_nodes_in(ring.nodes)

    # Store data
    node1.put_data("user1", {"prenom": "Daniel", "x": "123", "y": "123"})
    node1.put_data("user2", {"prenom": "Sol", "x": "123", "y": "123"})

    # Retrieve data
    print(node1.get_data("user1"))
    print(node1.get_data("user2"))

    send_message_between_nodes(node1, node5.node_id, f"Hello from Node {node1.node_id}!")
    send_message_between_nodes(node2, node5.node_id, f"Hello from Node {node1.node_id}!")

    display_routing_table_of_all_nodes_in(ring.nodes)

    # Send message quicker by "cheating"
    node2.add_long_link(node5)
    send_message_between_nodes(node2, node5.node_id, f"Hello from Node {node1.node_id}!")

    display_routing_table_of_all_nodes_in(ring.nodes)
    # Run the simulation
    env.run(until=100)


def display_routing_table_of_all_nodes_in(nodes):
    print("\n\n#----------> Display routing table:")
    for node in nodes:
        print(f"Node {node.node_id} routing table: {node.routing_table}")
    print("\n")


def send_message_between_nodes(sender, receiver_id, content):
    print(f"\n\n#----------> Sending message from Node {sender.node_id} to Node {receiver_id}:")
    message = type('Message', (object,), {"sender": sender, "content": content, "receiver_id": receiver_id})()
    sender.route_message(message)


if __name__ == "__main__":
    main()