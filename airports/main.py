import argparse


parser = argparse.ArgumentParser()
parser.add_argument("--name")
args = parser.parse_args()

name_upper = args.name.upper()

print(name_upper)
