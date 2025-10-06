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

    @api.onchange("use_http_printer")
    def _onchange_use_http_printer(self):
        if not self.use_http_printer:
            self.pos_http_printer_ip = False

    @api.depends("pos_other_devices", "pos_config_id")
    def _compute_pos_http_printer_ip(self):
        for res_config in self:
            res_config.pos_http_printer_ip = res_config.pos_config_id.http_printer_ip

    def action_ping_http_printer(self):
        return {
            "type": "ir.actions.client",
            "tag": "ping_printer_action",
            "context": {
                "default_name": "Ping",
            },
            "params": {
                "url": self.pos_http_printer_ip,
            },
        }
