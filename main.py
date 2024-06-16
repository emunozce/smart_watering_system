import time
import requests
import serial
import boto3
import resend

# Open the serial port
ser = serial.Serial("COM6", 9600)  # Replace 'COM3' with your Arduino's serial port
time.sleep(2)  # Wait for the serial connection to initialize

# Define the endpoint URL
url = "https://6qotkczdj9.execute-api.us-east-1.amazonaws.com/Dev/post_data"


def read_from_serial():
    try:
        while True:
            if ser.in_waiting > 0:
                # Read data from serial
                data = ser.readline().decode("utf-8").strip()

                # Split the data into its parts
                temperature, humidity, soil_moisture, ldr_value = data.split(",")

                # Print the received data
                print(f"Temperature: {temperature}°C")
                print(f"Humidity: {humidity}%")
                print(f"LDR Value: {ldr_value}")
                print(f"Soil Moisture: {soil_moisture}")

                # Print the received data
                print(f"LDR Value: {ldr_value}")
                print(f"Temperature: {temperature}°C")
                print(f"Humidity: {humidity}%")
                print(f"Soil Moisture: {soil_moisture}")

                payload = {
                    "hum_amb": float(humidity),
                    "hum_tierra": int(soil_moisture),
                    "temp_amb": float(temperature),
                    "luz": int(ldr_value),
                }

                response = requests.post(url, json=payload, timeout=3000)

                print(f"Response Status Code: {response.status_code}")
                print(f"Response Body: {response.text}")

                resend.api_key = "re_Y2bSb3Ya_PAByFhtBrJqpw1bEHSqY2Lgk"

                r = resend.Emails.send(
                    {
                        "from": "onboarding@resend.dev",
                        "to": "pablo.martinez@edu.uaa.mx",
                        "subject": "Monitor ambiental inteligente",
                        "html": "<p>Checa los datos de tu planta</p><a>https://plant-proyect.onrender.com</a>",
                    }
                )
                # Add any additional processing of the data here

                # Delay for a bit before reading the next set of data
                time.sleep(3)
    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        ser.close()


if __name__ == "__main__":
    read_from_serial()
