import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont
import sys

from enums import BloodType
from mesi_simulator import MESISimulator
from blood_bank.BloodBank import BloodBank


class OutputBox:
    def __init__(self):
        self.widget = None

    def write(self, message):
        self.widget.configure(state="normal")
        self.widget.insert(tk.END, message)
        self.widget.configure(state="disabled")
        self.widget.see(tk.END)

    def attach_text_box(self, text_box):
        self.widget = text_box


class BloodBankGUI:
    def __init__(self, simulator: MESISimulator):
        self.blood_bank = BloodBank(simulator)

        self.main_memory = simulator.main_memory
        self.caches = simulator.caches
        self.MAIN_MEMORY_SIZE = simulator.main_memory.n_lines
        self.BLOCK_SIZE = simulator.main_memory.block_size

        self.tables = []
        self.processor_map = {}
        for i in range(len(self.caches)):
            self.processor_map[f"Hospital {i + 1}"] = i

        self.output = OutputBox()

        self.root = tk.Tk()
        self.root.title("MESI Simulator")

        self.setup_ui()

    def refresh_tables(self):
        for table in self.tables:
            for item in table.get_children():
                table.delete(item)

        for i in range(self.MAIN_MEMORY_SIZE):
            if i % 10 < 5:
                self.tables[0].insert(
                    "", "end", values=(i, self.main_memory.data[i]), tags=("fixed")
                )
            else:
                self.tables[0].insert(
                    "",
                    "end",
                    values=(i, self.main_memory.data[i]),
                    tags=("lightgray", "fixed"),
                )

        active_hospital = self.processor_map[self.hospital_combobox.get()]
        for addr in reversed(self.caches[active_hospital].queue):
            data = " | ".join(
                [str(v) for v in self.caches[active_hospital].data[addr].data]
            )
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

    def use_blood(self):
        hospital = self.processor_map[self.hospital_combobox.get()]

        selected_item = self.tables[0].selection()[0]
        values = self.tables[0].item(selected_item, "values")
        blood_id = int(values[0])
        blood_type = values[1].strip()

        self.output.write(
            f"Hospital {hospital + 1} trying to use blood {blood_type} from bag {blood_id}.\n"
        )
        self.output.write(self.blood_bank.use_blood(hospital, blood_id, blood_type))
        self.output.write("\n\n")
        self.refresh_tables()

    def donate_blood(self):
        hospital = self.processor_map[self.hospital_combobox.get()]
        blood_type = self.blood_combobox.get().strip()

        self.output.write(
            f"Hospital {hospital + 1} trying to donate blood of type {blood_type}.\n"
        )
        self.output.write(self.blood_bank.donate_blood(hospital, blood_type))
        self.output.write("\n\n")

        self.refresh_tables()

    def request_blood(self):
        hospital = self.processor_map[self.hospital_combobox.get()]

        selected_item = self.tables[0].selection()[0]
        values = self.tables[0].item(selected_item, "values")
        blood_id = int(values[0])

        self.output.write(
            f"Hospital {hospital + 1} requesting the blood type from bag number {blood_id}.\n"
        )
        self.output.write(self.blood_bank.request_blood(hospital, blood_id))
        self.output.write("\n\n")
        self.refresh_tables()

    def setup_ui(self):
        fixed_font = tkFont.Font(family="Courier New", size=10)

        control_frame = tk.Frame(self.root)
        control_frame.pack(pady=10)

        blood_label = tk.Label(control_frame, text="Value:")
        blood_label.pack(side=tk.LEFT, padx=5, pady=5)
        blood_options = [str(x) for x in list(BloodType)]
        self.blood_combobox = ttk.Combobox(
            control_frame, values=blood_options, width=4, state="readonly"
        )
        self.blood_combobox.pack(side=tk.LEFT, padx=5, pady=5)
        self.blood_combobox.current(0)

        hospital_label = tk.Label(control_frame, text="Processor:")
        hospital_label.pack(side=tk.LEFT, padx=5, pady=5)
        hospital_options = list(self.processor_map.keys())
        self.hospital_combobox = ttk.Combobox(
            control_frame, values=hospital_options, width=12, state="readonly"
        )
        self.hospital_combobox.pack(side=tk.LEFT, padx=5, pady=5)
        self.hospital_combobox.current(0)

        request_blood = tk.Button(
            control_frame, text="Request Blood", command=self.request_blood
        )
        request_blood.pack(side=tk.LEFT, padx=5, pady=5)

        use_blood_button = tk.Button(
            control_frame, text="Use Blood", command=self.use_blood
        )
        use_blood_button.pack(side=tk.LEFT, padx=5, pady=5)

        donate_button = tk.Button(
            control_frame, text="Donate Blood", command=self.donate_blood
        )
        donate_button.pack(side=tk.LEFT, padx=5, pady=5)

        table_frame = tk.Frame(self.root)
        table_frame.pack(pady=10)

        table_label = tk.Label(table_frame, text="Blood Bank")
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
        table.tag_configure("lightgray", background="#d3d3d3")
        table.tag_configure("fixed", font=fixed_font)

        scrollbar = tk.Scrollbar(table_frame, orient="vertical", command=table.yview)
        scrollbar.grid(
            row=0, column=1, rowspan=2, padx=(0, 5), pady=(25, 5), sticky="ns"
        )

        table.configure(yscrollcommand=scrollbar.set)
        self.tables.append(table)

        active_hospital = self.processor_map[self.hospital_combobox.get()]

        cache_table_label = tk.Label(
            table_frame, text=f"Hospital {active_hospital + 1} Cache"
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
        cache_table.grid(
            rowspan=2, row=0, column=2, sticky="nswe", padx=5, pady=(25, 5)
        )
        self.tables.append(cache_table)

        def on_combobox_change(event):
            cache_table_label.config(text=f"{self.hospital_combobox.get()} Cache")
            self.refresh_tables()

        self.hospital_combobox.bind("<<ComboboxSelected>>", on_combobox_change)
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

        self.output.attach_text_box(console)

    def mainloop(self):
        self.root.mainloop()
