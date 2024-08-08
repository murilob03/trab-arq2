from mesi_gui import MESISimulatorGUI, MESISimulator


simulator = MESISimulator(n_caches=6)
simulator.populate_main_memory()
simulator.populate_caches()

gui = MESISimulatorGUI(simulator)
gui.mainloop()
