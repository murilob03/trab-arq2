import random
from main_memory import MainMemory
from bus import Bus
from cache import Cache
from enums import BloodType

MAIN_MEMORY_SIZE = 80
CACHE_SIZE = 3
BLOCK_SIZE = 5

if MAIN_MEMORY_SIZE % BLOCK_SIZE != 0:
    raise ValueError("The main memory size must be divisible by the block size!")

# Initializa objects
main_memory = MainMemory(MAIN_MEMORY_SIZE, BLOCK_SIZE)
bus = Bus(main_memory)
caches = [Cache(CACHE_SIZE, BLOCK_SIZE, bus) for _ in range(4)]

# Attach caches to bus
for cache in caches:
    bus.attach_cache(cache)

# Populate main memory
for i in range(0, MAIN_MEMORY_SIZE, BLOCK_SIZE):
    random_block = [random.choice(list(BloodType)) for _ in range(BLOCK_SIZE)]
    main_memory.write(i, random_block)

# Populate caches from main
for cache in caches:
    while cache.n < cache.n_max:
        cache.read(random.randint(0, MAIN_MEMORY_SIZE - 1))

# Main loop
while True:
    command = input(
        "PRINT MAIN (1), PRINT CACHE (2), CACHE READ (3), CACHE WRITE (4), EXIT (5)\n"
    )

    if command == "1":
        print(main_memory)
    if command == "2":
        cache_n = int(input(f"Select a cache to print (1-{len(caches)})\n")) - 1
        print(caches[cache_n])
    if command == "3":
        cache_n = int(input(f"Select a cache to read (1-{len(caches)})\n")) - 1
        addr = int(input(f"Select an address to read (0-{MAIN_MEMORY_SIZE})\n"))
        print(str(caches[cache_n].read(addr)))
    if command == "4":
        cache_n = int(input(f"Select a cache to read (1-{len(caches)})\n")) - 1
        addr = int(input(f"Select an address to read (0-{MAIN_MEMORY_SIZE})\n"))
        value = BloodType(input(f"Enter a value to write\n"))
        caches[cache_n].write(addr, value)
    if command == "5":
        break
