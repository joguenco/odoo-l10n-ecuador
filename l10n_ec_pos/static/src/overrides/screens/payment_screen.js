/**
 * Author: Jorge Luis
 * Email: jorgeluis@resolvedor.dev
 * Website: https://joguenco.dev
 */
import { patch } from '@web/core/utils/patch'
import { _t } from '@web/core/l10n/translation'
import { AlertDialog } from '@web/core/confirmation_dialog/confirmation_dialog'
import { PaymentScreen } from '@point_of_sale/app/screens/payment_screen/payment_screen'

patch(PaymentScreen.prototype, {
  /**
   * Overrides `validateOrder` method to make the customer mandatory.
   * @param {boolean} isForceValidate
   * @returns {Promise<boolean>}
   */
  async validateOrder (isForceValidate) {
    const order = this.currentOrder

    if (order.get_partner() === undefined) {
      this.env.services.dialog.add(AlertDialog, {
        title: _t('Error'), body: _t('The customer is mandatory.')
      })

      return false
    }

    return await super.validateOrder(...arguments)
  },
  /**
   * Overrides `shouldDownloadInvoice` method to never downloading invoice.
   * @returns {boolean}
   */
  shouldDownloadInvoice () {
    return false
  },
  /**
   * Overrides `afterOrderValidation` method to query invoice and set the invoice in the order.
   */
  async afterOrderValidation () {
    await super.afterOrderValidation(...arguments)
    const order = this.currentOrder

    if (order.is_to_invoice() && order.raw.account_move) {
      const invoiceId = order.raw.account_move
      const invoice = await this.invoiceService.getInvoice(invoiceId)

      if (invoice) {
        if (invoice.length > 0) {
          order.set_invoice(invoice[0])
        }
      }
    }
  }

})
