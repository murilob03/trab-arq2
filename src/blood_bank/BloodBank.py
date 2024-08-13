from src.mesi_simulator import MESISimulator
from src.enums import BloodType


class BloodBank:
    """Handles blood bank operations using the MESI protocol."""

    def __init__(self, simulator: MESISimulator):
        self.mesi_simulator = simulator

    def use_blood(self, hospital_id: int, blood_id: int, required_blood_type: str):
        """Uses blood from a specified bag if it matches the needed type."""
        if required_blood_type == "E":
            return "You can't use blood from an empty bag!"

        data = self.mesi_simulator.caches[hospital_id].read(blood_id)
        available_blood = data.data[blood_id % 5]  # type: ignore

        if available_blood.value != required_blood_type:  # type: ignore
            return "Blood requested is not available anymore."

        self.mesi_simulator.caches[hospital_id].write(blood_id, BloodType("E"))
        return "Transaction successful."

    def request_blood(self, hospital_id: int, blood_id: int):
        """Requests the type of blood in a specified bag."""
        data = self.mesi_simulator.caches[hospital_id].read(blood_id)
        blood_type = data.data[blood_id % 5].value  # type: ignore

        if blood_type != "E":  # type: ignore
            return f"The type of the blood in bag {blood_id} is {blood_type}."
        return f"The bag number {blood_id} is empty."

    def donate_blood(self, hospital_id: int, donated_blood_type: str):
        """Donates blood to an empty bag in the bank."""
        empty_bag_address = self._find_empty_bag(hospital_id)
        if empty_bag_address is None:
            return "The bank is out of empty bags!"

        self.mesi_simulator.caches[hospital_id].write(
            empty_bag_address, BloodType(donated_blood_type)
        )
        return f"Blood accepted at bag number {empty_bag_address}."

    def _find_empty_bag(self, hospital_id: int):
        """Finds an empty bag address in the blood bank."""
        for addr in range(0, self.mesi_simulator.main_memory.n_lines, 5):
            block = self.mesi_simulator.caches[hospital_id].read(addr)
            if BloodType("E") in block.data:  # type: ignore
                for i, blood in enumerate(block.data):  # type: ignore
                    if blood.value == "E":  # type: ignore
                        return addr + i
        return None
