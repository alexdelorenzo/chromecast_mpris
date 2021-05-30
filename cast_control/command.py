from typing import Optional, List
import collections
import logging
import sys

import click

from .base import RC_NO_CHROMECAST, LOG_LEVEL, \
  DEFAULT_RETRY_WAIT, RC_NOT_RUNNING, LOG
from .run import MprisDaemon, DaemonArgs, get_daemon, \
  run_safe, get_daemon_from_args


LOG_MODE: str = 'r'
LOG_END: str = ''

HELP: str = """
Control casting devices via Linux media controls and desktops.

This daemon connects your casting device directly to the D-Bus media player interface.
"""


class OrderCommands(click.Group):
  """List `click` commands in the order they're declared."""

  def list_commands(self, ctx: click.Command) -> List[str]:
    return list(self.commands)


@click.group(help=HELP)
def cmd():
  pass


@cmd.command(
  help='Connect to the device and run the service in the foreground.',
)
@click.option('--name', '-n',
  default=None, show_default=True, type=click.STRING,
  help="Connect to a device via its name, otherwise control the first device found.")
@click.option('--host', '-h',
  default=None, show_default=True, type=click.STRING,
  help="Connect to a device via its hostname or IP address, otherwise control the first device found.")
@click.option('--uuid', '-u',
  default=None, show_default=True, type=click.STRING,
  help="Connect to a device via its UUID, otherwise control the first device found.")
@click.option('--wait', '-w',
  default=None, show_default=True, type=click.FLOAT,
  help="Seconds to wait between trying to make initial successful connections to a device.")
@click.option('--retry-wait', '-r',
  default=DEFAULT_RETRY_WAIT, show_default=True, type=click.FLOAT,
  help="Seconds to wait between reconnection attempts if a successful connection is interrupted.")
@click.option('--icon', '-i',
  is_flag=True, default=False, show_default=True, type=click.BOOL,
  help="Use a lighter icon instead of the dark icon. The lighter icon goes well with dark themes.")
@click.option('--log-level', '-l',
  default=LOG_LEVEL, show_default=True, type=click.STRING,
  help='Set the debugging log level.')
def connect(
  name: Optional[str],
  host: Optional[str],
  uuid: Optional[str],
  wait: Optional[float],
  retry_wait: Optional[float],
  icon: bool,
  log_level: str
):
  args = DaemonArgs(
    name,
    host,
    uuid,
    wait,
    retry_wait,
    icon,
    log_level
  )

  run_safe(*args, set_logging=True)


@cmd.group(
  cls=OrderCommands,
  help='Connect, disconnect or reconnect the background service to or from your device.',
)
def service():
  pass


@service.command(
  help='Connect the background service to the device.'
)
@click.option('--name', '-n',
  default=None, show_default=True, type=click.STRING,
  help="Connect to a device via its name, otherwise control the first device found.")
@click.option('--host', '-h',
  default=None, show_default=True, type=click.STRING,
  help="Connect to a device via its hostname or IP address, otherwise control the first device found.")
@click.option('--uuid', '-u',
  default=None, show_default=True, type=click.STRING,
  help="Connect to a device via its UUID, otherwise control the first device found.")
@click.option('--wait', '-w',
  default=None, show_default=True, type=click.FLOAT,
  help="Seconds to wait between trying to make initial successful connections to a device.")
@click.option('--retry-wait', '-r',
  default=DEFAULT_RETRY_WAIT, show_default=True, type=click.FLOAT,
  help="Seconds to wait between reconnection attempts if a successful connection is interrupted.")
@click.option('--icon', '-i',
  is_flag=True, default=False, show_default=True, type=click.BOOL,
  help="Use a lighter icon instead of the dark icon. The lighter icon goes well with dark themes.")
@click.option('--log-level', '-l',
  default=LOG_LEVEL, show_default=True, type=click.STRING,
  help='Set the debugging log level.')
def connect(
  name: Optional[str],
  host: Optional[str],
  uuid: Optional[str],
  wait: Optional[float],
  retry_wait: Optional[float],
  icon: bool,
  log_level: str
):
  args = DaemonArgs(
    name,
    host,
    uuid,
    wait,
    retry_wait,
    icon,
    log_level
  )
  args.save()

  try:
    daemon = get_daemon_from_args(run_safe, args)
    daemon.start()

  except Exception as e:
    logging.exception(e)
    logging.warning("Error launching daemon.")

    args.delete()


@service.command(
  help='Disconnect the background service from the device.'
)
def disconnect():
  daemon = get_daemon()

  if not daemon.pid:
    logging.warning("Daemon isn't running.")
    sys.exit(RC_NOT_RUNNING)

  daemon.stop()
  DaemonArgs.delete()


@service.command(
  help='Reconnect the background service to the device.'
)
def reconnect():
  daemon: Optional[MprisDaemon] = None
  args = DaemonArgs.load()

  if args:
    daemon = get_daemon_from_args(run_safe, args)

  if not args or not daemon.pid:
    logging.warning("Daemon isn't running.")
    sys.exit(RC_NOT_RUNNING)

  daemon.restart()


@service.command(
  help='Show the service log.'
)
def show():
  print(f"<Log file: {LOG}>")

  # a large log could crash Python or the system
  # iterate over the file instead of using Path.read_text()
  with LOG.open(LOG_MODE) as log:
    for line in log:
      print(line, end=LOG_END)


if __name__ == "__main__":
  cmd()