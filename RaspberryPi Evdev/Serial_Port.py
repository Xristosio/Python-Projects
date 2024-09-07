import serial

# Set up the Bluetooth server serial port
bluetooth_port = '/dev/rfcomm0'  # Bluetooth serial port
baud_rate = 9600

# Open the Bluetooth serial port
bluetooth_serial = serial.Serial(bluetooth_port, baud_rate)

print("Waiting for incoming Bluetooth connections...")

# Receive data from the Bluetooth client
while True:
    received_data = bluetooth_serial.readline().decode().rstrip()
    print("Received:", received_data)

    # Check if the received message is 'exit' to end the program
    if received_data == "exit":
        break

    # Send a message to the Bluetooth client
    message = input("Enter a message to send: ")
    bluetooth_serial.write(message.encode())

# Close the Bluetooth serial port
bluetooth_serial.close()
print("Bluetooth connection closed.")
