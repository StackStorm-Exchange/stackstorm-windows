from pywinexe.api import cmd as run_cmd

from st2common.runners.base_action import Action

__all__ = [
    'WinExeCmdAction'
]


class WinExeCmdAction(Action):
    def run(self, host, command, password, username='Administrator'):
        """
        Run command on a remote node
        """
        out = run_cmd(
            command,
            args=[],
            user=username,
            password=password,
            host=host)
        return {'stdout': out}
