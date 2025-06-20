from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    reidi_api_url = fields.Char(
        string="API URL",
    )
    reidi_bearer_token = fields.Char(
        string="Bearer Token",
    )
