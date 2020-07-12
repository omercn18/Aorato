import argparse

from manager import Manager


def main(server_port, num_of_clients):
    manager = Manager(num_of_clients, server_port)
    manager.start()
    input("Press ENTER to exit\n")
    # If achieved here user wants to exit
    print("Stopping gracefully..")
    manager.stop()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='HTTP dos protection system')
    parser.add_argument('--server_port',
                        help='A single port that server should listen to and client should interact with',
                        type=int,
                        required=True)
    parser.add_argument('--num_of_clients',
                        help='A number of clients to simulate',
                        type=int,
                        required=True)
    args = parser.parse_args()
    main(args.server_port, args.num_of_clients)
