import atexit
import os
import subprocess
import time


def get_my_address():
    import socket
    return socket.gethostbyname(socket.gethostname())


def add_arguments(parser):
    parser.add_argument('--redis-address', type=str, default=get_my_address(),
                        help='The IP address of the redis server')
    parser.add_argument('--redis-port', type=int, default=6380,
                        help='The port of the redis server')
    parser.add_argument('--notification-port', type=int, default=7777,
                        help='The port of the notification server')
    parser.add_argument('--notification-listening-port', type=int, default=8888,
                        help='The listening port of the notification client')
    parser.add_argument('--plasma-socket', type=str, default="/tmp/multicast_plasma",
                        help='The path of the unix domain socket')
    parser.add_argument('--object_writer_port', type=int, default=6666,
                        help='The path of the unix domain socket')
    parser.add_argument('--grpc-port', type=int, default=50055,
                        help='The path of the unix domain socket')


def extract_dict_from_args(args):
    return {
        'redis_address': args.redis_address.encode(),
        'redis_port': args.redis_port,
        'notification_port': args.notification_port,
        'notification_listening_port': args.notification_listening_port,
        'plasma_socket': args.plasma_socket.encode(),
        'object_writer_port': args.object_writer_port,
        'grpc_port': args.grpc_port,
    }


# def create_store_using_dict(args_dict):
#     import py_distributed_object_store as store_lib
#     store = store_lib.DistributedObjectStore(
#         args_dict['redis_address'],
#         args_dict['redis_port'],
#         args_dict['notification_port'],
#         args_dict['notification_listening_port'],
#         args_dict['plasma_socket'],
#         args_dict['object_writer_port'],
#         args_dict['grpc_port'])
#     return store


# def object_id_from_int(n):
#     import py_distributed_object_store as store_lib
#     return store_lib.ObjectID(str(n).encode().rjust(20, b'\0'))


# def random_object_id():
#     import random
#     return object_id_from_int(random.randint(0, 1e20-1))


def register_cleanup(processes):
    def _cleanup_processes():
        for p in processes:
            p.terminate()
    atexit.register(_cleanup_processes)


def start_location_server():
    notification_path = os.path.join(os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))), 'notification')
    notification_p = subprocess.Popen([notification_path, get_my_address()])
    register_cleanup([notification_p])
    time.sleep(2)