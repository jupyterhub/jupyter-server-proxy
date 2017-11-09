define(function(require) {
    var $ = require('jquery');
    var Jupyter = require('base/js/namespace');
    var utils = require('base/js/utils');

    var base_url = utils.get_body_data('baseUrl');


    function load() {
        if (!Jupyter.notebook_list) return;

        /* locate the right-side dropdown menu of apps and notebooks */
        var menu = $('.tree-buttons').find('.dropdown-menu');

        /* create a divider */
        var divider = $('<li>')
            .attr('role', 'presentation')
            .addClass('divider');

        /* add the divider */
        menu.append(divider);

        /* create our list item */
        var rsession_item = $('<li>')
            .attr('role', 'presentation')
            .addClass('new-rstudio');

        /* create our list item's link */
        var rsession_link = $('<a>')
            .attr('role', 'menuitem')
            .attr('tabindex', '-1')
            .attr('href', base_url + 'rstudio/')
            .attr('target', '_blank')
            .text('RStudio Session');

        /* add the link to the item and
         * the item to the menu */
        rsession_item.append(rsession_link);
        menu.append(rsession_item);
    }

    return {
        load_ipython_extension: load
    };
});
