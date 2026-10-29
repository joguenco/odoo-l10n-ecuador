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
# Modificado: pruebas de la lógica invertida («Diarios permitidos»).
from odoo.exceptions import ValidationError
from odoo.tests import tagged
from odoo.tests.common import TransactionCase


@tagged('post_install', '-at_install')
class TestAllowedJournals(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        journal = cls.env['account.journal']
        cls.sale_main = journal.create({'name': 'Ventas prueba A', 'code': 'TVA', 'type': 'sale'})
        cls.sale_cashier = journal.create({'name': 'Ventas prueba B', 'code': 'TVB', 'type': 'sale'})
        cls.bank_a = journal.create({'name': 'Banco prueba A', 'code': 'TBA', 'type': 'bank'})
        cls.bank_b = journal.create({'name': 'Banco prueba B', 'code': 'TBB', 'type': 'bank'})
        cls.cash = journal.create({'name': 'Efectivo prueba', 'code': 'TEF', 'type': 'cash'})
        groups = [
            cls.env.ref('base.group_user').id,
            cls.env.ref('account.group_account_invoice').id,
        ]
        # Cajero: de Ventas solo «B» y de Banco solo «A»; el Efectivo queda libre
        cls.cashier = cls.env['res.users'].create({
            'name': 'Cajero prueba',
            'login': 'cajero_prueba_restrict_journal',
            'group_ids': [(6, 0, groups)],
            'allowed_journal_ids': [(6, 0, [cls.sale_cashier.id, cls.bank_a.id])],
        })
        cls.free_user = cls.env['res.users'].create({
            'name': 'Usuario libre prueba',
            'login': 'libre_prueba_restrict_journal',
            'group_ids': [(6, 0, groups)],
        })
        cls.partner = cls.env['res.partner'].create({'name': 'Cliente prueba'})
        cls.all_test_journals = (
            cls.sale_main | cls.sale_cashier | cls.bank_a | cls.bank_b | cls.cash
        )

    def test_filter_by_type(self):
        """De los tipos elegidos solo quedan los permitidos; los demás tipos, libres."""
        allowed = self.cashier._filter_allowed_journals(self.all_test_journals)
        self.assertEqual(allowed, self.sale_cashier | self.bank_a | self.cash)

    def test_user_without_allowed_journals_is_free(self):
        allowed = self.free_user._filter_allowed_journals(self.all_test_journals)
        self.assertEqual(allowed, self.all_test_journals)

    def test_invoice_journal_list_and_default(self):
        """En la factura solo sale su diario de ventas, y ya viene elegido."""
        move = self.env['account.move'].with_user(self.cashier)
        suitable = move._get_suitable_journal_ids('out_invoice')
        self.assertIn(self.sale_cashier, suitable)
        self.assertNotIn(self.sale_main, suitable)
        invoice = move.new({'move_type': 'out_invoice', 'partner_id': self.partner.id})
        self.assertEqual(invoice.journal_id, self.sale_cashier)

    def test_invoice_in_other_journal_fails(self):
        move = self.env['account.move'].with_user(self.cashier)
        with self.assertRaises(ValidationError):
            move.create({
                'move_type': 'out_invoice',
                'partner_id': self.partner.id,
                'journal_id': self.sale_main.id,
            })
        invoice = move.create({
            'move_type': 'out_invoice',
            'partner_id': self.partner.id,
            'journal_id': self.sale_cashier.id,
        })
        self.assertEqual(invoice.journal_id, self.sale_cashier)

    def test_payment_journal(self):
        """Pago en un banco no permitido: error. En el permitido o en efectivo: bien."""
        payment = self.env['account.payment'].with_user(self.cashier)
        values = {'amount': 10.0, 'payment_type': 'inbound', 'partner_type': 'customer'}
        with self.assertRaises(ValidationError):
            payment.create({**values, 'journal_id': self.bank_b.id})
        self.assertEqual(payment.create({**values, 'journal_id': self.bank_a.id}).journal_id, self.bank_a)
        self.assertEqual(payment.create({**values, 'journal_id': self.cash.id}).journal_id, self.cash)

    def test_admin_without_allowed_journals_uses_any(self):
        """El administrador (sin diarios permitidos) sigue usando todos."""
        invoice = self.env['account.move'].create({
            'move_type': 'out_invoice',
            'partner_id': self.partner.id,
            'journal_id': self.sale_main.id,
        })
        self.assertEqual(invoice.journal_id, self.sale_main)
