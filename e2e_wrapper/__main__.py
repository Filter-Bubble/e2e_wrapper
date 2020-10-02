import logging
import argparse
import sys
import io

from . import parse, __version__

# try:
#     # python3: sys.stdin.buffer contains the 'bytes'
#     input_file = sys.stdin.buffer
# except AttributeError:
#     # python2: sys.stdin contains bytes (aka 'str)
#     input_file = sys.stdin

parser = argparse.ArgumentParser(description='Coreference resolution using e2e')
parser.add_argument("--verbose", "-v", help="Verbose output", action="store_true")
parser.add_argument('-V', '--version', action='version', version="{} ({})".format(__name__, __version__))
parser.add_argument('--model_name', '-m', type=str, default='best')
parser.add_argument('cfg_file', type=str)
parser.add_argument('input_file', nargs='?', type=argparse.FileType('rb'), default=sys.stdin.buffer)


args = parser.parse_args()

logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO,
                    format='[%(asctime)s %(name)-12s %(levelname)-5s] %(message)s')

# Mute output
stdout = io.StringIO()
sys.stdout = stdout
in_obj = parse(args.input_file, args.cfg_file, args.model_name)
sys.stdout = sys.__stdout__
logging.info(stdout.getvalue())
in_obj.dump()
