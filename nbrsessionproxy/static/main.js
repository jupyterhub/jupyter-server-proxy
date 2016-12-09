define(['jquery', 'base/js/namespace', 'base/js/utils'], function($, namespace, utils) {

	var base_url = utils.get_body_data('baseUrl');

	function open_rsession(data) {
		console.log("response: " + data);
		var proxy_url;
		if ("url" in data) {
			proxy_url = data['url'];
		} else {
			/* debug hack */
			proxy_url = base_url + 'proxy/8001/';
		}
		var w = window.open(proxy_url, "_blank");
		w.focus();
	}

    function load() {
		console.log("nbrsessionproxy loading");
        if (!namespace.notebook_list) return;

		/* the url we POST to to start rsession */
        var rsp_url = base_url + 'rsessionproxy';
        console.log("nbrsessionproxy: url: " + rsp_url);

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
            .addClass('new-rsessionproxy');

		/* create our list item's link */
		var rsession_link = $('<a>')
			.attr('role', 'menuitem')
			.attr('tabindex', '-1')
			.text('RStudio Session')
			.on('click', function() {
				$.post(rsp_url, {}, open_rsession);
			});

		/* add the link to the item and
         * the item to the menu */
		rsession_item.append(rsession_link);
		menu.append(rsession_item);
    }

	var load_ipython_extension = function () {
        load();
    }

    return {
        load_ipython_extension: load_ipython_extension,
    };

});
