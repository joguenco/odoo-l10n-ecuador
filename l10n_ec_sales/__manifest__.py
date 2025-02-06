# coding: utf-8
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Report - Sale order ticket',
    'version': '1.0',
    'description': 'Sale modifications for ticket order',
    'category': 'Localization',
    'depends': [
        'sale',
    ],
    'data': [
        'report/sale_order_templates.xml',
    ],
    'installable': True,
    'auto_install': True,
    'license': 'LGPL-3',
}
