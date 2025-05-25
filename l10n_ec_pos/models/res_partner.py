from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'


    @api.model
    def _get_default_country(self):

        country = self.env['res.country'].search([('code', '=', 'EC')], limit=1)

        return country
    
    country_id = fields.Many2one('res.country', string='Country', default=_get_default_country)