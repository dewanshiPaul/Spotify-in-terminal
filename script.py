import argparse
from main import spotify

def run(args):
	spotify()


def main():
	parser=argparse.ArgumentParser(description="Run your spotify right from terminal!!!")
	parser.add_argument("-u",help="Enter the userid of your account", type=str, required=True)
	args=parser.parse_args()
	run(args)

if __name__=="__main__":
	main()