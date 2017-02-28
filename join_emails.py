import json
import sys

if __name__ == "__main__":
    emails = []
    for filename in sys.argv[1:]:
        with open(filename) as fd:
            emails += json.load(fd)
    with open("emails.json", "w+") as fd:
        json.dump(emails, fd)
