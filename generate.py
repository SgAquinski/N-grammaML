from train import t as _t
import argparse
import pickle

if __name__ == '__main__':
    parser1 = argparse.ArgumentParser()
    parser1.add_argument("--model", type=str, required=True)
    parser1.add_argument("--prefix", type=str, help="use underscore between words instead of space.")
    parser1.add_argument("--lenght", type=int, required=True)
    arg = parser1.parse_args()

    _t.generate(arg.model, arg.prefix, arg.lenght)


