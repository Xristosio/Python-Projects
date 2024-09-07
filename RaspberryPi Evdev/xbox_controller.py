from evdev import InputDevice

def main():
    dev = InputDevice('/dev/input/event1')
    print(dev)

    print("Περιμένω εισόδους από το χειριστήριο...")
    for event in dev.read_loop():
        print(event)

if __name__ == "__main__":
    main()
