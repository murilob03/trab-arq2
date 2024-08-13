from src.components import Bus
from src.enums import BloodType, MESITag, SnoopMessage, SnoopResponse


# Represents a single cache block
class CacheBlock:
    def __init__(self, tag, data):
        self.tag: MESITag = tag  # MESI tag (Modified, Exclusive, Shared, Invalid)
        self.data: list[BloodType | None] = list(data)  # Data stored in the cache block

    def __str__(self) -> str:
        # String representation of the cache block
        return f"({' | '.join([str(x) for x in self.data])} || {self.tag.value})"


# Cache class managing cache operations and coherence
class Cache:
    def __init__(self, n_lines, block_size, bus) -> None:
        self.max_lines = n_lines  # Maximum number of cache blocks
        self.block_size = block_size  # Size of each cache block

        self.current_lines = 0  # Current number of blocks in the cache
        self.queue = []  # FIFO queue for managing block eviction
        self.data: dict[int, CacheBlock] = {}  # Mapping of addresses to cache blocks

        self.bus: Bus = bus  # Bus for communication with main memory and other caches

    # Calculate the block index based on the address
    def calculate_block_index(self, address):
        return address - (address % self.block_size)

    # Read a block from cache
    def read(self, address, to_write=False, is_local=False) -> CacheBlock | None:
        block_index = self.calculate_block_index(address)
        block = self.data.get(block_index)

        # If block is found and is not invalid, it's a hit
        if block and block.tag != MESITag.I:
            self.handle_cache_hit(to_write, is_local)
            return block

        # If it's a local read and the block is not found, return None
        if is_local:
            return None

        # Handle cache miss if the block is not found or invalid
        return self.handle_cache_miss(address, block_index, to_write)

    # Handle a cache hit
    def handle_cache_hit(self, to_write, is_local):
        if not is_local:
            if to_write:
                print("Write Hit!")
            else:
                print("Read Hit!")

    # Handle a cache miss, either for read or write
    def handle_cache_miss(self, address, block_index, to_write) -> CacheBlock:
        if to_write:
            print("Write Miss!")
            response = self.broadcast_message(
                SnoopMessage.READ_WITH_INTENT_TO_MODIFY, block_index
            )
        else:
            print("Read Miss!")
            response = self.broadcast_message(SnoopMessage.READ, block_index)

        # Fetch the block from main memory
        block_from_main = self.bus.read_from_main(block_index)
        # Set tag based on snoop response
        tag = MESITag.S if response == SnoopResponse.SHARED else MESITag.E
        new_block = CacheBlock(tag, block_from_main)

        # Update existing block or add a new one
        if block_index in self.data:
            self.data[block_index] = new_block
        else:
            self.add_block_to_cache(block_index, new_block)

        return new_block

    # Add a block to the cache, handling eviction if necessary
    def add_block_to_cache(self, block_index, new_block: CacheBlock):
        if self.current_lines >= self.max_lines:
            self.evict_block()  # Evict a block using FIFO policy

        self.data[block_index] = new_block
        self.queue.append(block_index)
        self.current_lines += 1

    # Evict the oldest block from the cache
    def evict_block(self):
        removed_addr = self.queue.pop(0)  # Remove the oldest block
        # Write the evicted block back to main memory
        self.bus.write_back(removed_addr, self.data[removed_addr].data)
        del self.data[removed_addr]
        self.current_lines -= 1

    # Write data to the cache
    def write(self, address, data):
        block = self.read(address, to_write=True)  # First, read to get the cache block

        # If the block is shared, broadcast an invalidate message
        if block.tag == MESITag.S:  # type: ignore
            self.broadcast_message(SnoopMessage.INVALIDATE, address)

        # Write the data to the block at the position corresponding to the address
        index = address % self.block_size
        block.data[index] = data  # type: ignore
        block.tag = MESITag.M  # Mark the block as modified # type: ignore

        block_index = self.calculate_block_index(address)
        self.data[block_index] = block  # type: ignore

        return 0  # Return 0 to indicate success

    # Handle snoop messages (reads/writes from other caches)
    def handle_snoop_message(self, message, address) -> SnoopResponse:
        block_index = self.calculate_block_index(address)
        block = self.read(address, is_local=True)  # Perform a local read of the block

        if message == SnoopMessage.READ:
            return self.handle_read_snoop(block, block_index, address)
        elif message == SnoopMessage.READ_WITH_INTENT_TO_MODIFY:
            return self.handle_rwitm_snoop(block, block_index, address)
        elif message == SnoopMessage.INVALIDATE:
            return self.handle_invalidate_snoop(block, block_index)
        return SnoopResponse.INVALID

    # Handle a READ snoop message
    def handle_read_snoop(self, block, block_index, address) -> SnoopResponse:
        if not block or block.tag == MESITag.I:
            return SnoopResponse.OK

        if block.tag == MESITag.M:
            self.bus.write_back(address, block.data)
            self.data[block_index].tag = MESITag.S
            return SnoopResponse.SHARED

        if block.tag == MESITag.E:
            self.data[block_index].tag = MESITag.S

        return SnoopResponse.SHARED

    # Handle a READ_WITH_INTENT_TO_MODIFY snoop message
    def handle_rwitm_snoop(self, block, block_index, address) -> SnoopResponse:
        if not block or block.tag == MESITag.I:
            return SnoopResponse.OK

        if block.tag == MESITag.M:
            self.bus.write_back(address, block.data)
            return SnoopResponse.OK

        self.data[block_index].tag = MESITag.I
        return SnoopResponse.OK

    # Handle an INVALIDATE snoop message
    def handle_invalidate_snoop(self, block, block_index) -> SnoopResponse:
        if not block or block.tag == MESITag.I:
            return SnoopResponse.OK

        self.data[block_index].tag = MESITag.I
        return SnoopResponse.OK

    # Send a message via the bus
    def broadcast_message(self, message, address) -> SnoopResponse:
        return self.bus.broadcast(message, address, self)  # type: ignore

    # String representation of the cache, showing all blocks in the FIFO queue
    def __str__(self) -> str:
        return "\n".join([f"{addr}: {str(self.data[addr])}" for addr in self.queue])
