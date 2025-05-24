/**
 * Author: Jorge Luis
 * Email: jorgeluis@resolvedor.dev
 * Website: https://joguenco.dev
 */

import { PosOrder } from '@point_of_sale/app/models/pos_order'
import { patch } from '@web/core/utils/patch'

patch(PosOrder.prototype, {

  setup (_defaultObj, options) {
    super.setup(...arguments)
    // Initial value for to_invoice when screen is loaded
    this.to_invoice = true
    this.invoice_id = false
  },
  /**
   * Override `export_for_printing` method to add the partner data to the header.
   */
  export_for_printing (baseUrl, headerData) {
    const results = super.export_for_printing(...arguments)

    if (this.get_partner()) {
      results.headerData.partner = this.get_partner()
    }

    if (this.get_invoice()) {
      results.invoice_id = this.get_invoice()
    }

    return results
  },

  /**
   * Override `set_to_invoice` method so that it is always an invoice.
   */
  set_to_invoice (to_invoice) {
    super.set_to_invoice(...arguments)
    this.to_invoice = true
  },

  set_invoice (invoice) {
    this.invoice_id = invoice
  },

  get_invoice () {
    return this.invoice_id
  }

})
