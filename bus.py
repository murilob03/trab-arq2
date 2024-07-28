from main_memory import MainMemory


class Bus:
    def __init__(self, main_memory: MainMemory):
        self.caches = []
        self.main_memory: MainMemory = main_memory

    def attach_cache(self, cache):
        self.caches.append(cache)

    def broadcast(self, message, address, sender) -> str:
        responses = []
        for cache in self.caches:
            if cache != sender:
                responses.append(cache.handle_snoop_message(message, address))
        if "shared" in responses:
            return "shared"
        return "ok"

    def write_back(self, address, data):
        self.main_memory.write(address, data)

    def read_from_main(self, address):
        return self.main_memory.read(address)
