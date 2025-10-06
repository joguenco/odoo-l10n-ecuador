{
    "name": "Ecuadorian Point of Sale",
    "summary": " Point of Sale Ecuadorian localization",
    "category": "Sales/Point of Sale",
    "author": "Odoo Community Association (OCA), " "Jorge Luis",
    "website": "https://github.com/OCA/l10n-ecuador" "https://resolvedor.dev",
    "license": "AGPL-3",
    "version": "18.0.1.0.0",
    "depends": ["point_of_sale", "l10n_ec_account_edi", "l10n_ec_online_services"],
    "data": [
        # 'security/ir.model.access.csv',
        "views/res_partner_view.xml",
    ],
    "installable": True,
    "application": True,
    "assets": {
        "point_of_sale._assets_pos": [
            "l10n_ec_pos/static/src/**/*.js",
            "l10n_ec_pos/static/src/**/*.xml",
        ],
    },
}
