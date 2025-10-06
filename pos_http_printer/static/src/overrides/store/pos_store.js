/**
 * Author: Jorge Luis
 * Email: jorgeluis@resolvedor.dev
 * Website: https://joguenco.dev
 */
import {patch} from "@web/core/utils/patch";
import {PosStore} from "@point_of_sale/app/store/pos_store";
import {OrderReceipt} from "@point_of_sale/app/screens/receipt_screen/receipt/order_receipt";

patch(PosStore.prototype, {
    /**
     * Override `getReceiptHeaderData` method to add the invoice to the header.
     * @param {*} order
     * @returns
     */

    async printReceipt({
        basic = false,
        order = this.get_order(),
        printBillActionTriggered = false,
    } = {}) {
        const orderForPrinting = this.orderExportForPrinting(order);

        if (this.config.http_printer_ip) {
            const url = `${this.config.http_printer_ip}/print`;
            const lines = this.buildReceiptLines(orderForPrinting);
            const data = {lines};

            try {
                await fetch(url, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify(data),
                });
            } catch (error) {
                this.env.services.notification.add("Fail print", {type: "danger"});
                return false;
            }
        } else {
            await this.printer.print(
                OrderReceipt,
                {
                    data: orderForPrinting,
                    formatCurrency: this.env.utils.formatCurrency,
                    basic_receipt: basic,
                },
                {webPrintFallback: true}
            );
        }

        return true;
    },

    buildReceiptLines(order) {
        const lines = [];

        lines.push({line: `${order.headerData.company.name}`});
        lines.push({line: `RUC: ${order.headerData.company.vat}`});
        lines.push({
            line: `Dirección: ${order.headerData.company.city} ${order.headerData.company.street}`,
        });
        lines.push({line: `Teléfono: ${order.headerData.company.phone}`});
        if (order.headerData.company.email) {
            lines.push({line: `${order.headerData.company.email}`});
        }
        if (order.headerData.company.website) {
            lines.push({line: `${order.headerData.company.website}`});
        }
        lines.push({line: "Clave de Acceso: "});
        lines.push({line: `${order.invoice_id.l10n_ec_xml_access_key}`});
        lines.push({line: `${order.invoice_id.name}`});
        lines.push({line: `Fecha: ${order.invoice_id.invoice_date}`});
        lines.push({line: `Cliente: ${order.headerData.partner.name}`});
        lines.push({line: `Identificación: ${order.headerData.partner.vat}`});
        if (order.headerData.partner.street) {
            lines.push({line: `Dirección: ${order.headerData.partner.street}`});
        }
        if (order.headerData.partner.email) {
            lines.push({line: `${order.headerData.partner.email}`});
        }
        lines.push({line: "- - - - - - - - - - - - - - - - - - - - - - - -"});
        lines.push({line: "Producto                         #       Precio"});
        lines.push({line: "- - - - - - - - - - - - - - - - - - - - - - - -"});
        for (const l of order.orderlines) {
            const productName = l.productName.padEnd(27).slice(0, 27);
            const quantity = l.qty.padStart(9);
            const price = l.price.slice(2).padStart(9);

            lines.push({line: `${productName} ${quantity} ${price}`});
        }
        lines.push({line: "- - - - - - - - - - - - - - - - - - - - - - - -"});

        const subtotal = this.env.utils.formatCurrency(order.total_without_tax, false);
        const tax = this.env.utils.formatCurrency(order.taxTotals.tax_amount, false);
        const total = this.env.utils.formatCurrency(order.total_paid, false);

        lines.push({line: `${"".padStart(27)} Subtotal: ${subtotal.padStart(9)}`});
        lines.push({line: `${"".padStart(27)}      IVA: ${tax.padStart(9)}`});
        lines.push({line: `${"".padStart(27)}    Total: ${total.padStart(9)}`});
        lines.push({line: `Forma de Pago:`});
        for (const payment of order.paymentlines) {
            lines.push({line: `- ${payment.name}: ${payment.amount}`});
        }

        return lines;
    },
});
