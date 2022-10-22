#!/usr/bin/env python3
"""Usage: async_multicommand.py [-vh] COMMAND HOSTFILE

Arguments:
  COMMANDs  List of command to run, separated by comma
  HOSTFILE file with a list of all hosts, one host per row

Options:
  -h --help
"""
from docopt import docopt
import asyncio
import asyncssh


def get_arguments():
    arguments = docopt(__doc__)
    return arguments['COMMAND'], arguments['HOSTFILE']


async def run_command(host, cmd, conn):
    """Run a command on a host and capture the exit status and output"""

    try:
        result = await conn.run(cmd)
        print(host+": "+result.stdout)
    except Exception as exc:
        print(exc)


async def run_commands(host, cmds):
    """Run a set of commands on a host"""

    try:
        conn = await asyncssh.connect(host, known_hosts=None)
    except Exception as exc:
        print(exc)
    else:
        return [run_command(host, cmd, conn) for cmd in cmds]


async def parallel_run(hosts, cmds):
    """Run a set of commands on a set of hosts in parallel"""

    results = sum([await run_commands(host, cmds) for host in hosts], [])
    await asyncio.gather(*results)


def main():
    command_input, hostfile = get_arguments()
    with open(hostfile) as f:
        hosts = f.read().split()
    commands = command_input.split(',')
    asyncio.run(parallel_run(hosts, commands))


if __name__ == '__main__':
    main()
