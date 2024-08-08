import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont
import sys

from enums import BloodType
from mesi_simulator import MESISimulator


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


class BloodBankGUI:
    def __init__(self, simulator: MESISimulator):
        self.main_memory = simulator.main_memory
        self.caches = simulator.caches
        self.MAIN_MEMORY_SIZE = simulator.main_memory.n_lines
        self.BLOCK_SIZE = simulator.main_memory.block_size

        self.tables = []
        self.processor_map = {}
        for i in range(len(self.caches)):
            self.processor_map[f"Hospital {i + 1}"] = i

        self.root = tk.Tk()
        self.root.title("MESI Simulator")

        self.setup_ui()

    def refresh_tables(self, event):
        for table in self.tables:
            for item in table.get_children():
                table.delete(item)

        for i in range(self.MAIN_MEMORY_SIZE):
            self.tables[0].insert("", "end", values=(i, self.main_memory.data[i]))

        active_hospital = self.processor_map[self.processor_combobox.get()]
        for addr in reversed(self.caches[active_hospital].queue):
            data = " | ".join([str(v) for v in self.caches[active_hospital].data[addr].data])
            self.tables[1].insert(
                "",
                "end",
                values=(
                    addr,
                    data,
                    self.caches[active_hospital].data[addr].tag.value,
                ),
                tags=("fixed",),
            )

    def write_address(self):
        address_raw = self.address_entry.get()
        if (
            not address_raw.isdigit()
            or int(address_raw) < 0
            or int(address_raw) >= self.MAIN_MEMORY_SIZE
        ):
            print(
                f"Address must be a number between 0 and {self.MAIN_MEMORY_SIZE - 1}."
            )
            return
        address = int(address_raw)
        processor = self.processor_combobox.get()
        value = self.value_combobox.get()
        print(f"{processor} writing {value.strip()} to address: {address}")
        self.caches[self.processor_map[processor]].write(
            address, BloodType(value.strip())
        )
        print()
        self.refresh_tables()

    def read_address(self):
        address_raw = self.address_entry.get()
        if (
            not address_raw.isdigit()
            or int(address_raw) < 0
            or int(address_raw) >= self.MAIN_MEMORY_SIZE
        ):
            print(
                f"Address must be a number between 0 and {self.MAIN_MEMORY_SIZE - 1}."
            )
            return
        address = int(address_raw)
        processor = self.processor_combobox.get()
        print(f"{processor} reading on address: {address}")
        index = address % self.BLOCK_SIZE
        print(self.caches[self.processor_map[processor]].read(address).data[index])  # type: ignore
        print()
        self.refresh_tables()

    def print_queue(self):
        processor = self.processor_combobox.get()
        print(self.caches[self.processor_map[processor]].queue)

    def setup_ui(self):
        fixed_font = tkFont.Font(family="Courier New", size=10)

        control_frame = tk.Frame(self.root)
        control_frame.pack(pady=10)

        address_label = tk.Label(control_frame, text="Address:")
        address_label.pack(side=tk.LEFT, padx=5, pady=5)
        self.address_entry = tk.Entry(control_frame, width=5)
        self.address_entry.pack(side=tk.LEFT, padx=5, pady=5)

        value_label = tk.Label(control_frame, text="Value:")
        value_label.pack(side=tk.LEFT, padx=5, pady=5)
        value_options = [str(x) for x in list(BloodType)]
        self.value_combobox = ttk.Combobox(
            control_frame, values=value_options, width=4, state="readonly"
        )
        self.value_combobox.pack(side=tk.LEFT, padx=5, pady=5)
        self.value_combobox.current(0)

        processor_label = tk.Label(control_frame, text="Processor:")
        processor_label.pack(side=tk.LEFT, padx=5, pady=5)
        processor_options = list(self.processor_map.keys())
        self.processor_combobox = ttk.Combobox(
            control_frame, values=processor_options, width=12, state="readonly"
        )
        self.processor_combobox.pack(side=tk.LEFT, padx=5, pady=5)
        self.processor_combobox.current(0)

        write_button = tk.Button(
            control_frame, text="Write", command=self.write_address
        )
        write_button.pack(side=tk.LEFT, padx=5, pady=5)

        read_button = tk.Button(control_frame, text="Read", command=self.read_address)
        read_button.pack(side=tk.LEFT, padx=5, pady=5)

        queue_button = tk.Button(control_frame, text="Queue", command=self.print_queue)
        queue_button.pack(side=tk.LEFT, padx=5, pady=5)

        table_frame = tk.Frame(self.root)
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
        table.grid(
            row=0, column=0, rowspan=2, sticky="nswe", padx=(10, 0), pady=(25, 5)
        )
        table.tag_configure("fixed", font=fixed_font)

        scrollbar = tk.Scrollbar(table_frame, orient="vertical", command=table.yview)
        scrollbar.grid(
            row=0, column=1, rowspan=2, padx=(0, 5), pady=(25, 5), sticky="ns"
        )

        table.configure(yscrollcommand=scrollbar.set)
        self.tables.append(table)

        active_hospital = self.processor_map[self.processor_combobox.get()]

        cache_table_label = tk.Label(
            table_frame, text=f"Hospital {active_hospital + 1}"
        )
        cache_table_label.grid(row=0, column=2, sticky="n")

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
        cache_table.grid(row=0, column=2, sticky="nswe", padx=5, pady=(25, 5))
        self.tables.append(cache_table)

        self.processor_combobox.bind("<<ComboboxSelected>>", self.refresh_tables)
        self.refresh_tables()

        console_label = tk.Label(table_frame, text="Output")
        console_label.grid(row=0, column=len(self.caches), sticky="n")

        console = tk.Text(table_frame, wrap="word", width=50)
        console.grid(
            row=0,
            column=len(self.caches),
            rowspan=2,
            sticky="nswe",
            padx=(5, 0),
            pady=(25, 5),
        )

        scrollbar = tk.Scrollbar(table_frame, orient="vertical", command=console.yview)
        scrollbar.grid(
            row=0,
            column=len(self.caches) + 1,
            rowspan=2,
            padx=(0, 10),
            pady=(25, 5),
            sticky="ns",
        )

        console.configure(state="disabled", yscrollcommand=scrollbar.set)

        sys.stdout = ConsoleOutput(console)

    def mainloop(self):
        self.root.mainloop()
