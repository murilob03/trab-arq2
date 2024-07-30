import random
import sys
import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont

from main_memory import MainMemory
from bus import Bus
from cache import Cache
from enums import BloodType

# Constants
MAIN_MEMORY_SIZE = 200
CACHE_SIZE = 10
BLOCK_SIZE = 5

# Validate main memory size
if MAIN_MEMORY_SIZE % BLOCK_SIZE != 0:
    raise ValueError("The main memory size must be divisible by the block size!")

# Initialize objects
main_memory = MainMemory(MAIN_MEMORY_SIZE, BLOCK_SIZE)
bus = Bus(main_memory)
caches = [Cache(CACHE_SIZE, BLOCK_SIZE, bus) for _ in range(4)]

# Attach caches to bus
for cache in caches:
    bus.attach_cache(cache)

# Populate main memory with random data
for i in range(0, MAIN_MEMORY_SIZE, BLOCK_SIZE):
    random_block = [random.choice(list(BloodType)) for _ in range(BLOCK_SIZE)]
    main_memory.write(i, random_block)

# Populate caches from main memory
for cache in caches:
    while cache.n < cache.n_max:
        cache.read(random.randint(0, MAIN_MEMORY_SIZE - 1))


def cli_loop():
    """Command-line interface loop for interacting with the memory system."""
    while True:
        command = input(
            "PRINT MAIN (1), PRINT CACHE (2), CACHE READ (3), CACHE WRITE (4), EXIT (5)\n"
        )
        if command == "1":
            print(main_memory)
        elif command == "2":
            cache_n = int(input(f"Select a cache to print (1-{len(caches)})\n")) - 1
            print(caches[cache_n])
        elif command == "3":
            cache_n = int(input(f"Select a cache to read (1-{len(caches)})\n")) - 1
            addr = int(input(f"Select an address to read (0-{MAIN_MEMORY_SIZE})\n"))
            print(str(caches[cache_n].read(addr)))
        elif command == "4":
            cache_n = int(input(f"Select a cache to write (1-{len(caches)})\n")) - 1
            addr = int(input(f"Select an address to write (0-{MAIN_MEMORY_SIZE})\n"))
            value = BloodType(input(f"Enter a value to write\n"))
            caches[cache_n].write(addr, value)
        elif command == "5":
            break


def gui():
    """Graphical user interface for interacting with the memory system."""
    tables = []

    processor_map = {
        "Processor 1": 0,
        "Processor 2": 1,
        "Processor 3": 2,
        "Processor 4": 3,
    }

    class ConsoleOutput:
        def __init__(self, widget):
            self.widget = widget

        def write(self, message):
            self.widget.configure(state="normal")
            self.widget.insert(tk.END, message)
            self.widget.configure(state="disabled")
            self.widget.see(tk.END)

        def flush(self):
            pass

    def refresh_tables():
        for table in tables:
            for item in table.get_children():
                table.delete(item)

        for i in range(MAIN_MEMORY_SIZE):
            tables[0].insert("", "end", values=(i, main_memory.data[i]))

        for i in range(1, len(caches) + 1):
            for addr in reversed(caches[i - 1].queue):
                data = " | ".join([str(v) for v in caches[i - 1].data[addr].data])
                tables[i].insert(
                    "",
                    "end",
                    values=(
                        addr,
                        data,
                        caches[i - 1].data[addr].tag.value,
                    ),
                    tags=("fixed",),
                )

    def write_address():
        address_raw = address_entry.get()
        if (
            not address_raw.isdigit()
            or int(address_raw) < 0
            or int(address_raw) >= MAIN_MEMORY_SIZE
        ):
            print(f"Address must be a number between 0 and {MAIN_MEMORY_SIZE - 1}.")
            return
        address = int(address_raw)
        processor = processor_combobox.get()
        value = value_combobox.get()
        print(f"{processor} writing {value.strip()} to address: {address}")
        caches[processor_map[processor]].write(address, BloodType(value.strip()))
        print()
        refresh_tables()

    def read_address():
        address_raw = address_entry.get()
        if (
            not address_raw.isdigit()
            or int(address_raw) < 0
            or int(address_raw) >= MAIN_MEMORY_SIZE
        ):
            print(f"Address must be a number between 0 and {MAIN_MEMORY_SIZE - 1}.")
            return
        address = int(address_raw)
        processor = processor_combobox.get()
        print(f"{processor} reading on address: {address}")
        index = address % BLOCK_SIZE
        print(caches[processor_map[processor]].read(address).data[index])  # type: ignore
        print()
        refresh_tables()

    def print_queue():
        processor = processor_combobox.get()
        print(caches[processor_map[processor]].queue)

    root = tk.Tk()
    root.title("MESI Simulator")

    fixed_font = tkFont.Font(family="Courier New", size=10)

    control_frame = tk.Frame(root)
    control_frame.pack(pady=10)

    address_label = tk.Label(control_frame, text="Address:")
    address_label.pack(side=tk.LEFT, padx=5, pady=5)
    address_entry = tk.Entry(control_frame, width=5)
    address_entry.pack(side=tk.LEFT, padx=5, pady=5)

    value_label = tk.Label(control_frame, text="Value:")
    value_label.pack(side=tk.LEFT, padx=5, pady=5)
    value_options = [str(x) for x in list(BloodType)]
    value_combobox = ttk.Combobox(
        control_frame, values=value_options, width=4, state="readonly"
    )
    value_combobox.pack(side=tk.LEFT, padx=5, pady=5)
    value_combobox.current(0)

    processor_label = tk.Label(control_frame, text="Processor:")
    processor_label.pack(side=tk.LEFT, padx=5, pady=5)
    processor_options = list(processor_map.keys())
    processor_combobox = ttk.Combobox(
        control_frame, values=processor_options, width=12, state="readonly"
    )
    processor_combobox.pack(side=tk.LEFT, padx=5, pady=5)
    processor_combobox.current(0)

    write_button = tk.Button(control_frame, text="Write", command=write_address)
    write_button.pack(side=tk.LEFT, padx=5, pady=5)

    read_button = tk.Button(control_frame, text="Read", command=read_address)
    read_button.pack(side=tk.LEFT, padx=5, pady=5)

    queue_button = tk.Button(control_frame, text="Queue", command=print_queue)
    queue_button.pack(side=tk.LEFT, padx=5, pady=5)

    table_frame = tk.Frame(root)
    table_frame.pack(pady=10)

    table_label = tk.Label(table_frame, text="Main Memory")
    table_label.grid(row=0, column=0, sticky="n", padx=(15, 0))

    table = ttk.Treeview(
        table_frame, columns=("Col1", "Col2"), show="headings", height=40
    )
    table.heading("Col1", text="Address")
    table.heading("Col2", text="Value")
    table.column("Col1", width=80, anchor="center")
    table.column("Col2", width=80, anchor="center")
    table.grid(row=0, column=0, rowspan=2, sticky="nswe", padx=(10, 0), pady=(25, 5))
    table.tag_configure("fixed", font=fixed_font)

    scrollbar = tk.Scrollbar(table_frame, orient="vertical", command=table.yview)
    scrollbar.grid(row=0, column=1, rowspan=2, padx=(0, 5), pady=(25, 5), sticky="ns")

    table.configure(yscrollcommand=scrollbar.set)
    tables.append(table)

    for i in range(len(caches)):
        cache_table_label = tk.Label(table_frame, text=f"Processor {i + 1}")
        cache_table_label.grid(row=i // 2, column=2 + i % 2, sticky="n")

        cache_table = ttk.Treeview(
            table_frame, columns=("Col1", "Col2", "Col3"), show="headings"
        )
        cache_table.heading("Col1", text="Address")
        cache_table.heading("Col2", text="Data")
        cache_table.heading("Col3", text="Tag")
        cache_table.column("Col1", width=80, anchor="center")
        cache_table.column("Col2", width=250, anchor="center")
        cache_table.column("Col3", width=40, anchor="center")
        cache_table.tag_configure("fixed", font=fixed_font)
        cache_table.grid(
            row=i // 2, column=2 + i % 2, sticky="nswe", padx=5, pady=(25, 5)
        )
        tables.append(cache_table)

    refresh_tables()

    console_label = tk.Label(table_frame, text="Output")
    console_label.grid(row=0, column=4, sticky="n")

    console = tk.Text(table_frame, wrap="word", width=50)
    console.grid(row=0, column=4, rowspan=2, sticky="nswe", padx=(5, 0), pady=(25, 5))

    scrollbar = tk.Scrollbar(table_frame, orient="vertical", command=console.yview)
    scrollbar.grid(row=0, column=5, rowspan=2, padx=(0, 10), pady=(25, 5), sticky="ns")

    console.configure(state="disabled", yscrollcommand=scrollbar.set)

    sys.stdout = ConsoleOutput(console)

    root.mainloop()


if __name__ == "__main__":
    gui()
