import argparse
from itertools import cycle


# helper functions

def number_of_bodies(value):
    value = int(value)
    if value not in [2, 3]:
        raise argparse.ArgumentTypeError("Only double (N = 2) and triple (N = 3) pendulums are supported")
    return value


def positive_int(value):
    value = float(value)
    if value <= 0:
        raise argparse.ArgumentTypeError("Must be positive")
    return value


# argparse configurations

def configure_dubl_parser(dubl_parser):
    dubl_parser.add_argument(
        '-g', dest="g", type=positive_int, nargs='+',
        default=9.8, help='gravitational constant (or list of)'
    )
    dubl_parser.add_argument(
        '-t_max', dest="t_max", type=positive_int,
        default=30, help='time to run simulation for'
    )
    # dubl_parser.add_argument(
    #     '-o', "--output-file", dest="output_file", type=str,
    #     default=None, help='output file (a GIF)'
    # )

    masses = dubl_parser.add_argument_group('masses')
    rod_lengths = dubl_parser.add_argument_group('rod lengths')
    init_pos = dubl_parser.add_argument_group('initial positions')
    init_vel = dubl_parser.add_argument_group('initial velocities')

    masses.add_argument(
        '-m1', dest="m1", type=positive_int, nargs='+',
        default=1, help='mass of first body (or list of)'
    )
    masses.add_argument(
        '-m2', dest="m2", type=positive_int, nargs='+',
        default=1, help='mass of second body (or list of)'
    )

    rod_lengths.add_argument(
        '-l1', dest="l1", type=positive_int, nargs='+',
        default=1, help='length of first rod (or list of)'
    )
    rod_lengths.add_argument(
        '-l2', dest="l2", type=positive_int, nargs='+',
        default=1, help='length of second rod (or list of)'
    )
    
    init_pos.add_argument(
        '-theta1', dest="theta1", type=float, nargs='+',
        default=1, help='angle of first rod (or list of)'
    )
    init_pos.add_argument(
        '-theta2', dest="theta2", type=float, nargs='+',
        default=1, help='angle of second rod (or list of)'
    )
    
    init_vel.add_argument(
        '-dtheta1', dest="dtheta1", type=float, nargs='+',
        default=0, help='angular velocity of first rod (or list of)'
    )
    init_vel.add_argument(
        '-dtheta2', dest="dtheta2", type=float, nargs='+',
        default=0, help='angular velocity of second rod (or list of)'
    )


def configure_trpl_parser(trpl_parser):
    trpl_parser.add_argument(
        '-g', dest="g", type=positive_int, nargs='+',
        default=9.8, help='gravitational constant (or list of)'
    )
    trpl_parser.add_argument(
        '-t_max', dest="t_max", type=positive_int,
        default=30, help='time to run simulation for'
    )
    # trpl_parser.add_argument(
    #     '-o', "--output-file", dest="output_file", type=str,
    #     default=None, help='output file (a GIF)'
    # )

    masses = trpl_parser.add_argument_group('masses')
    rod_lengths = trpl_parser.add_argument_group('rod lengths')
    init_pos = trpl_parser.add_argument_group('initial positions')
    init_vel = trpl_parser.add_argument_group('initial velocities')

    masses.add_argument(
        '-m1', dest="m1", type=positive_int, nargs='+',
        default=1, help='mass of first body (or list of)'
    )
    masses.add_argument(
        '-m2', dest="m2", type=positive_int, nargs='+',
        default=1, help='mass of second body (or list of)'
    )
    masses.add_argument(
        '-m3', dest="m3", type=positive_int, nargs='+',
        default=1, help='mass of third body (or list of)'
    )

    rod_lengths.add_argument(
        '-l1', dest="l1", type=positive_int, nargs='+',
        default=1, help='length of first rod (or list of)'
    )
    rod_lengths.add_argument(
        '-l2', dest="l2", type=positive_int, nargs='+',
        default=1, help='length of second rod (or list of)'
    )
    rod_lengths.add_argument(
        '-l3', dest="l3", type=positive_int, nargs='+',
        default=1, help='length of third rod (or list of)'
    )

    init_pos.add_argument(
        '-theta1', dest="theta1", type=float, nargs='+',
        default=1, help='angle of first rod (or list of)'
    )
    init_pos.add_argument(
        '-theta2', dest="theta2", type=float, nargs='+',
        default=1, help='angle of second rod (or list of)'
    )
    init_pos.add_argument(
        '-theta3', dest="theta3", type=float, nargs='+',
        default=1, help='angle of third rod (or list of)'
    )

    init_vel.add_argument(
        '-dtheta1', dest="dtheta1", type=float, nargs='+',
        default=0, help='angular velocity of first rod (or list of)'
    )
    init_vel.add_argument(
        '-dtheta2', dest="dtheta2", type=float, nargs='+',
        default=0, help='angular velocity of second rod (or list of)'
    )
    init_vel.add_argument(
        '-dtheta3', dest="dtheta3", type=float, nargs='+',
        default=0, help='angular velocity of third rod (or list of)'
    )


def get_parser():
    parser = argparse.ArgumentParser(
        "n-pendulum",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    subparsers = parser.add_subparsers(
        help='Number of bodies', dest="n",
    )
    dubl_parser = subparsers.add_parser(
        "2", help='double pendulum',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    trpl_parser = subparsers.add_parser(
        "3", help='triple pendulum',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    configure_dubl_parser(dubl_parser)
    configure_trpl_parser(trpl_parser)
    
    return parser


# driver functions

def dol_to_lod(dol):
    lod = [dict(zip(dol, t)) for t in zip(*dol.values())]
    return lod


def parse_args():
    parser = get_parser()
    args = vars(parser.parse_args())

    dol = {k: v if isinstance(v, list) else cycle([v]) for (k, v) in args.items()}
    return dol_to_lod(dol)




