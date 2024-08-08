import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont
from enums import BloodType
from mesi_simulator import MESISimulator
from blood_bank.BloodBank import BloodBank


class OutputBox:
    """Handles output logging to a text widget."""

    def __init__(self):
        self.widget = None

    def write(self, message):
        """Writes a message to the attached text widget."""
        if self.widget:
            self.widget.configure(state="normal")
            self.widget.insert(tk.END, message)
            self.widget.configure(state="disabled")
            self.widget.see(tk.END)
        else:
            raise Exception("A text box must be attached before using this function!")

    def attach_text_box(self, text_box):
        """Attaches a text widget to the OutputBox for logging."""
        self.widget = text_box


class BloodBankGUI:
    """GUI class for the Blood Bank simulator using the MESI protocol."""

    def __init__(self, simulator: MESISimulator):
        self.blood_bank = BloodBank(simulator)
        self.main_memory = simulator.main_memory
        self.caches = simulator.caches
        self.MAIN_MEMORY_SIZE = simulator.main_memory.n_lines
        self.tables = []
        self.processor_map = {f"Hospital {i + 1}": i for i in range(len(self.caches))}
        self.output = OutputBox()
        self.root = tk.Tk()
        self.root.title("MESI Simulator")
        self.setup_ui()

    def refresh_tables(self):
        """Refreshes the data displayed in the tables."""
        for table in self.tables:
            table.delete(*table.get_children())

        # Populate main memory table
        for i in range(self.MAIN_MEMORY_SIZE):
            tag = "lightgray" if i % 10 >= 5 else "fixed"
            self.tables[0].insert(
                "", "end", values=(i, self.main_memory.data[i]), tags=(tag,)
            )

        # Populate cache table for the selected hospital
        active_hospital = self.processor_map[self.hospital_combobox.get()]
        for addr in reversed(self.caches[active_hospital].queue):
            data = " | ".join(
                [str(v) for v in self.caches[active_hospital].data[addr].data]
            )
            self.tables[1].insert(
                "",
                "end",
                values=(addr, data, self.caches[active_hospital].data[addr].tag.value),
                tags=("fixed",),
            )

    def use_blood(self):
        """Handles the use blood action."""
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
        """Handles the donate blood action."""
        hospital = self.processor_map[self.hospital_combobox.get()]
        blood_type = self.blood_combobox.get().strip()

        self.output.write(
            f"Hospital {hospital + 1} trying to donate blood of type {blood_type}.\n"
        )
        self.output.write(self.blood_bank.donate_blood(hospital, blood_type))
        self.output.write("\n\n")
        self.refresh_tables()

    def request_blood(self):
        """Handles the request blood action."""
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
        """Sets up the UI components."""
        fixed_font = tkFont.Font(family="Courier New", size=10)
        control_frame = tk.Frame(self.root)
        control_frame.pack(pady=10)

        # Blood type combobox
        tk.Label(control_frame, text="Value:").pack(side=tk.LEFT, padx=5, pady=5)
        blood_options = [str(x) for x in list(BloodType)]
        self.blood_combobox = ttk.Combobox(
            control_frame, values=blood_options, width=4, state="readonly"
        )
        self.blood_combobox.pack(side=tk.LEFT, padx=5, pady=5)
        self.blood_combobox.current(0)

        # Hospital combobox
        tk.Label(control_frame, text="Processor:").pack(side=tk.LEFT, padx=5, pady=5)
        hospital_options = list(self.processor_map.keys())
        self.hospital_combobox = ttk.Combobox(
            control_frame, values=hospital_options, width=12, state="readonly"
        )
        self.hospital_combobox.pack(side=tk.LEFT, padx=5, pady=5)
        self.hospital_combobox.current(0)

        # Action buttons
        tk.Button(control_frame, text="Request Blood", command=self.request_blood).pack(
            side=tk.LEFT, padx=5, pady=5
        )
        tk.Button(control_frame, text="Use Blood", command=self.use_blood).pack(
            side=tk.LEFT, padx=5, pady=5
        )
        tk.Button(control_frame, text="Donate Blood", command=self.donate_blood).pack(
            side=tk.LEFT, padx=5, pady=5
        )

        # Table frame for data display
        table_frame = tk.Frame(self.root)
        table_frame.pack(pady=10)

        # Main memory table
        tk.Label(table_frame, text="Blood Bank").grid(
            row=0, column=0, sticky="n", padx=(15, 0)
        )
        memory_table = ttk.Treeview(
            table_frame, columns=("Col1", "Col2"), show="headings", height=40
        )
        memory_table.heading("Col1", text="Address")
        memory_table.heading("Col2", text="Value")
        memory_table.column("Col1", width=80, anchor="center")
        memory_table.column("Col2", width=80, anchor="center")
        memory_table.grid(
            row=0, column=0, rowspan=2, sticky="nswe", padx=(10, 0), pady=(25, 5)
        )
        memory_table.tag_configure("lightgray", background="#d3d3d3")
        memory_table.tag_configure("fixed", font=fixed_font)
        self.tables.append(memory_table)

        memory_scrollbar = tk.Scrollbar(
            table_frame, orient="vertical", command=memory_table.yview
        )
        memory_scrollbar.grid(
            row=0, column=1, rowspan=2, padx=(0, 5), pady=(25, 5), sticky="ns"
        )
        memory_table.configure(yscrollcommand=memory_scrollbar.set)

        # Cache table for the selected hospital
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

        # Output console
        tk.Label(table_frame, text="Output").grid(
            row=0, column=len(self.caches), sticky="n"
        )
        console = tk.Text(table_frame, wrap="word", width=50)
        console.grid(
            row=0,
            column=len(self.caches),
            rowspan=2,
            sticky="nswe",
            padx=(5, 0),
            pady=(25, 5),
        )
        console_scrollbar = tk.Scrollbar(
            table_frame, orient="vertical", command=console.yview
        )
        console_scrollbar.grid(
            row=0,
            column=len(self.caches) + 1,
            rowspan=2,
            padx=(0, 10),
            pady=(25, 5),
            sticky="ns",
        )
        console.configure(yscrollcommand=console_scrollbar.set)
        self.output.attach_text_box(console)

        self.refresh_tables()

    def mainloop(self):
        """Starts the main loop of the Tkinter application."""
        self.root.mainloop()
