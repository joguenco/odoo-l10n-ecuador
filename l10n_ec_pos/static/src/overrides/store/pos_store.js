/**
 * Author: Jorge Luis
 * Email: jorgeluis@resolvedor.dev
 * Website: https://joguenco.dev
 */
import { patch } from '@web/core/utils/patch'
import { PosStore } from '@point_of_sale/app/store/pos_store'
// import { OrderReceipt } from '@point_of_sale/app/screens/receipt_screen/receipt/order_receipt'

patch(PosStore.prototype, {
  /**
   * Override `getReceiptHeaderData` method to add the invoice to the header.
   * @param {*} order
   * @returns
   */
  getReceiptHeaderData (order) {
    const result = super.getReceiptHeaderData(...arguments)
    result.invoice_id = order.get_invoice()
    return result
  }
/*
  async printReceipt ({
    basic = false,
    order = this.get_order(),
    printBillActionTriggered = false
  } = {}) {
    const orderForPrinting = this.orderExportForPrinting(order)
    const url = `${this.config.epson_printer_ip}/print`
    const lines = buildReceiptLines(orderForPrinting)
    const data = { lines }

    try {
      await fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
      })
    } catch (error) {
      await this.printer.print(
        OrderReceipt,
        {
          data: orderForPrinting,
          formatCurrency: this.env.utils.formatCurrency,
          basic_receipt: basic
        },
        { webPrintFallback: true }
      )
    }

    return true
  }
    */
})

/*
function buildReceiptLines (order) {
  const lines = []

  console.log('order', order)
  console.log('company', order)
  lines.push({ line: `${order.headerData.company.name}` })
  lines.push({ line: `VAT: ${order.headerData.company.vat}` })
  lines.push({ line: `Phone: ${order.headerData.company.phone}` })
  lines.push({ line: `Address: ${order.headerData.company.city} ${order.headerData.company.street}` })
  lines.push({ line: `${order.headerData.company.email}` })
  lines.push({ line: `${order.headerData.company.website}` })
  lines.push({ line: 'Customer Info' })
  lines.push({ line: '- - - - - - - - - - - - - - - - - - - - - ' })
  lines.push({ line: `${order.headerData.partner.name}` })
  lines.push({ line: `VAT: ${order.headerData.partner.vat}` })
  lines.push({ line: `${order.headerData.partner.contact_address.replace(/\n/g, ' ')}` })
  lines.push({ line: `${order.headerData.partner.email}` })
  lines.push({ line: '- - - - - - - - - - - - - - - - - - - - - ' })
  lines.push({ line: 'Product               Qty        Price' })
  lines.push({ line: '- - - - - - - - - - - - - - - - - - - - - ' })

  return lines
}
*/
