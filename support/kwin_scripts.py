"""Load a KWin script for the duration of a with block."""

from contextlib import contextmanager
from pathlib import Path

import dbus


class KWinScripts:
    def __init__(self, bus):
        self.bus = bus
        self.scripting = dbus.Interface(
            bus.get_object("org.kde.KWin", "/Scripting"), "org.kde.kwin.Scripting")

    @contextmanager
    def running(self, filename, name, on_error):
        try:
            self.scripting.unloadScript(name)
            path = Path(__file__).resolve().with_name(filename)
            script_id = int(self.scripting.loadScript(str(path), name, signature="ss"))
            if script_id < 0:
                raise RuntimeError(f"KWin could not load {filename}")
            script = dbus.Interface(
                self.bus.get_object("org.kde.KWin", f"/Scripting/Script{script_id}"),
                "org.kde.kwin.Script")
            script.run(reply_handler=lambda: None, error_handler=on_error)
            yield
        finally:
            try:
                self.scripting.unloadScript(name)
            except dbus.DBusException:
                pass
