import zmq
import time
import json

class MarvinMessageBus:
    def __init__(self):
        self.context = zmq.Context()
        
        # PUB socket: For broadcasting system-wide events
        self.pub_socket = self.context.socket(zmq.PUB)
        self.pub_socket.bind("tcp://*:5556")
        
        # SUB socket: To receive messages from any module to re-broadcast
        self.sub_socket = self.context.socket(zmq.SUB)
        self.sub_socket.bind("tcp://*:5557")
        self.sub_socket.setsockopt_string(zmq.SUBSCRIBE, "")

        print("[BUS] Internal Resonance Bus Active on Ports 5556 (PUB) and 5557 (SUB)")

    def start(self):
        """
        Acts as a proxy/forwarder. 
        Collects messages from port 5557 and broadcasts them to 5556.
        """
        try:
            while True:
                # Check for incoming messages from modules
                try:
                    message = self.sub_socket.recv_json(flags=zmq.NOBLOCK)
                    topic = message.get("topic", "GENERAL")
                    print(f"[BUS] Routing: {topic} -> {message.get('data')}")
                    
                    # Re-broadcast to all subscribers
                    self.pub_socket.send_json(message)
                except zmq.Again:
                    # No message received, sleep briefly to save CPU
                    time.sleep(0.01)
        except KeyboardInterrupt:
            print("[BUS] Shutting down...")
        finally:
            self.pub_socket.close()
            self.sub_socket.close()
            self.context.term()

if __name__ == "__main__":
    bus = MarvinMessageBus()
    bus.start()