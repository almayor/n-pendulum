import argparse


def check_n(value):
    value = int(value)
    if value not in [2, 3]:
        raise argparse.ArgumentTypeError("Only double (N = 2) and triple (N = 3) pendulums are supported")
    return value


def check_positive(value):
    value = float(value)
    if value <= 0:
        raise argparse.ArgumentTypeError("Must be positive")
    return value


def configure_dubl_parser(dubl_parser):
    dubl_parser.add_argument(
        '-g', dest="g", type=check_positive,
        default=9.8, help='gravitational constant'
    )
    dubl_parser.add_argument(
        '-t_max', dest="t_max", type=check_positive,
        default=30, help='time to run simulation for'
    )
    dubl_parser.add_argument(
        '-o', "--output-file", dest="output_file", type=str,
        default=None, help='output file (a GIF)'
    )

    masses = dubl_parser.add_argument_group('masses')
    rod_lengths = dubl_parser.add_argument_group('rod lengths')
    init_pos = dubl_parser.add_argument_group('initial positions')
    init_vel = dubl_parser.add_argument_group('initial velocities')

    masses.add_argument(
        '-m1', dest="m1", type=check_positive,
        default=1, help='mass of first body'
    )
    masses.add_argument(
        '-m2', dest="m2", type=check_positive,
        default=1, help='mass of second body'
    )

    rod_lengths.add_argument(
        '-l1', dest="l1", type=check_positive,
        default=1, help='length of first rod'
    )
    rod_lengths.add_argument(
        '-l2', dest="l2", type=check_positive,
        default=1, help='length of second rod'
    )
    
    init_pos.add_argument(
        '-theta1', dest="theta1", type=float,
        default=1, help='angle of first rod'
    )
    init_pos.add_argument(
        '-theta2', dest="theta2", type=float,
        default=1, help='angle of second rod'
    )
    
    init_vel.add_argument(
        '-dtheta1', dest="dtheta1", type=float,
        default=0, help='angular velocity of first rod'
    )
    init_vel.add_argument(
        '-dtheta2', dest="dtheta2", type=float,
        default=0, help='angular velocity of second rod'
    )


def configure_trpl_parser(trpl_parser):
    trpl_parser.add_argument(
        '-g', dest="g", type=check_positive,
        default=9.8, help='gravitational constant'
    )
    trpl_parser.add_argument(
        '-t_max', dest="t_max", type=check_positive,
        default=30, help='time to run simulation for'
    )
    trpl_parser.add_argument(
        '-o', "--output-file", dest="output_file", type=str,
        default=None, help='output file (a GIF)'
    )

    masses = trpl_parser.add_argument_group('masses')
    rod_lengths = trpl_parser.add_argument_group('rod lengths')
    init_pos = trpl_parser.add_argument_group('initial positions')
    init_vel = trpl_parser.add_argument_group('initial velocities')

    masses.add_argument(
        '-m1', dest="m1", type=check_positive,
        default=1, help='mass of first body'
    )
    masses.add_argument(
        '-m2', dest="m2", type=check_positive,
        default=1, help='mass of second body'
    )
    masses.add_argument(
        '-m3', dest="m3", type=check_positive,
        default=1, help='mass of third body'
    )

    rod_lengths.add_argument(
        '-l1', dest="l1", type=check_positive,
        default=1, help='length of first rod'
    )
    rod_lengths.add_argument(
        '-l2', dest="l2", type=check_positive,
        default=1, help='length of second rod'
    )
    rod_lengths.add_argument(
        '-l3', dest="l3", type=check_positive,
        default=1, help='length of third rod'
    )

    init_pos.add_argument(
        '-theta1', dest="theta1", type=float,
        default=1, help='angle of first rod'
    )
    init_pos.add_argument(
        '-theta2', dest="theta2", type=float,
        default=1, help='angle of second rod'
    )
    init_pos.add_argument(
        '-theta3', dest="theta3", type=float,
        default=1, help='angle of third rod'
    )

    init_vel.add_argument(
        '-dtheta1', dest="dtheta1", type=float,
        default=0, help='angular velocity of first rod'
    )
    init_vel.add_argument(
        '-dtheta2', dest="dtheta2", type=float,
        default=0, help='angular velocity of second rod'
    )
    init_vel.add_argument(
        '-dtheta3', dest="dtheta3", type=float,
        default=0, help='angular velocity of third rod'
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
