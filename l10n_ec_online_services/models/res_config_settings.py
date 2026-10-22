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
        readonly=False,
        config_parameter="l10n_ec_online_services.reidi_api_url",
    )
    reidi_bearer_token = fields.Char(
        string="Bearer Token",
        readonly=False,
        config_parameter="l10n_ec_online_services.reidi_bearer_token",
    )
