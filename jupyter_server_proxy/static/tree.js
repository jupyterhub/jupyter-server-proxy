define(["jquery", "base/js/namespace", "base/js/utils"], function (
  $,
  Jupyter,
  utils,
) {
  var $ = require("jquery");
  var Jupyter = require("base/js/namespace");
  var utils = require("base/js/utils");

  var base_url = utils.get_body_data("baseUrl");

  function load() {
    if (!Jupyter.notebook_list) return;

    var servers_info_url = base_url + "server-proxy/servers-info";
    $.get(servers_info_url, function (data) {
      /* locate the right-side dropdown menu of apps and notebooks */
      var $menu = $(".tree-buttons").find(".dropdown-menu");

      /* create a divider */
      var $divider = $("<li>").attr("role", "presentation").addClass("divider");

      /* add the divider */
      $menu.append($divider);

      $.each(data.server_processes, function (_, server_process) {
        if (!server_process.launcher_entry.enabled) {
          return;
        }

        /* create our list item */
        var $entry_container = $("<li>")
          .attr("role", "presentation")
          .addClass("new-" + server_process.name);

        /* create our list item's link */
        var $entry_link = $("<a>")
          .attr("role", "menuitem")
          .attr("tabindex", "-1")
          .attr("href", base_url + server_process.launcher_entry.path_info)
          .attr("target", "_blank")
          .text(server_process.launcher_entry.title);

        /* add the link to the item and
         * the item to the menu */
        $entry_container.append($entry_link);
        $menu.append($entry_container);
      });
    });
  }

  return {
    load_ipython_extension: load,
  };
});
