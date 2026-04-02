import { Component, xml } from "@odoo/owl";
import { Notebook } from "@web/core/notebook/notebook";
import { registry } from "@web/core/registry";

class PageComponent extends Component {
  static template = xml`
    <h1 t-esc="props.title" />
    <p t-esc="props.text" />
  `;
}

class NotebookComponent extends Component {
  static template = xml`
  <div class="container border my-3">
    <Notebook defaultPage="'page_2'" pages="pages"/>
  </div>
  `;
  static components = { Notebook };
  get pages() {
    return [
      {
        Component: PageComponent,
        title: "Page 1",
        props: {
          title: "My First Page",
          text: "This page is not visible",
        },
      },
      {
        Component: PageComponent,
        id: "page_2",
        title: "Page 2",
        props: {
          title: "My second page",
          text: "You're at the right place!",
        },
      },
    ]
  }
}
registry.category("actions").add("owl_js_practice.notebook_action", NotebookComponent);