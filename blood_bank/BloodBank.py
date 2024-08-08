from mesi_simulator import MESISimulator


class BloodBank:
    def __init__(self):
        self.bank = MESISimulator()

    def use_blood(self, hospital_id: int, blood_id: int, blood_type_needed):
        data = self.bank.caches[hospital_id].read(blood_id)

        blood_available = data.data[blood_id % 5]  # type: ignore

        if blood_available != blood_type_needed:
            return "Blood requested is not available anymore."

        self.bank.caches[hospital_id].write(blood_id, "E")

        return "Transaction successful."

    def request_blood(self, unit_id: int, blood_id: int):
        data = self.bank.caches[unit_id].read(blood_id)

        return data.data[blood_id % 5]  # type: ignore

    def donate_blood(self, hospital_id: int, blood_id: int, blood_type_donated):
        data = self.bank.caches[hospital_id].read(blood_id)

        blood_available = data.data[blood_id % 5]  # type: ignore

        if blood_available != "E":
            return "This blood unit is not empty anymore, please select another one."

        self.bank.caches[hospital_id].write(blood_id, "E")

        return "Transaction successful."
