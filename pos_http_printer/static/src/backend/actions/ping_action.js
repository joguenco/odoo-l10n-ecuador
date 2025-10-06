import {registry} from "@web/core/registry";

async function pingPrinterAction(env, action) {
    const url = `${action.params.url}/ping`;

    try {
        await fetch(url, {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
            },
        });
        env.services.notification.add("Pong", {type: "success"});
    } catch (error) {
        env.services.notification.add("Fail ping", {type: "danger"});
    }
}

registry.category("actions").add("ping_printer_action", pingPrinterAction);
