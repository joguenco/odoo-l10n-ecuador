# -*- coding: utf-8 -*-
#############################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2026-TODAY Cybrosys Technologies(<https://www.cybrosys.com>)
#    Author: Cybrosys Techno Solutions(<https://www.cybrosys.com>)
#
#    You can modify it under the terms of the GNU LESSER
#    GENERAL PUBLIC LICENSE (LGPL v3), Version 3.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU LESSER GENERAL PUBLIC LICENSE (LGPL v3) for more details.
#
#    You should have received a copy of the GNU LESSER GENERAL PUBLIC LICENSE
#    (LGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
#############################################################################
# Modificado: lógica invertida. En vez de los diarios prohibidos se eligen los
# diarios permitidos del usuario («Diarios permitidos»).
from odoo import _, fields, models
from odoo.exceptions import ValidationError


class ResUsers(models.Model):
    """Diarios permitidos: con qué diarios puede facturar y cobrar el usuario.

    Va por tipo de diario: si el usuario tiene diarios permitidos de un tipo (por
    ejemplo de Ventas), de ese tipo solo puede usar los elegidos. Los tipos sin
    ninguno elegido quedan libres. Sin diarios permitidos no hay restricción.
    """

    _inherit = 'res.users'

    allowed_journal_ids = fields.Many2many(
        'account.journal',
        'res_users_allowed_journal_rel',
        'user_id',
        'journal_id',
        string='Diarios permitidos',
        help='Los diarios que este usuario puede usar. De cada tipo de diario '
        '(Ventas, Efectivo, Banco...) que elijas aquí, solo podrá usar los '
        'elegidos; los tipos sin ninguno elegido quedan libres.',
    )

    def _filter_allowed_journals(self, journals):
        """De esos diarios, deja solo los que el usuario puede usar."""
        self.ensure_one()
        allowed = self.sudo().allowed_journal_ids
        restricted_types = set(allowed.mapped('type'))
        return journals.filtered(
            lambda journal: journal.type not in restricted_types or journal in allowed
        )

    def _check_allowed_journal(self, journal):
        """Error si el usuario no puede usar ese diario."""
        self.ensure_one()
        if journal and not self._filter_allowed_journals(journal):
            allowed = self.sudo().allowed_journal_ids.filtered(
                lambda j: j.type == journal.type
            )
            raise ValidationError(
                _(
                    'El usuario «%(user)s» no puede usar el diario «%(journal)s».\n'
                    'Sus diarios permitidos de este tipo son: %(allowed)s.\n\n'
                    'Se cambian en Ajustes → Usuarios → %(user)s → Diarios '
                    'permitidos.',
                    user=self.name,
                    journal=journal.display_name,
                    allowed=', '.join(allowed.mapped('display_name')),
                )
            )
