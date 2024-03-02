import subprocess
import time
import signal
import sys

# Frequencies (in Hz) to scan: 433.92 MHz, 868 MHz, 915 MHz
# frequencies = [433920000, 868000000, 915000000]


# Generate a list of frequencies in 1MHz spacing to scan
def generate_frequencies(start=345000000, end=440000000, step=1000000):
    return list(range(start, end + step, step))


# Handle Ctrl-C gracefully
def signal_handler(signal, frame):
    print('Exiting...')
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)


def run_rtl_433(freq, interval=30):
    # Construct the rtl_433 command with -G to enable all protocols
    cmd = ['rtl_433', '-f', str(freq), '-G', '4', '-S', 'all', '-T', '30']
    print(f"Running {' '.join(cmd)}")
    try:
        # Run the command and wait for it to complete
        subprocess.run(cmd)
    except subprocess.CalledProcessError as e:
        print(f"rtl_433 exited with error: {e}")


def main():
    frequencies = generate_frequencies()
    interval = 30  # seconds
    # calculate seconds to run the command and convert to minutes
    totaltime = interval * frequencies.__len__() / 60
    print(f"List has: {frequencies.__len__()} number of frequencies to scan. {interval} seconds each.")
    print(f"Total time to run: {totaltime} minutes list of qty of frequencies: {frequencies.__len__()}")
    for freq in frequencies:
        run_rtl_433(freq)


if __name__ == '__main__':
    while True:
        main()
