from src.enums import SnoopResponse

# Represents the bus that connects multiple caches and the main memory
class Bus:
    def __init__(self, main_memory):
        self.caches = []  # List of caches attached to the bus
        self.main_memory = main_memory  # Reference to the main memory

    # Attach a cache to the bus
    def attach_cache(self, cache):
        self.caches.append(cache)

    # Broadcast a message to all caches except the sender
    def broadcast(self, message, address, sender) -> SnoopResponse:
        responses = []  # Collect responses from caches
        for cache in self.caches:
            if cache != sender:  # Do not send the message back to the sender
                responses.append(cache.handle_snoop_message(message, address))
        # If any cache responds with SHARED, return SHARED
        if SnoopResponse.SHARED in responses:
            return SnoopResponse.SHARED
        # Otherwise, return OK
        return SnoopResponse.OK

    # Write data back to the main memory
    def write_back(self, address, data):
        self.main_memory.write(address, data)

    # Read data from the main memory
    def read_from_main(self, address):
        return self.main_memory.read(address)
