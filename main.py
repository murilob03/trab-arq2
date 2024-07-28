import random
from main_memory import MainMemory
from bus import Bus
from cache import Cache
from enums import BloodType

MAIN_MEMORY_SIZE = 50
CACHE_SIZE = 3
BLOCK_SIZE = 2

main_memory = MainMemory(MAIN_MEMORY_SIZE, BLOCK_SIZE)

bus = Bus(main_memory)

caches = [Cache(CACHE_SIZE, BLOCK_SIZE, bus) for _ in range(4)]

for cache in caches:
    bus.attach_cache(cache)

for i in range(MAIN_MEMORY_SIZE):
    random_block = [random.choice(list(BloodType)) for _ in range(BLOCK_SIZE)]
    main_memory.write(i, random_block)

while True:
    command = input("PRINT MAIN (1), PRINT CACHE (2), CACHE READ (3), CACHE WRITE (4), EXIT (5)\n")

    if command == '1':
        print(main_memory)
    if command == '2':
        cache_n = int(input("Select a cache to read (1-4)\n")) - 1
        print(caches[cache_n])
    if command == '3':
        cache_n = int(input("Select a cache to read (1-4)\n")) - 1
        addr = int(input(f"Select a address to read (0-{MAIN_MEMORY_SIZE})\n"))
        print(str(caches[cache_n].read(addr)))
    if command == '5':
        break