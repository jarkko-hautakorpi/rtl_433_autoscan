import subprocess
import time
import signal
import sys
import argparse


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
    cmd = ['rtl_433', '-f', str(freq), '-G', '4', '-S', 'all', '-T', str(interval)]
    print(f"Running {' '.join(cmd)}")
    try:
        # Run the command and wait for it to complete
        subprocess.run(cmd)
    except subprocess.CalledProcessError as e:
        print(f"rtl_433 exited with error: {e}")


def main():
    # Create the parser
    parser = argparse.ArgumentParser(description="example: python3 start_autoscan.py 30 345000000 440000000 1000000")

    # Add arguments
    parser.add_argument('--sec', type=int, default=30,
                        help='Time in seconds (default: 30)')
    parser.add_argument('--start', type=int, default=345000000,
                        help='Starting frequency (default: 345000000)')
    parser.add_argument('--stop', type=int, default=440000000,
                        help='End frequency (default: 440000000)')
    parser.add_argument('--step', type=int, default=1000000,
                        help='Frequency step (default: 1000000)')

    # Parse arguments
    args = parser.parse_args()

    # If the first command line parameter is given, use it as a number and use it as the interval of seconds
    interval = args.sec
    frequencies = generate_frequencies(args.start, args.stop, args.step)
    # calculate seconds to run the command and convert to minutes
    totaltime = interval * frequencies.__len__() / 60
    print(f"*")
    print(f"* List has: {frequencies.__len__()} frequencies to scan. {interval} seconds each.")
    print(f"* Total time to run: {totaltime} minutes for list of {frequencies.__len__()} frequencies.")
    print(f"*")
    while True:
        for freq in frequencies:
            run_rtl_433(freq, interval)


if __name__ == '__main__':
    main()
