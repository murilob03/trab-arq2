from mesi_simulator import MESISimulator
from enums import BloodType


class BloodBank:
    def __init__(self, simulator: MESISimulator):
        self.mesi_simulator = simulator

    def use_blood(self, hospital_id: int, blood_id: int, blood_type_needed):
        if blood_type_needed == "E":
            return "You can't use blood from an empty bag!"
        data = self.mesi_simulator.caches[hospital_id].read(blood_id)

        blood_available = data.data[blood_id % 5]  # type: ignore

        if blood_available.value != blood_type_needed:  # type: ignore
            return "Blood requested is not available anymore."

        self.mesi_simulator.caches[hospital_id].write(blood_id, BloodType("E"))

        return "Transaction successful."

    def request_blood(self, unit_id: int, blood_id: int):
        data = self.mesi_simulator.caches[unit_id].read(blood_id)

        blood_type = data.data[blood_id % 5].value  # type: ignore
        if blood_type != "E":  # type: ignore
            return f"The type of the blood in bag {blood_id} is {blood_type}."
        else:
            return f"The bag number {blood_id} is empty."

    def donate_blood(self, hospital_id: int, blood_donated):
        # Try to find an empty bag
        addr = 0
        block = self.mesi_simulator.caches[hospital_id].read(addr)
        found = False
        while addr < self.mesi_simulator.main_memory.n_lines - 4:
            if BloodType("E") in block.data:
                found = True
                break
            addr += 5
            block = self.mesi_simulator.caches[hospital_id].read(addr)

        if not found:
            return "The bank is out of empty bags!"

        for i in range(len(block.data)):
            if block.data[i].value == "E":
                addr += i
                break

        self.mesi_simulator.caches[hospital_id].write(addr, BloodType(blood_donated))

        return f"Blood accepted at bag number {addr}."
