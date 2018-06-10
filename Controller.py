class Controller:
    @staticmethod
    def apply_signal(car, signal):
        car.ax = signal.values["ax"]
        car.lane = signal.values["lane"]
        # print(signal.values["ax"], '\t', car.vx)
