from enums import BloodType


class MainMemory:
    def __init__(self, n_lines, block_size) -> None:
        self.n_lines = n_lines
        self.block_size = block_size
        self.data: list[BloodType | None] = [None for _ in range(n_lines)]

    def read(self, address) -> list[BloodType | None]:
        if address >= self.n_lines:
            raise IndexError("Line number exceeds the total number of lines.")

        block_index = address - (address % self.block_size)
        block = self.data[block_index : block_index + self.block_size]
        return block

    def write(self, address, data) -> None:
        if address >= self.n_lines:
            raise IndexError("Line number exceeds the total number of lines.")

        block_index = address - (address % self.block_size)
        for i in range(self.block_size):
            if (block_index + i) < self.n_lines:
                self.data[block_index + i] = data[i]

    def clear(self) -> None:
        self.data: list[BloodType | None] = [None for _ in range(self.n_lines)]

    def __str__(self) -> str:
        blocks = [
            self.data[i : i + self.block_size]
            for i in range(0, self.n_lines, self.block_size)
        ]

        for i in range(len(blocks)):
            blocks[i][0] = f"{i * self.block_size}: {blocks[i][0]}"  # type: ignore

        text = "\n".join([" | ".join([str(x) for x in block]) for block in blocks])
        return text
