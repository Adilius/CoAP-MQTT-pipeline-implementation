import random

# Sensor class
class sensor():
    # Initialize mean, sigma, and starting value of sensor generation
    def __init__(self):
        self.mean = 20
        self.sigma = 2
        self.value = 22

    # Get a new sensor data
    def get_sensor_data(self):

        # Get current value
        current_value = self.value
        new_value = self.value

        # Assign new value
        while new_value == current_value:
            new_value = int(random.gauss(self.mean, self.sigma))

        # Update & return new value 
        self.value = new_value
        new_value = str(new_value)
        return new_value.encode('utf-8')

# Test that sensor data generation works
if __name__ == '__main__':
    sens = sensor()
    for _ in range(100):
        print(sens.get_sensor_data())

