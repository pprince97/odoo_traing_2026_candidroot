odoo.define('library_management_rushvi.collection_filter', function (require) {
    'use strict';

    var publicWidget = require('web.public.widget');

    publicWidget.registry.CollectionFilter = publicWidget.Widget.extend({
        selector: '.js_collection_filter',
        events: {
            'change': '_onChange',
        },

        _onChange: function () {
            let selected = [];
            document.querySelectorAll('.js_collection_filter:checked').forEach(el => {
                selected.push(el.value);
            });

            let params = new URLSearchParams(window.location.search);

            if (selected.length) {
                params.set('collection', selected.join(','));
            } else {
                params.delete('collection');
            }

            window.location.search = params.toString();
        },
    });
