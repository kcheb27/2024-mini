from machine import Pin
import time
import random
import json
import requests  # Ensure 'requests' is installed correctly
import network

N: int = 3
sample_ms = 10.0
on_ms = 500

# Firebase URL
dataBaseURL = "https://raspberry-pi-pico-miniproject-default-rtdb.firebaseio.com/response_times.json"

def upload_to_firebase(data: dict):
    jsonData = json.dumps(data)  # Correcting json.dump to json.dumps
    try:
        response = requests.post(dataBaseURL, data=jsonData)
        # Check for successful upload
        if response.status_code == 200:
            print("Data uploaded successfully.")
        else:
            print(f"Failed to upload data. Status code: {response.status_code}")
    except Exception as e:
        print(f"An error occurred while uploading data: {e}")

def random_time_interval(tmin: float, tmax: float) -> float:
    """return a random time interval between max and min"""
    return random.uniform(tmin, tmax)

def blinker(N: int, led: Pin) -> None:
    # Let user know game started / is over
    for _ in range(N):
        led.high()
        time.sleep(0.1)
        led.low()
        time.sleep(0.1)

def write_json(json_filename: str, data: dict) -> None:
    """Writes data to a JSON file."""
    with open(json_filename, "w") as f:
        json.dump(data, f)

def scorer(t: list[int | None]) -> None:
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    ssid = "MYSSID"
    password = "MYPSWD"
    # Connect to the specified network
    wlan.connect(ssid, password)
    A
    # Wait for the connection to be established
    max_wait = 10
    while max_wait > 0:
        if wlan.status() < 0 or wlan.status() >= 3:
            break
        max_wait -= 1
        print('Waiting for connection...')
        time.sleep(1)
    
    # Handle connection result
    if wlan.status() != 3:
        raise RuntimeError('Network connection failed')
    else:
        print('Connected')
        status = wlan.ifconfig()
        print('IP Address:', status[0])
    # Collate results
    misses = t.count(None)
    print(f"You missed the light {misses} / {len(t)} times")

    t_good = [x for x in t if x is not None]
    print(t_good)

    avg = sum(t_good) / len(t_good) if t_good else 0
    maximum = max(t_good) if t_good else None
    minimum = min(t_good) if t_good else None

    data = {
        "minimum": minimum,
        "maximum": maximum,
        "avg": avg,
        "score": (len(t) - misses) / len(t)
    }

    # Upload data to Firebase
    upload_to_firebase(data)

    # Make dynamic filename and write JSON
    now: tuple[int] = time.localtime()
    now_str = "-".join(map(str, now[:3])) + "T" + "_".join(map(str, now[3:6]))
    filename = f"score-{now_str}.json"

    print("write", filename)
    print(data)

    write_json(filename, data)

if __name__ == "__main__":
    # using "if __name__" allows us to reuse functions in other script files
    led = Pin(6, Pin.OUT)
    button = Pin(16, Pin.IN, Pin.PULL_UP)

    t: list[int | None] = []

    blinker(3, led)

    for i in range(N):
        time.sleep(random_time_interval(0.5, 5.0))

        led.high()
        tic = time.ticks_ms()
        t0 = None
        while time.ticks_diff(time.ticks_ms(), tic) < on_ms:
            if button.value() == 0:
                t0 = time.ticks_diff(time.ticks_ms(), tic)
                led.low()
                break
        t.append(t0)
        led.low()

    blinker(5, led)

        
    scorer(t)

