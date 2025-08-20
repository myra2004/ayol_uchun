JAZZMIN_SETTINGS = {
    "site_title": "Ayol Uchun Admin",
    "site_header": "Open Cloud",
    "site_logo_classes": "img-circle",
    "welcome_sign": "Welcome to the Open Cloud Admin",
    "search_model": ["auth.User", "auth.Group"],
    "user_avatar": "avatar",

    "topmenu_links": [
        {"name": "Home",  "url": "admin:index", "permissions": ["auth.view_user"]},
        {"name": "Support", "url": "https://github.com/farridav/django-jazzmin/issues", "new_window": True},
        {"app": "accounts"},
    ],

    "show_sidebar": True,
    "navigation_expanded": False,
    "hide_apps": [],
    "hide_models": [],

    "custom_links": {
        "books": [{
            "name": "Make Messages",
            "url": "make_messages",
            "icon": "fas fa-comments",
            "permissions": ["books.view_book"]
        }]
    },

    "icons": {
        "auth": "fas fa-users-cog",
        "accounts.Admins": "fas fa-user",
        "auth.Group": "fas fa-users",
        "accounts.Partners": "fas fa-handshake",
    },

    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",

    "related_modal_active": False,
    "custom_css": None,
    "custom_js": None,
    "use_google_fonts_cdn": True,
    "show_ui_builder": True,

    "changeform_format": "horizontal_tabs",
    "changeform_format_overrides": {
        "auth.user": "collapsible",
        "auth.group": "vertical_tabs",
        "partners.Partners": "horizontal_tabs"
    },

    "language_chooser": True,
}
