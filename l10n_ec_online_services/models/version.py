import platform

from odoo import api, fields, models


class Version(models.Model):
    _name = "one.version"
    _description = "Get Version"

    version = fields.Char(default="Versions of Odoo Platform")
    version_database = fields.Char(
        compute="_compute_version_database", string="Database"
    )
    version_python = fields.Char(compute="_compute_version_python", string="Python")
    version_os = fields.Char(compute="_compute_version_os", string="OS")
    version_odoo = fields.Char(compute="_compute_version_odoo", string="Odoo")

    @api.depends("version")
    def _compute_version_python(self):
        for record in self:
            record.version_python = platform.python_version()

    @api.depends("version")
    def _compute_version_database(self):
        sql_query = """
            SELECT version() as database_version
        """
        self.env.cr.execute(sql_query)
        result = self.env.cr.fetchall()
        database_version = result[0][0]
        for record in self:
            record.version_database = database_version

    @api.depends("version")
    def _compute_version_os(self):
        for record in self:
            record.version_os = f"{platform.system()}  {platform.release()}"

    @api.depends("version")
    def _compute_version_odoo(self):
        result = self.env["ir.module.module"].search_read(
            [("name", "=", "base")], ["latest_version"]
        )
        version = result[0]["latest_version"]
        for record in self:
            record.version_odoo = version
