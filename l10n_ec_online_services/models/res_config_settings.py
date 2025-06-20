from odoo import fields, models, api, _


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"


    use_reidi = fields.Boolean(
        string="Use ReIdi",
        default=True,
        config_parameter="l10n_ec_online_services.use_reidi",
        help="Enable or disable the use of ReIdi",
    )
    reidi_api_url = fields.Char(
        string="API URL",
        default="https://reidi.ec.service.resolvedor.dev/entity/",
        config_parameter="l10n_ec_online_services.reidi_api_url",
    )
    reidi_bearer_token = fields.Char(
        string="Bearer Token",
        config_parameter="l10n_ec_online_services.reidi_bearer_token",
    )

    @api.model
    def get_values(self):
        res = super().get_values()
        res.update(
            {
                "reidi_api_url": self.env["ir.config_parameter"].sudo().get_param("l10n_ec_online_services.reidi_api_url"),
                "reidi_bearer_token": self.env["ir.config_parameter"].sudo().get_param("l10n_ec_online_services.reidi_bearer_token"),
            }
        )
        return res

    def set_values(self):
        super().set_values()
        self.env["ir.config_parameter"].sudo().set_param("l10n_ec_online_services.reidi_api_url", self.reidi_api_url)
        self.env["ir.config_parameter"].sudo().set_param("l10n_ec_online_services.reidi_bearer_token", self.reidi_bearer_token)