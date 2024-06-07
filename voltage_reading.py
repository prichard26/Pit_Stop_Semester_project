import serial
import threading
import time

# Configuration for serial port
arduino_port = "/dev/tty.usbmodem11201"  # Replace with the correct port for macOS
# For Raspberry Pi, you would use something like '/dev/ttyACM0' or '/dev/ttyUSB0'
baud_rate = 9600  # Ensure this matches the baud rate set on your Arduino

file_name = "analog-data.csv"  # Name of the CSV file to be generated
print_labels = False  # Whether to print out line IDs to the terminal

def read_from_arduino():
    """Function to continuously read from the Arduino."""
    while not stop_thread:
        if ser.in_waiting > 0:
            data = ser.readline().decode('utf-8').strip()
            with open(file_name, "a") as file:
                file.write(data + "\n")
                if print_labels:
                    print("Line: writing...")

def wait_for_enter():
    """Function to wait for the user to press Enter to stop the data collection."""
    global stop_thread
    input("Press Enter to stop data collection...")
    stop_thread = True

def main():
    global stop_thread, ser
    stop_thread = False

    # Initialize serial connection
    ser = serial.Serial(arduino_port, baud_rate)
    print("Connected to Arduino port:" + arduino_port)
    time.sleep(2)  # Wait for the connection to be established

    # Open the file for writing
    with open(file_name, "w") as file:
        print("File created")

    # Start the thread that will read from Arduino
    read_thread = threading.Thread(target=read_from_arduino)
    read_thread.start()

    # Start the thread that waits for the user to press Enter
    enter_thread = threading.Thread(target=wait_for_enter)
    enter_thread.start()

    # Wait for the Enter thread to finish, then signal the read thread to stop
    enter_thread.join()
    stop_thread = True
    read_thread.join()

    # Close the serial connection
    ser.close()
    print("Data collection complete!")

if __name__ == "__main__":
    main()
