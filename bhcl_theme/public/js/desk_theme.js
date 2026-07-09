(function () {
	function pin_workspace_footer() {
		var page = document.getElementById("page-Workspaces");
		if (!page) return;

		var footer = page.querySelector(".workspace-footer");
		if (!footer) return;

		var headContent =
			page.querySelector(".page-head .page-head-content") ||
			page.querySelector(".page-head .container") ||
			page.querySelector(".page-head");
		if (!headContent) return;

		if (footer.closest(".page-head")) {
			footer.classList.add("bhcl-workspace-actions");
			return;
		}

		var host =
			headContent.querySelector(".page-actions") ||
			headContent.querySelector(".flex.col") ||
			headContent.querySelector(".bhcl-workspace-actions-host");

		if (!host) {
			host = document.createElement("div");
			host.className = "bhcl-workspace-actions-host";
			headContent.appendChild(host);
		}

		footer.classList.add("bhcl-workspace-actions");
		host.appendChild(footer);
	}

	function schedule_pin() {
		pin_workspace_footer();
		setTimeout(pin_workspace_footer, 50);
		setTimeout(pin_workspace_footer, 200);
		setTimeout(pin_workspace_footer, 500);
	}

	$(document).on("page-change", schedule_pin);
	$(document).on("form-refresh", schedule_pin);
	frappe.ready(schedule_pin);
})();
