
# Started: some random afternoon, finished much later than planned
import requests, sys
from colorama import Fore, init
from time import sleep

# forgot why I imported sys but might need it later
init(autoreset=True)  # important — without this your terminal looks like a rainbow after exit

API_KEY = "bf2b99cba7de9b6b74063d7c31967bee"   # TODO: should move this to env variables (future me's problem)

# Old test variable I didn’t delete
debug_mode = False  # set True if you want more print outputs

def fetch_weather(city_name):
    """
    Fetches weather info from OpenWeatherMap.
    I know it's missing docstring format but shhh.
    """
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    
    # added metric units because Fahrenheit is confusing
    params = {"q": city_name, "appid": API_KEY, "units": "metric"}
    
    try:
        r = requests.get(base_url, params=params)  # should maybe add timeout but meh
        data = r.json()

        # debugging leftover
        if debug_mode:
            print("DEBUG:", data)

        if r.status_code == 200:
            temp = data["main"]["temp"]          # was tempC before, renamed for no reason
            humid = data["main"]["humidity"]
            cond = data["weather"][0]["description"]
            cname = data["name"]                 # oh wow, API corrects city names
            country = data["sys"]["country"]

            # inconsistent print formatting (intentional)
            print(Fore.CYAN + f"\nWeather in {cname}, {country}")
            print(Fore.YELLOW + f"Temperature: {temp}°C")
            print(Fore.BLUE, "Humidity:", humid, "%")
            print(Fore.MAGENTA + f"Condition: {cond.capitalize()}")
            # could add wind speed but don’t feel like it
        else:
            # API sends lowercase msgs
            msg = data.get("message", "Weird error, try again.")
            print(Fore.RED + "Error:", msg)

    except requests.exceptions.ConnectionError:
        print(Fore.RED + "No internet? Or maybe API down.")
    except Exception as e:
        print(Fore.RED + f"Unexpected crash: {e}")  # not fixing, just printing


def main():
    print(Fore.GREEN + "=== Weather Terminal App ===")
    print("(Type exit to quit)\n")

    while True:
        # this part could be cleaner but works fine
        city = input("Enter city: ").strip()

        # weird input cases
        if not city:
            print("...you didn't type anything.")
            continue
        
        if city.lower() in ["exit", "quit", "bye", "q"]:
            print("Closing app...")
            sleep(0.4)  # purely for dramatic effect
            break

        if len(city) == 1:
            print("City name too short. Try again.")
            continue

        fetch_weather(city)


# always keep this or importing will cause chaos
if __name__ == "__main__":
    # Random warm-up print
    if debug_mode:
        print("Starting in debug mode...")
    main()
