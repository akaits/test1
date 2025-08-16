import sys
import time
import signal


def setup():
    print("!!!Set up!!!")


def cleanup():
    print("!!!Clean up!!!")
    # Cleanup処理いろいろ
    time.sleep(10)
    print("!!!Clean up Done!!!")


def sig_handler(signum, frame) -> None:
    sys.exit(1)


def main():
    setup()
    signal.signal(signal.SIGTERM, sig_handler)
    try:
        # いろいろな処理
        print("b")
        time.sleep(60)
        print("b")
    finally:
        signal.signal(signal.SIGTERM, signal.SIG_IGN)
        signal.signal(signal.SIGINT, signal.SIG_IGN)
        cleanup()
        signal.signal(signal.SIGTERM, signal.SIG_DFL)
        signal.signal(signal.SIGINT, signal.SIG_DFL)


if __name__ == "__main__":
    sys.exit(main())

