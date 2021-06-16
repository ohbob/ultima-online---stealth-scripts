import preprocess from "svelte-preprocess";
import adapter from '@sveltejs/adapter-static';
import imagePreprocessor from 'svimg';

/** @type {import('@sveltejs/kit').Config} */
const config = {
	preprocess: [
		imagePreprocessor({
			inputDir: 'static',
			outputDir: 'static/g',
			webp: true,
			avif: true
		}),
		preprocess({
			postcss: true
		}),
	],
	kit: {
		// hydrate the <div id="svelte"> element in src/app.html
		// target: '#svelte',
		adapter: adapter({
			// default options are shown
			pages: 'public/svelte/',
			assets: 'public/svelte/',
			fallback: null
		})
	}

};

export default config;
