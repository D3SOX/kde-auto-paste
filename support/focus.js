function reportFocus(window) {
    callDBus(
        "ca.vasilevsky.AutoPaste",
        "/ca/vasilevsky/AutoPaste",
        "ca.vasilevsky.AutoPaste",
        "FocusChanged",
        JSON.stringify(window ? {
            resourceClass: String(window.resourceClass),
            caption: String(window.caption),
            resourceName: String(window.resourceName),
            windowRole: String(window.windowRole),
            internalId: String(window.internalId),
            popupWindow: window.popupWindow,
            dialog: window.dialog,
            normalWindow: window.normalWindow
        } : null)
    );
}

workspace.windowActivated.connect(reportFocus);
reportFocus(workspace.activeWindow);
