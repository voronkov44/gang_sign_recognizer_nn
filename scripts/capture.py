import argparse
from data.capture import DataCapture


def main():
    parser = argparse.ArgumentParser(description="Capture gang sign training data")
    parser.add_argument("--camera", type=int, default=0, help="Camera index (0-iPhone, 1-Mac)")
    parser.add_argument("--output", type=str, default="training_data", help="Output directory")
    parser.add_argument("--samples", type=int, default=1000, help="Samples per class")

    args = parser.parse_args()

    capture = DataCapture(args.output)
    capture.capture(camera_index=args.camera, samples_per_class=args.samples)


if __name__ == "__main__":
    main()