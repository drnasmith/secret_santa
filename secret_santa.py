"""
Program to determine secret santa for a given list of names
Assumes that the list contains unique names
"""
import random

# Hard code the list for now - could read from a file in future?
names = [
    "Boaty McBoatface",
    "Jingly McSparkles",
    "Fizzy Prosecco Sipper",
    "Punky Toe Bells",
    "Dr Scrooge",
    "Huski Dude",
    "Slytherin Girl",
    "Wreck-it Ralph",
    "Gin-meister",
    "Photo Boy",
    "Short shorts",
]


def secret_santa_shuffle(names):
    """
    Version using the shuffle method.
    Each name in the list buys the next one.
    Last in the shuffled list buys the first name

    Return a dictionary with the gift giver as key, recipient as value
    e.g. {'Alice': 'Bob', ...}
    """
    results = {}

    # In place shuffle of the list
    random.shuffle(names)

    # Iterate through the list
    # Each person buys for the next in list
    # Remember list access starts at 0 for first entry
    for index, name in enumerate(names):
        # If we get to the last name in the list,
        # names[index+1] will fail with an index error
        # Catch this and set the last receiver to the first name in the list
        try:
            recipient = names[index + 1]
        except IndexError:
            # print("Reached end of list, buy for first name in list")
            recipient = names[0]

        results[name] = recipient

    return results


def secret_santa_zip(names):
    """
    Version using the zip method.
    Create a recipient list by moving the last name to the first
    of the shuffled list of names
    Zip the two lists together and convert to a dictionary on return.

    Return a dictionary with the gift giver as key, recipient as value
    e.g. {'Alice': 'Bob', ...}
    """
    results = {}

    # In place shuffle of the list
    random.shuffle(names)
    recipients = [names[-1]] + names[:-1]

    results = dict(zip(names, recipients))

    return results


def secret_santa_list(names):
    """
    The method to determine who is buying for who...
    Iterate through the list of names and work out who
    this person can buy for (not including self)

    Remove each recipient who has been bought a present to
    avoid them getting picked twice!

    Return a dictionary with the gift giver as key, recipient as value
    e.g. {'Alice': 'Bob', ...}
    """
    results = {}
    recipients = list(names)

    for name in names:
        # print("Determing present options for {}".format(name))

        # Can't buy for yourself...
        options = [x for x in recipients if x != name]

        # print("{} can buy for {}".format(name, ','.join(options)))

        recipient = random.choice(options)

        results[name] = recipient

        # Now remove this recipient from the list of available options
        recipients.remove(recipient)

    return results


if __name__ == "__main__":
    """
    Running this as an application so we can choose which method
    """
    import sys
    import argparse

    parser = argparse.ArgumentParser(description="Secret Santa Application")
    parser.add_argument(
        "-m",
        "--method",
        choices=["list", "shuffle", "zip"],
        default="list",
        dest="method",
        help="Choose which method to use (lower case)",
    )

    args = parser.parse_args()

    # Define results object we will use
    results = {}

    if args.method.lower() == "list":
        results = secret_santa_list(names)
    elif args.method.lower() == "shuffle":
        results = secret_santa_shuffle(names)
    elif args.method.lower() == "zip":
        results = secret_santa_zip(names)
    else:
        # Should not be able to get here with argparse choices...
        print("Error unsupported method for secret santa")
        parser.print_help()
        sys.exit(1)

    print("Secret Santa using '{}' method:".format(args.method))

    for key in results.keys():
        print("{} is buying for {}".format(key, results[key]))
