{
    "name": "POS HTTP Printer",
    "summary": "Print receipts from Odoo POS using HTTP protocol "
    "to communicate with the printer.",
    "author": "Odoo Community Association (OCA), " "Jorge Luis",
    "website": "https://github.com/OCA/l10n-ecuador" "https://resolvedor.dev",
    "category": "Sales/Point of Sale",
    "license": "AGPL-3",
    "version": "18.0.1.0.0",
    "depends": ["point_of_sale"],
    "data": [
        "views/res_config_settings_views.xml",
    ],
    "installable": True,
    "application": True,
    "assets": {
        "point_of_sale._assets_pos": [
            "pos_http_printer/static/src/overrides/**/*.js",
        ],
        "web.assets_backend": [
            "pos_http_printer/static/src/backend/actions/**/*.js",
        ],
    },
}
