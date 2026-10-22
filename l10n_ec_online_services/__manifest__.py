{
    "name": "Online Services for Ecuador",
    "summary": "Online services for Ecuadorian localization",
    "author": "Odoo Community Association (OCA), " "Jorge Luis",
    "website": "https://github.com/OCA/l10n-ecuador" "https://resolvedor.dev",
    "category": "Services/Online Services",
    "license": "AGPL-3",
    "version": "18.0.1.0.0",
    "depends": ["base", "l10n_ec_account_edi"],
    "data": [
        "security/ir.model.access.csv",
        "data/version.xml",
        "wizard/one_reidi.xml",
        "views/one_dashboard.xml",
        "views/one_version.xml",
        "views/res_config_settings.xml",
        "views/one_menu.xml",
    ],
    "installable": True,
    "application": True,
    "assets": {
        "web.assets_backend": [
            "l10n_ec_online_services/static/src/**/*.js",
            "l10n_ec_online_services/static/src/**/*.xml",
        ],
    },
}
