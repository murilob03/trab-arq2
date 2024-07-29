import random
import tkinter as tk
from tkinter import ttk

from main_memory import MainMemory
from bus import Bus
from cache import Cache
from enums import BloodType

MAIN_MEMORY_SIZE = 200
CACHE_SIZE = 6
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


def cli_loop():
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


def gui():
    # Function to handle writing to an address
    def write_address():
        address = address_entry.get()
        # Implement the logic to write to the given address
        print(f"Writing to address: {address}")

    # Function to handle reading from an address
    def read_address():
        address = address_entry.get()
        # Implement the logic to read from the given address
        print(f"Reading from address: {address}")

    root = tk.Tk()
    root.title("MESI Simulator")

    # Create a frame for the address and processor entries and buttons
    control_frame = tk.Frame(root)
    control_frame.pack(pady=10)

    # Entry for address
    address_label = tk.Label(control_frame, text="Endereço:")
    address_label.grid(row=0, column=0, padx=5, pady=5)
    address_entry = tk.Entry(control_frame, width=20)
    address_entry.grid(row=0, column=1, padx=5, pady=5)

    # Dropdown for processor
    processor_label = tk.Label(control_frame, text="Processador:")
    processor_label.grid(row=0, column=2, padx=5, pady=5)
    processor_options = ["Processor 1", "Processor 2", "Processor 3", "Processor 4"]
    processor_combobox = ttk.Combobox(
        control_frame, values=processor_options, width=18, state="readonly"
    )
    processor_combobox.grid(row=0, column=3, padx=5, pady=5)
    processor_combobox.current(0)  # Set default selection

    # Write button
    write_button = tk.Button(control_frame, text="Write", command=write_address)
    write_button.grid(row=0, column=4, padx=5, pady=5)

    # Read button
    read_button = tk.Button(control_frame, text="Read", command=read_address)
    read_button.grid(row=0, column=5, padx=5, pady=5)

    # Create a frame for the table
    table_frame = tk.Frame(root)
    table_frame.pack(pady=10)

    # Create the table
    table1 = ttk.Treeview(
        table_frame, columns=("Col1", "Col2"), show="headings", height=40
    )
    table1.heading("Col1", text="Endereço")
    table1.heading("Col2", text="Valor")
    table1.column("Col1", width=80, anchor="center")
    table1.column("Col2", width=80, anchor="center")
    table1.grid(row=0, column=0, rowspan=2, sticky="nswe", padx=10, pady=5)

    for i in range(0, MAIN_MEMORY_SIZE):
        table1.insert("", "end", values=(i, main_memory.data[i]))

    for i in range(len(caches)):
        cache_table = ttk.Treeview(
            table_frame, columns=("Col1", "Col2", "Col3"), show="headings"
        )
        cache_table.heading("Col1", text="Endereço")
        cache_table.heading("Col2", text="Dados")
        cache_table.heading("Col3", text="Tag")
        cache_table.column("Col1", width=80, anchor="center")
        cache_table.column("Col2", width=120, anchor="center")
        cache_table.column("Col3", width=80, anchor="center")
        cache_table.grid(row=i // 2, column=1 + i % 2, sticky="nswe", padx=10, pady=5)

        for addr in caches[i].queue:
            cache_table.insert(
                "",
                "end",
                values=(
                    addr,
                    [str(v) for v in caches[i].data[addr].data],
                    caches[i].data[addr].tag.value,
                ),
            )

    # Run the application
    root.mainloop()


if __name__ == "__main__":
    gui()
