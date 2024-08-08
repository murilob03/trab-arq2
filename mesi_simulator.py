import random

from components import Cache, MainMemory, Bus

from enums import BloodType


# Constants
MAIN_MEMORY_SIZE = 200
CACHE_SIZE = 10
BLOCK_SIZE = 5

# Validate main memory size
if MAIN_MEMORY_SIZE % BLOCK_SIZE != 0:
    raise ValueError("The main memory size must be divisible by the block size!")


class MESISimulator:
    def __init__(
        self, main_memory_size=200, cache_size=10, n_caches=4, block_size=5
    ) -> None:
        self.main_memory = MainMemory(main_memory_size, block_size)
        self.bus = Bus(self.main_memory)
        self.caches = [Cache(cache_size, block_size, self.bus) for _ in range(n_caches)]

        for cache in self.caches:
            self.bus.attach_cache(cache)

    def populate_main_memory(self):
        # Populate main memory with random data
        for i in range(0, MAIN_MEMORY_SIZE, BLOCK_SIZE):
            random_block = [random.choice(list(BloodType)) for _ in range(BLOCK_SIZE)]
            self.main_memory.write(i, random_block)

    def populate_caches(self):
        # Populate caches from main memory
        for cache in self.caches:
            while cache.n < cache.n_max:
                cache.read(random.randint(0, MAIN_MEMORY_SIZE - 1))
