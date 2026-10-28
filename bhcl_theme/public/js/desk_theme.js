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
	// frappe.ready só existe no site (website); no Desk usamos o ready do jQuery
	$(document).ready(schedule_pin);
})();

// Notificações em três níveis: badge com contagem + título da aba (sempre), toast e sino balançando
// na chegada, e faixa abaixo da navbar enquanto houver itens que pedem ação (atribuição, menção, alerta).
(function () {
	var ACTION_TYPES = ["Assignment", "Mention", "Alert"];
	// Alertas puramente informativos não acionam a faixa (ex.: conclusão do OCR de PDF).
	var INFO_DOCTYPES = ["PDF OCR Document"];
	var GROUP_WINDOW_MS = 10000;
	var SNOOZE_MS = 4 * 60 * 60 * 1000;

	var pending = [];
	var group_timer = null;
	var refresh_timer = null;
	var known = new Set();

	function storage(kind) {
		try {
			return window[kind];
		} catch (e) {
			return null;
		}
	}

	function read_key(kind, key) {
		var s = storage(kind);
		if (!s) return null;
		try {
			return JSON.parse(s.getItem(key));
		} catch (e) {
			return null;
		}
	}

	function write_key(kind, key, value) {
		var s = storage(kind);
		if (!s) return;
		try {
			s.setItem(key, JSON.stringify(value));
		} catch (e) {
			// armazenamento bloqueado: a faixa só não lembra o adiamento
		}
	}

	function key(name) {
		return "bhcl_notif_" + name + "_" + frappe.session.user;
	}

	function plain_text(html, max) {
		var text = new DOMParser().parseFromString(html || "", "text/html").body.textContent || "";
		text = text.replace(/\s+/g, " ").trim();
		return text.length > max ? text.slice(0, max - 1) + "…" : text;
	}

	function is_action(log) {
		return ACTION_TYPES.includes(log.type) && !INFO_DOCTYPES.includes(log.document_type);
	}

	function log_link(log) {
		if (log.link) return log.link;
		return frappe.utils.get_form_link(
			log.document_type || "Notification Log",
			log.document_name || log.name,
		);
	}

	function bell() {
		return $(".navbar .dropdown-notifications .notifications-icon");
	}

	function fetch_unread() {
		return frappe
			.call({
				method: "frappe.client.get_list",
				args: {
					doctype: "Notification Log",
					filters: { for_user: frappe.session.user, read: 0 },
					fields: ["name", "type", "subject", "document_type", "document_name", "link"],
					order_by: "creation desc",
					limit_page_length: 100,
				},
				type: "GET",
			})
			.then(function (r) {
				return r.message || [];
			});
	}

	function render_badge(count) {
		var $bell = bell();
		if (!$bell.length) return;
		var $badge = $bell.find(".bhcl-notif-badge");
		if (!count) {
			$badge.remove();
		} else {
			if (!$badge.length) {
				$badge = $('<span class="bhcl-notif-badge" aria-hidden="true"></span>').appendTo($bell);
			}
			$badge.text(count >= 100 ? "99+" : count > 9 ? "9+" : String(count));
		}
		$bell.attr(
			"aria-label",
			count ? __("Notificações: {0} não lidas", [count]) : __("Notificações"),
		);
		var prefix = count ? "(" + (count >= 100 ? "99+" : count) + ")" : "";
		// antes do primeiro set_title não há título a reaplicar: o core quebraria em undefined.replace
		if (frappe._original_title === undefined) frappe._title_prefix = prefix;
		else frappe.utils.set_title_prefix(prefix);
	}

	// O adiamento/fechamento vale para o conjunto atual: um item novo que pede ação reabre a faixa.
	function render_action_bar(actions) {
		var $bar = $(".bhcl-action-bar");
		var latest = actions.length ? actions[0].name : null;
		var snooze = read_key("localStorage", key("snooze"));
		var dismissed = read_key("sessionStorage", key("dismissed"));
		var hidden =
			!latest ||
			(snooze && snooze.latest === latest && snooze.until > Date.now()) ||
			dismissed === latest;

		if (hidden) {
			$bar.remove();
			$("body").removeClass("bhcl-has-action-bar");
			return;
		}

		if (!$bar.length) {
			$bar = $(
				'<div class="bhcl-action-bar" role="status">' +
					'<span class="bhcl-action-bar-icon">' +
					frappe.utils.icon("notification", "sm") +
					"</span>" +
					'<span class="bhcl-action-bar-text"></span>' +
					'<button type="button" class="btn btn-xs btn-primary bhcl-action-open"></button>' +
					'<button type="button" class="btn btn-xs btn-default bhcl-action-snooze"></button>' +
					'<button type="button" class="btn-reset bhcl-action-close"></button>' +
					"</div>",
			);
			$bar.find(".bhcl-action-open").text(__("Ver"));
			$bar.find(".bhcl-action-snooze").text(__("Lembrar mais tarde"));
			$bar
				.find(".bhcl-action-close")
				.attr({ title: __("Fechar"), "aria-label": __("Fechar") })
				.html(frappe.utils.icon("close", "sm"));
			$(".sticky-top").first().append($bar);
		}

		$bar.data("latest", latest);
		$bar.data("actions", actions);
		$bar
			.find(".bhcl-action-bar-text")
			.text(
				actions.length === 1
					? __("Você tem 1 item aguardando sua ação: {0}", [plain_text(actions[0].subject, 90)])
					: __("Você tem {0} itens aguardando sua ação.", [
							actions.length >= 100 ? "99+" : actions.length,
						]),
			);
		$("body").addClass("bhcl-has-action-bar");
	}

	function apply(logs) {
		known = new Set(logs.map((log) => log.name));
		render_badge(logs.length);
		render_action_bar(logs.filter(is_action));
	}

	function refresh() {
		return fetch_unread().then(apply);
	}

	function schedule_refresh(delay) {
		clearTimeout(refresh_timer);
		refresh_timer = setTimeout(refresh, delay || 0);
	}

	function ring() {
		var $bell = bell();
		$bell.removeClass("bhcl-bell-ring");
		// força reflow para a animação recomeçar se já estiver aplicada
		void ($bell[0] && $bell[0].offsetWidth);
		$bell.addClass("bhcl-bell-ring");
	}

	function flush_toasts() {
		group_timer = null;
		if (document.hidden || !pending.length) return;
		var logs = pending;
		pending = [];
		ring();
		if (logs.length === 1) {
			var log = logs[0];
			frappe.show_alert(
				{
					message:
						'<a class="bhcl-notif-toast" href="' +
						encodeURI(log_link(log)) +
						'">' +
						frappe.utils.escape_html(plain_text(log.subject, 140)) +
						"</a>",
					indicator: is_action(log) ? "orange" : "blue",
				},
				6,
			);
		} else {
			frappe.show_alert(
				{
					message:
						'<a class="bhcl-notif-toast" href="#" data-bhcl-open-notifications="1">' +
						frappe.utils.escape_html(__("{0} novas notificações", [logs.length])) +
						"</a>",
					indicator: logs.some(is_action) ? "orange" : "blue",
				},
				6,
			);
		}
	}

	function on_new_notification() {
		fetch_unread().then(function (logs) {
			var fresh = logs.filter((log) => !known.has(log.name));
			apply(logs);
			if (!fresh.length) return;
			pending = pending.concat(fresh);
			if (!group_timer && !document.hidden) {
				// mostra a primeira na hora e agrupa as que chegarem na sequência
				flush_toasts();
				group_timer = setTimeout(flush_toasts, GROUP_WINDOW_MS);
			}
		});
	}

	function go_to(url) {
		if (/^(https?:)?\/\//.test(url) || url.charAt(0) === "/") {
			window.location.href = url;
		} else {
			frappe.set_route(url);
		}
	}

	function open_list() {
		frappe.set_route("List", "Notification Log", { read: 0 });
		schedule_refresh(800);
	}

	function open_actions(actions) {
		if (actions.length !== 1) return open_list();
		var log = actions[0];
		frappe.call({
			method: "frappe.desk.doctype.notification_log.notification_log.mark_as_read",
			args: { docname: log.name },
			callback: function () {
				schedule_refresh(300);
			},
		});
		go_to(log_link(log));
	}

	// O core guarda em route_titles o título já prefixado e o devolve ao voltar à rota, o que
	// empilha "(1) (1) ...". Removemos prefixos de contagem recebidos para o prefixo ser único.
	function patch_set_title() {
		if (frappe.utils._bhcl_set_title_patched) return;
		frappe.utils._bhcl_set_title_patched = true;
		var original = frappe.utils.set_title;
		frappe.utils.set_title = function (title) {
			if (typeof title !== "string") title = document.title || "";
			title = title.replace(/^(\(\d+\+?\)\s*)+/, "");
			return original.call(frappe.utils, title);
		};
	}

	function setup() {
		if (!frappe.session || frappe.session.user === "Guest" || !frappe.realtime) return;
		// sem o sino (notificações desligadas nas Desk Settings) não há o que destacar
		if (!bell().length) return;
		patch_set_title();

		frappe.realtime.on("notification", on_new_notification);
		frappe.realtime.on("indicator_hide", function () {
			schedule_refresh(300);
		});

		var $dropdown = $(".navbar .dropdown-notifications");
		$dropdown.on("hidden.bs.dropdown", function () {
			schedule_refresh(300);
		});
		// marcar como lida (item, "marcar todas") é feito pelo Frappe; recontamos logo depois
		$dropdown.on("click", ".notifications-list", function () {
			schedule_refresh(800);
		});

		$(document).on("click", ".bhcl-action-open", function () {
			open_actions($(".bhcl-action-bar").data("actions") || []);
		});
		$(document).on("click", ".bhcl-action-snooze", function () {
			var latest = $(".bhcl-action-bar").data("latest");
			write_key("localStorage", key("snooze"), { latest: latest, until: Date.now() + SNOOZE_MS });
			refresh();
		});
		$(document).on("click", ".bhcl-action-close", function () {
			write_key("sessionStorage", key("dismissed"), $(".bhcl-action-bar").data("latest"));
			refresh();
		});
		$(document).on("click", "[data-bhcl-open-notifications]", function (e) {
			e.preventDefault();
			open_list();
		});
		$(document).on("animationend", ".bhcl-bell-ring", function () {
			$(this).removeClass("bhcl-bell-ring");
		});
		document.addEventListener("visibilitychange", function () {
			if (document.hidden) return;
			schedule_refresh(0);
			if (pending.length && !group_timer) flush_toasts();
		});

		refresh();
	}

	$(document).ready(function () {
		// a navbar e frappe.realtime só existem depois do boot do Desk
		setTimeout(setup, 500);
	});
})();
