from tutor import hooks

hooks.Filters.ENV_PATCHES.add_items([
    (
        "openedx-lms-common-settings",
        """INSTALLED_APPS.append("coupledinput")
"""
    ),
])
