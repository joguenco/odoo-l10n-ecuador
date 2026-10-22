/** @odoo-module **/

import {registry} from "@web/core/registry";
import {useService} from "@web/core/utils/hooks";

const {Component, useState, onWillStart} = owl;

export class OwlOneDashboard extends Component {
    setup() {
        this.state = useState({
            title: "",
            information: [],
            countModules: [],
        });

        this.orm = useService("orm");

        onWillStart(async () => {
            console.log("onWillStart");
            this.state.title = "Dashboard";
        });
    }
}

OwlOneDashboard.template = "owl.OneDashboard";

registry.category("actions").add("owl.one_dashboard", OwlOneDashboard);
