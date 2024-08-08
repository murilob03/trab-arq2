from mesi_simulator import MESISimulator
from blood_bank.BloodBankGUI import BloodBankGUI

simulator = MESISimulator()
simulator.populate_main_memory()
simulator.populate_caches()

gui = BloodBankGUI(simulator)
gui.mainloop()