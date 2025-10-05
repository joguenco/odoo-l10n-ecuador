from odoo import fields, models


class PosConfig(models.Model):
    _inherit = "pos.config"

    http_printer_ip = fields.Char(
        string="HTTP Printer IP", help=("Local IP address of an HTTP Server Printer")
    )
