callDBus(
    "ca.vasilevsky.AutoPaste",
    "/ca/vasilevsky/AutoPaste/EmojiWindowCloser",
    "ca.vasilevsky.AutoPaste.EmojiWindowCloser",
    "TakeCloseRequest",
    function (windowId) {
        if (!windowId) {
            return;
        }
        try {
            const window = workspace.activeWindow;
            if (window && String(window.internalId) === windowId &&
                    String(window.resourceClass) === "org.kde.plasma.emojier") {
                window.closeWindow();
            }
        } finally {
            callDBus(
                "ca.vasilevsky.AutoPaste",
                "/ca/vasilevsky/AutoPaste/EmojiWindowCloser",
                "ca.vasilevsky.AutoPaste.EmojiWindowCloser",
                "CloseScriptFinished"
            );
        }
    }
);
