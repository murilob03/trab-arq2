import random
from main_memory import MainMemory
from bus import Bus
from cache import Cache
from enums import BloodType

MAIN_MEMORY_SIZE = 50
CACHE_SIZE = 6
BLOCK_SIZE = 2

main_memory = MainMemory(MAIN_MEMORY_SIZE, BLOCK_SIZE)

bus = Bus(main_memory)

cache1 = Cache(CACHE_SIZE, BLOCK_SIZE, bus)

bus.attach_cache(cache1)

for i in range(MAIN_MEMORY_SIZE):
    random_block = [random.choice(list(BloodType)) for _ in range(BLOCK_SIZE)]
    main_memory.write(i, random_block)
