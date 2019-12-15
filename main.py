from src.match import TwoThreeMatching
import argparse
import sys

def main():
    filename = sys.argv[1]
    m = TwoThreeMatching(filename).match()

    for i, g in enumerate(m):
        print("팀 #{} : {}".format(i, g))
    #parser = argparse.ArgumentParser()
    #parser.add_argument('--filename', help="input filename")

if __name__ == "__main__":
    main()
