from bus import Bus
from enums import BloodType, MESITag, SnoopMessage


class CacheBlock:
    def __init__(self, tag, data):
        self.tag: MESITag = tag
        self.data: list[BloodType | None] = list(data)

    def __str__(self) -> str:
        return f"({' | '.join([str(x) for x in self.data])} || {self.tag.value})"


class Cache:
    def __init__(self, n_lines, block_size, bus) -> None:
        self.n_max = n_lines  # max number of blocks
        self.block_size = block_size  # the size of a block

        self.n = 0  # actual number of blocks
        self.queue = []  # order that the blocks were added for FIFO policy
        self.data: dict[int, CacheBlock] = {}

        self.bus: Bus = bus

    # read a block from cache
    def read(self, address, to_write=False, is_local=False) -> CacheBlock | None:
        block_index = address - (address % self.block_size)
        # search in the cache
        block = self.data.get(block_index)
        if block and block.tag != MESITag.I:
            print("Cache hit!")
            return block  # read hit

        # If it's a local read don't deal with read miss
        if is_local:
            return None

        print("Cache miss!")
        # consider intention to write
        if to_write:
            response = self.broadcast_message(
                SnoopMessage.READ_WITH_INTENT_TO_MODIFY, block_index
            )
        else:
            response = self.broadcast_message(SnoopMessage.READ, block_index)

        # update cache
        if (self.n + 1) > self.n_max:
            removed_addr = self.queue.pop(0)

            self.bus.write_back(removed_addr, self.data[removed_addr].data)
            self.data.pop(removed_addr)
            self.n -= 1

        # read from main memory
        block_from_main = self.bus.read_from_main(block_index)

        # select tag based on response (exclusive or shared)
        tag = MESITag.E
        if response == "shared":
            tag = MESITag.S

        block = CacheBlock(tag, block_from_main)
        self.data[block_index] = block

        self.queue.append(block_index)
        self.n += 1

        return block

    # write a block of data
    def write(self, address, data):
        block = self.read(address, to_write=True)

        if block.tag == MESITag.S:  # type: ignore
            self.broadcast_message(SnoopMessage.INVALIDATE, address)

        index = address % self.block_size
        block.data[index] = data  # type: ignore
        block.tag = MESITag.M  # type: ignore

        block_index = address - (address % self.block_size)
        self.data[block_index] = block  # type: ignore

        return 0

    def handle_snoop_message(self, message, address) -> str:
        block_index = address - (address % self.block_size)
        index = address % self.block_size
        block = self.read(address, is_local=True)

        if message == SnoopMessage.READ:
            # Not in cache or Invalid
            if block == None or block.tag == MESITag.I:
                return "ok"

            # Case Modified
            if block.tag == MESITag.M:
                self.bus.write_back(address, block)
                self.data[block_index].tag = MESITag.S
                return "ok"

            # Case exlclusive
            if block.tag == MESITag.E:
                self.data[block_index].tag = MESITag.S

            # Case exlclusive or shared
            return "shared"

        if message == SnoopMessage.READ_WITH_INTENT_TO_MODIFY:
            # Not in cache or Invalid
            if block == None or block.tag == MESITag.I:
                return "ok"

            if block.tag == MESITag.M:
                self.bus.write_back(address, block)
                return "ok"

            # Invalidate the block in local cache
            self.data[block_index].tag = MESITag.I
            return "ok"

        if message == SnoopMessage.INVALIDATE:
            # Not in cache or Invalid
            if block == None or block.tag == MESITag.I:
                return "ok"

            # Invalidate the block in local cache
            self.data[block_index].tag = MESITag.I
            return "ok"

        return "invalid"

    def broadcast_message(self, message, address):
        return self.bus.broadcast(message, address, self)

    def __str__(self) -> str:
        return "\n".join([f"{addr}: {str(self.data[addr])}" for addr in self.queue])
