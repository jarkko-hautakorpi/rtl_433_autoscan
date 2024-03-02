import subprocess
import time
import itertools
import signal
import sys

# Frequencies (in Hz) to scan: 433.92 MHz, 868 MHz, 915 MHz
frequencies = [433920000, 868000000, 915000000]

# Demodulator protocols to cycle through (example: enabling Acurite and enabling Oregon Scientific)
protocols = ['-R 40', '-R 41']


# Handle Ctrl-C gracefully
def signal_handler(signal, frame):
    print('Exiting...')
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)


def run_rtl_433(freq, protocol):
    # Construct the rtl_433 command
    cmd = ['rtl_433', '-f', str(freq), protocol, '-T', '300']
    print(f"Running {' '.join(cmd)}")
    try:
        # Run the command and wait for it to complete
        subprocess.run(cmd)
    except subprocess.CalledProcessError as e:
        print(f"rtl_433 exited with error: {e}")


def main():
    for freq, protocol in itertools.product(frequencies, protocols):
        run_rtl_433(freq, protocol)


if __name__ == '__main__':
    while True:
        main()
