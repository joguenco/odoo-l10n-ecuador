# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    use_http_printer = fields.Boolean(
        string="Use HTTP Printer",
        default=False,
        config_parameter="use_http_printer",
        help="Enable or disable the use of HTTP Printer",
    )

    pos_http_printer_ip = fields.Char(
        compute="_compute_pos_http_printer_ip",
        string="HTTP URL",
        store=True,
        readonly=False,
    )

    @api.depends("pos_other_devices", "pos_config_id")
    def _compute_pos_http_printer_ip(self):
        for res_config in self:
            res_config.pos_http_printer_ip = res_config.pos_config_id.http_printer_ip
