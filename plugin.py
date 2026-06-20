from __future__ import annotations

import sublime
import subprocess
import time
from os.path import dirname
from shutil import which
from typing import cast, override

from LSP.plugin import LspPlugin, OnPreStartContext

__all__ = ["RoslynPlugin", "plugin_loaded", "plugin_unloaded"]


class RoslynPlugin(LspPlugin):

    @classmethod
    @override
    def on_pre_start_async(cls, context: OnPreStartContext) -> None:
        cls.plugin_storage_path.mkdir(parents=True, exist_ok=True)

        server_path = str(cls.plugin_storage_path)
        context.variables["package_path"] = dirname(__spec__.origin)
        context.variables["server_path"] = server_path

        # check language server existence and determine last update check timestamp
        update_timestamp = 0.0
        update_timestamp_file = cls.plugin_storage_path / "last_update_check"
        server_binary = which(cast(str, sublime.expand_variables(context.configuration.command[0], context.variables)))
        if server_binary:
            try:
                update_timestamp = float(update_timestamp_file.read_text())
            except Exception:
                pass

        # check language server availability and install/upgrade on demand
        if (now := time.time()) > update_timestamp + 24 * 60:
            try:
                _ = subprocess.check_output(
                    args=[
                        cast(str, sublime.expand_variables(p, context.variables))
                        for p in context.configuration.install_command
                    ],
                    cwd=server_path,
                    shell=True,
                )
            except subprocess.CalledProcessError:
                if server_binary is None:
                    raise

            update_timestamp_file.write_text(str(now))


def plugin_loaded() -> None:
    RoslynPlugin.register()


def plugin_unloaded() -> None:
    RoslynPlugin.unregister()
