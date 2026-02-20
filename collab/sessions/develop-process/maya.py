import argparse
import sys

def main():
    parser = argparse.ArgumentParser(description="MayaLucIA: An Intelligence Amplifier")
    parser.add_argument("--version", action="version", version="MayaLucIA v0.1.0")
    parser.add_argument("--greet", type=str, help="Greet a user by name")
    
    args = parser.parse_args()
    
    if args.greet:
        print(f"Namaste, {args.greet}! Welcome to MayaLucIA.")
    else:
        print("MayaLucIA: Intelligence Amplifier for Scientific Inquiry")
        print("Use --greet <name> to be welcomed personally.")

if __name__ == "__main__":
    main()
