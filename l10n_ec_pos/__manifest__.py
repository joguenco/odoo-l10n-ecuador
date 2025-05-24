# -*- coding: utf-8 -*-
{
    "name": "Ecuadorian Point of Sale",
    "summary": " Point of Sale Ecuadorian localization",
    "category": "Sales/Point of Sale",
    "author": "Odoo Community Association (OCA), "
    "Jorge Quiguango",
    "website": "https://github.com/OCA/l10n-ecuador",
    "license": "AGPL-3",
    "version": "18.0.1.0.0",
    "depends": ["point_of_sale", "l10n_ec_account_edi"],
    'data': [
        # 'security/ir.model.access.csv',
    ],
    'installable': True,
    'application': True,
    'assets': {
        'point_of_sale._assets_pos': [
            'l10n_ec_pos/static/src/**/*.js',
            'l10n_ec_pos/static/src/**/*.xml',
        ],
    },
}

