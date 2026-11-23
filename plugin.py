from __future__ import annotations

import asyncio
import sublime
import time
from os.path import dirname
from shutil import which
from subprocess import CalledProcessError
from typing import cast, override

from LSP.plugin import LspPlugin, OnPreStartContext

IS_WIN = sublime.platform() == "windows"
if IS_WIN:
    import re
    from subprocess import list2cmdline as shell_join

    def shell_quote(s: str) -> str:
        s = re.sub(r"([&|<>?*])", R"^\1", s)
        return '"' + s.replace('"', '""') + '"' if " " in s else s

else:
    from shlex import join as shell_join, quote as shell_quote

__all__ = ["RoslynPlugin", "plugin_loaded", "plugin_unloaded"]


class RoslynPlugin(LspPlugin):
    @classmethod
    @override
    async def on_pre_start(cls, context: OnPreStartContext) -> None:
        cls.plugin_storage_path.mkdir(parents=True, exist_ok=True)

        server_path = str(cls.plugin_storage_path)
        context.variables["package_path"] = dirname(__spec__.origin)
        context.variables["server_path"] = server_path

        # check language server existence and determine last update check timestamp
        update_timestamp = 0.0
        update_timestamp_file = cls.plugin_storage_path / "last_update_check"
        server_binary = which(
            cast(str, sublime.expand_variables(shell_quote(context.configuration.command[0]), context.variables))
        )
        if server_binary:
            try:
                update_timestamp = float(update_timestamp_file.read_text())
            except Exception:
                pass

        # check language server availability and install/upgrade on demand
        if (now := time.time()) > update_timestamp + 24 * 60:
            try:
                args = [server_binary, *map(shell_quote, context.configuration.root_settings["install_command"][1:])]
                await asyncio.create_subprocess_shell(cmd=shell_join(args), cwd=server_path)
            except CalledProcessError:
                if server_binary is None:
                    raise

            update_timestamp_file.write_text(str(now))


def plugin_loaded() -> None:
    RoslynPlugin.register()


def plugin_unloaded() -> None:
    RoslynPlugin.unregister()
