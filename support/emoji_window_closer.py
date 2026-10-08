"""Close an emoji picker through KWin and await the script's completion."""

import asyncio

import dbus.service


CLOSE_SCRIPT_NAME = "auto-paste-close-emojier"


class EmojiWindowCloser(dbus.service.Object):
    """Own the D-Bus handshake used by close_emojier.js."""

    def __init__(self, bus_name, kwin_scripts):
        super().__init__(bus_name, "/ca/vasilevsky/AutoPaste/EmojiWindowCloser")
        # Loads the temporary script and unloads it when the request finishes.
        self.kwin_scripts = kwin_scripts
        # (window ID, completion future), or None when no close is in progress.
        self.pending_close = None

    async def close(self, window_id):
        """Ask KWin to close this picker; the caller waits for focus separately."""
        finished = asyncio.get_running_loop().create_future()
        self.pending_close = (window_id, finished)

        def failed(error):
            if not finished.done():
                finished.set_exception(error)

        try:
            with self.kwin_scripts.running("close_emojier.js", CLOSE_SCRIPT_NAME, failed):
                await finished
        finally:
            self.pending_close = None

    @dbus.service.method("ca.vasilevsky.AutoPaste.EmojiWindowCloser", in_signature="", out_signature="s")
    def TakeCloseRequest(self):
        """Give the KWin script the ID of the picker we want closed."""
        return self.pending_close[0] if self.pending_close else ""

    @dbus.service.method("ca.vasilevsky.AutoPaste.EmojiWindowCloser", in_signature="", out_signature="")
    def CloseScriptFinished(self):
        """Unblock close() after the script has attempted to close the picker."""
        if self.pending_close:
            finished = self.pending_close[1]
            if not finished.done():
                finished.set_result(None)
