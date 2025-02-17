"""Argparser module for hub push"""
from ..helper import add_arg_group


def mixin_hub_pull_parser(parser):
    """Add the arguments for hub pull to the parser
    :param parser: the parser configure
    """
    gp = add_arg_group(parser, title='Pull')
    gp.add_argument(
        'uri',
        type=str,
        help='The URI of the executor to download (e.g., jinahub[+docker]://UUID8)',
    )
    gp.add_argument(
        '--install-requirements',
        action='store_true',
        default=False,
        help='If set, install `requirements.txt` in the Hub Executor bundle to the local system',
    )
