# CASCADE FSW
# Main executable

# Import main process
from process import Process

def something():
    for i in range(20):
        print(f"something: {i}")

if __name__ == "__main__":
    # Initialize the main process
    cascade = Process()

    cascade.add(something)
    cascade.add(something)

    # Execute the main process
    cascade.run()