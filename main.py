import random
import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont

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
    tables = []

    def refresh_tables():
        for table in tables:
            for item in table.get_children():
                table.delete(item)

        for i in range(0, MAIN_MEMORY_SIZE):
            tables[0].insert("", "end", values=(i, main_memory.data[i]))

        for i in range(1, len(caches) + 1):
            for addr in caches[i - 1].queue:
                data = " | ".join([str(v) for v in caches[i - 1].data[addr].data])
                tables[i].insert(
                    "",
                    "end",
                    values=(
                        addr,
                        data,
                        caches[i - 1].data[addr].tag.value,
                    ),
                    tags=('fixed',)
                )

    # Define the mapping of labels to values
    processor_map = {
        "Processor 1": 0,
        "Processor 2": 1,
        "Processor 3": 2,
        "Processor 4": 3,
    }

    # Function to handle writing to an address
    def write_address():
        address = int(address_entry.get())
        processor = processor_combobox.get()
        value = value_combobox.get()
        # Implement the logic to write to the given address
        print(f"Writing to address: {address}")
        caches[processor_map[processor]].write(address, BloodType(value))
        refresh_tables()

    # Function to handle reading from an address
    def read_address():
        address = int(address_entry.get())
        processor = processor_combobox.get()
        # Implement the logic to read from the given address
        print(f"Reading from address: {address}")
        print(caches[processor_map[processor]].read(address))
        refresh_tables()

    
    root = tk.Tk()
    root.title("MESI Simulator")

    # Create a fixed-width font
    fixed_font = tkFont.Font(family="Courier New", size=10)

    # Create a frame for the address and processor entries and buttons
    control_frame = tk.Frame(root)
    control_frame.pack(pady=10)

    # Entry for address
    address_label = tk.Label(control_frame, text="Endereço:")
    address_label.pack(side=tk.LEFT, padx=5, pady=5)
    address_entry = tk.Entry(control_frame, width=5)
    address_entry.pack(side=tk.LEFT, padx=5, pady=5)

    # Dropdown for value
    value_label = tk.Label(control_frame, text="Valor:")
    value_label.pack(side=tk.LEFT, padx=5, pady=5)
    value_options = [str(x) for x in list(BloodType)]
    value_combobox = ttk.Combobox(control_frame, values=value_options, width=4, state="readonly")
    value_combobox.pack(side=tk.LEFT, padx=5, pady=5)
    value_combobox.current(0)  # Set default selection

    # Dropdown for processor
    processor_label = tk.Label(control_frame, text="Processador:")
    processor_label.pack(side=tk.LEFT, padx=5, pady=5)
    processor_options = ["Processor 1", "Processor 2", "Processor 3", "Processor 4"]
    processor_combobox = ttk.Combobox(control_frame, values=processor_options, width=12, state="readonly")
    processor_combobox.pack(side=tk.LEFT, padx=5, pady=5)
    processor_combobox.current(0)  # Set default selection

    # Write button
    write_button = tk.Button(control_frame, text="Write", command=write_address)
    write_button.pack(side=tk.LEFT, padx=5, pady=5)

    # Read button
    read_button = tk.Button(control_frame, text="Read", command=read_address)
    read_button.pack(side=tk.LEFT, padx=5, pady=5)


    # Create a frame for the table
    table_frame = tk.Frame(root)
    table_frame.pack(pady=10)

    # Create the table
    table = ttk.Treeview(
        table_frame, columns=("Col1", "Col2"), show="headings", height=40
    )
    table.heading("Col1", text="Endereço")
    table.heading("Col2", text="Valor")
    table.column("Col1", width=80, anchor="center")
    table.column("Col2", width=80, anchor="center")
    table.grid(row=0, column=0, rowspan=2, sticky="nswe", padx=10, pady=5)
    table.tag_configure('fixed', font=fixed_font)
    tables.append(table)

    for i in range(len(caches)):
        cache_table = ttk.Treeview(
            table_frame, columns=("Col1", "Col2", "Col3"), show="headings"
        )
        cache_table.heading("Col1", text="Endereço")
        cache_table.heading("Col2", text="Dados")
        cache_table.heading("Col3", text="Tag")
        cache_table.column("Col1", width=80, anchor="center")
        cache_table.column("Col2", width=250, anchor="center")
        cache_table.column("Col3", width=40, anchor="center")
        cache_table.tag_configure('fixed', font=fixed_font)
        cache_table.grid(row=i // 2, column=1 + i % 2, sticky="nswe", padx=10, pady=5)

        tables.append(cache_table)

    refresh_tables()

    # Run the application
    root.mainloop()


if __name__ == "__main__":
    gui()
