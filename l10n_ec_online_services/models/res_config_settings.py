from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    use_reidi = fields.Boolean(
        string="Use ReIdi",
        default=False,
        config_parameter="l10n_ec_online_services.use_reidi",
        help="Enable or disable the use of ReIdi",
    )
    reidi_api_url = fields.Char(
        string="API URL",
        related="company_id.reidi_api_url",
        readonly=False,
        default="https://reidi.ec.service.resolvedor.dev",
    )
    reidi_bearer_token = fields.Char(
        string="Bearer Token",
        related="company_id.reidi_bearer_token",
        readonly=False,
        default="your_bearer_token_here",
    )
