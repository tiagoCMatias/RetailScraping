import argparse
from pprint import pprint
from modules import (weblinks, pagereader)
# Script VERSION
__VERSION = "1.0"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--version",
                        action="store_true",
                        help="Show current version of this amazing script.")
    args = parser.parse_args()

    if args.version:
        print("Amazing Script Version: " + __VERSION)
        exit()

    link = "http://www.pai.pt/q/business/advanced/where/porto/what/Floristas/?contentErrorLinkEnabled=true"
    html_content = pagereader.read_first_page(link)
    client = weblinks.get_address(soup=html_content)
    print("size",len(client))
    pprint(client)


if __name__ == '__main__':

    try:
        main()

    except KeyboardInterrupt:
        print("Interrupt received! Exiting cleanly...")
