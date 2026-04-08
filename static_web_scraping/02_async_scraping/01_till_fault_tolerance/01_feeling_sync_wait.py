import time

def fetch(name,seconds):
    print(f"{name}, start.")
    time.sleep(seconds)
    print(f"{name} end.")

start = time.time()

fetch("A",2)
fetch("C",2)
fetch("B",2)

print(f"total time: {time.time() - start}") # total time  =  6.0..... secs

