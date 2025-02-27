
class Message:
    def __init__(self, sender, receiver, content):
        self.sender =sender
        self.receiver = receiver
        self.content = content
        self.is_delivered = False

    def send(self):
        if not self.is_delivered:
            self.is_delivered = True
            self.receiver.receive_message(self)
            print("The message has been delivered.")
            
        


    def __str__(self):
        return f"Message from Node {self.sender.node_id} to Node {self.receiver.node_id}: {self.content}"
