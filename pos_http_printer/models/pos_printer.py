from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class PosPrinter(models.Model):
    _inherit = "pos.printer"

    printer_type = fields.Selection(
        selection_add=[("http_epos", "Use an HTTP printer")]
    )
    http_printer_ip = fields.Char(
        string="HTTP Printer IP Address",
        help=("Local IP address of an HTTP Server Printer"),
        default="0.0.0.0",
    )

    @api.constrains("epson_printer_ip")
    def _constrains_epson_printer_ip(self):
        for record in self:
            if not record.http_printer_ip:
                raise ValidationError(_("Epson Printer IP Address cannot be empty."))

    @api.model
    def _load_pos_data_fields(self, config_id):
        params = super()._load_pos_data_fields(config_id)
        params += ["http_printer_ip"]
        return params
