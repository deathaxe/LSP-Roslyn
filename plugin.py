from __future__ import annotations

import sublime
import subprocess
from os.path import dirname
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

        # check language server availability and install/upgrade on demand
        subprocess.check_output(
            args=[
                cast(str, sublime.expand_variables(p, context.variables))
                for p in context.configuration.install_command
            ],
            cwd=server_path,
            shell=True,
        )


def plugin_loaded() -> None:
    RoslynPlugin.register()


def plugin_unloaded() -> None:
    RoslynPlugin.unregister()
