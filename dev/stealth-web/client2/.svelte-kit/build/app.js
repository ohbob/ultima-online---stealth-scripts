import { respond } from '@sveltejs/kit/ssr';
import root from './generated/root.svelte';
import { set_paths } from './runtime/paths.js';
import { set_prerendering } from './runtime/env.js';
import * as user_hooks from "./hooks.js";

const template = ({ head, body }) => "<!DOCTYPE html>\r\n<html lang=\"en\">\r\n\t<head>\r\n\r\n\t\t<meta charset=\"utf-8\" />\r\n\t\t<!--\t\t<link rel=\"icon\" href=\"assets/favicon.ico\" />-->\r\n\t\t<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />\r\n\t\t<title>Stealth web client</title>\r\n\t\t" + head + "\r\n\t</head>\r\n<!--\t<body class=\"font-sans antialiased\">-->\r\n\t<body class=\"bg-gray-50\">\r\n\t\t<div id=\"svelte\">" + body + "</div>\r\n\t</body>\r\n</html>\r\n\r\n\r\n";

let options = null;

// allow paths to be overridden in svelte-kit preview
// and in prerendering
export function init(settings) {
	set_paths(settings.paths);
	set_prerendering(settings.prerendering || false);

	options = {
		amp: false,
		dev: false,
		entry: {
			file: "/./_app/start-a81726f1.js",
			css: ["/./_app/assets/start-0826e215.css"],
			js: ["/./_app/start-a81726f1.js","/./_app/chunks/vendor-1a343f14.js"]
		},
		fetched: undefined,
		floc: false,
		get_component_path: id => "/./_app/" + entry_lookup[id],
		get_stack: error => String(error), // for security
		handle_error: error => {
			console.error(error.stack);
			error.stack = options.get_stack(error);
		},
		hooks: get_hooks(user_hooks),
		hydrate: true,
		initiator: undefined,
		load_component,
		manifest,
		paths: settings.paths,
		read: settings.read,
		root,
		router: true,
		ssr: true,
		target: null,
		template,
		trailing_slash: "never"
	};
}

const d = decodeURIComponent;
const empty = () => ({});

const manifest = {
	assets: [{"file":"favicon.ico","size":15086,"type":"image/vnd.microsoft.icon"},{"file":"site.webmanifest","size":426,"type":"application/manifest+json"}],
	layout: "src/routes/__layout.svelte",
	error: "src/routes/__error.svelte",
	routes: [
		{
						type: 'page',
						pattern: /^\/$/,
						params: empty,
						a: ["src/routes/__layout.svelte", "src/routes/index.svelte"],
						b: ["src/routes/__error.svelte"]
					}
	]
};

// this looks redundant, but the indirection allows us to access
// named imports without triggering Rollup's missing import detection
const get_hooks = hooks => ({
	getSession: hooks.getSession || (() => ({})),
	handle: hooks.handle || (({ request, resolve }) => resolve(request))
});

const module_lookup = {
	"src/routes/__layout.svelte": () => import("..\\..\\src\\routes\\__layout.svelte"),"src/routes/__error.svelte": () => import("..\\..\\src\\routes\\__error.svelte"),"src/routes/index.svelte": () => import("..\\..\\src\\routes\\index.svelte")
};

const metadata_lookup = {"src/routes/__layout.svelte":{"entry":"/./_app/pages/__layout.svelte-9fea9cec.js","css":["/./_app/assets/pages/__layout.svelte-e6dfdda8.css"],"js":["/./_app/pages/__layout.svelte-9fea9cec.js","/./_app/chunks/vendor-1a343f14.js"],"styles":null},"src/routes/__error.svelte":{"entry":"/./_app/pages/__error.svelte-20e84a1e.js","css":[],"js":["/./_app/pages/__error.svelte-20e84a1e.js","/./_app/chunks/vendor-1a343f14.js"],"styles":null},"src/routes/index.svelte":{"entry":"/./_app/pages/index.svelte-23215ff4.js","css":[],"js":["/./_app/pages/index.svelte-23215ff4.js","/./_app/chunks/vendor-1a343f14.js"],"styles":null}};

async function load_component(file) {
	return {
		module: await module_lookup[file](),
		...metadata_lookup[file]
	};
}

init({ paths: {"base":"","assets":"/."} });

export function render(request, {
	prerender
} = {}) {
	const host = request.headers["host"];
	return respond({ ...request, host }, options, { prerender });
}