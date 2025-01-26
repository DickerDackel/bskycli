import argparse
import sys
import time

from pathlib import Path

from bskycli.commands import post, ls, rm

def main():
    now = time.strftime('%F-%T')

    cmdline = argparse.ArgumentParser(description='Schedule a bluesky posts')

    subparsers = cmdline.add_subparsers(required=True, help='Command list')

    cmdline_help = subparsers.add_parser('help', help='Usage')
    cmdline_help.set_defaults(func=help)

    cmdline_post = subparsers.add_parser('post', help='Create a post')
    cmdline_post.add_argument('-t', '--at', type=str, default=now, help='Earliest time to post.  Format is YYYY-MM-DD-HH:MM[:SS].  Default is now.')
    cmdline_post.add_argument('textfile', type=Path, help='File containing the post text.  Use "-" for stdin.')
    cmdline_post.add_argument('images', nargs='*', type=Path, help='Optional list of up to 4 images')
    cmdline_post.set_defaults(func=post)

    cmdline_ls = subparsers.add_parser('ls', help='List queued posts')
    cmdline_ls.add_argument('-v', '--verbose', action='store_true', help='Verbose listing')
    cmdline_ls.add_argument('-s', '--spool', choices=['all', 'i', 'inbox', 'q', 'queue', 'a', 'active', 'd', 'done'],
                            default='queue', help='List jobs in specified spool states')
    cmdline_ls.set_defaults(func=ls)

    cmdline_rm = subparsers.add_parser('rm', help='Remove posts from the queue')
    cmdline_rm.add_argument('-v', '--verbose', action='store_true', help='Verbose removal')
    cmdline_rm.add_argument('jobs', nargs='+', help='Remove listed jobs from the queue')
    cmdline_rm.add_argument('-s', '--spool', choices=['all', 'i', 'inbox', 'q', 'queue', 'a', 'active', 'd', 'done'],
                            default='queue', help='Remove jobs from specified spool states')
    cmdline_rm.set_defaults(func=rm)

    opts = cmdline.parse_args(sys.argv[1:])

    opts.func(opts)


if __name__ == "__main__":
    main()
