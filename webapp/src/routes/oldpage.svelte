<script lang="ts">
	import { Canvas } from '@threlte/core';
	import Scene from '../components/Scene.svelte';
	import type { PageData } from './$types';
	export let data: PageData;
</script>

<div class="scene">
	<Canvas>
		<Scene articles={data.articles} />
	</Canvas>
</div>

<style>
	.scene {
		position: absolute;
		inset: 0;
		background-color: hsl(200, 10%, 10%);
	}
</style>
