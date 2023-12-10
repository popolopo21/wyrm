<script lang="ts">
	import { onMount } from 'svelte';
	import { T } from '@threlte/core';
	import { Align, Grid, OrbitControls } from '@threlte/extras';
	import type { anyad } from '$lib/types';
	import { Text } from '@threlte/extras';
	import { interactivity } from '@threlte/extras';
	import { spring } from 'svelte/motion';

	interactivity();

	const scale = spring(1);
	export let articles: anyad[];
</script>

<Grid
	infiniteGrid
	sectionColor="#4a4b4a"
	sectionSize={20}
	cellSize={20}
	fadeDistance={400}
/>

<T.PerspectiveCamera makeDefault position={[10, 100, 100]} fov={60}>
	<OrbitControls enableDamping />
</T.PerspectiveCamera>

<T.AmbientLight color="#fff" intensity={0.4} />
<T.DirectionalLight
	position={[20, 3, 200]}
	intensity={4}
	color="#fff"
/>
<T.DirectionalLight
	position={[0, 200, -200]}
	color="#fff"
	intensity={2}
/>

<Align auto position.y={100}>
	{#each articles as domain, i}
		<T.Mesh position={[-20, 0, -9 + 18 * i]} rotation={[-1.5, 0, 0]}>
			<Text
				text={String(domain.domain).replace('https://', '')}
				fontSize={18}
				anchorX="100%"
				anchorY="10%"
			/>
		</T.Mesh>
		{#each domain.articles as day, j}
			{#if day}
				<T.Group position={[0, 0, 18 * i]}>
					<T.Mesh
						position={[18 * j, day.elements.length / 2, 0]}
						scale={$scale}
						on:pointerenter={() => scale.set(1.5)}
						on:pointerleave={() => scale.set(1)}
						on:click={() => {
							console.log(day.key.day);
						}}
					>
						<T.BoxGeometry args={[10, day.elements.length, 10]} />
						<T.MeshStandardMaterial color="orange" />
					</T.Mesh>
					{#if i === 0}
						<T.Mesh
							position={[18 * j + 2, 0, 45]}
							rotation={[-1.5, 0, 1.2]}
						>
							<Text
								text={String(day.key.day)}
								fontSize={9}
								anchorX="100%"
								anchorY="100%"
							/>
						</T.Mesh>
					{/if}
				</T.Group>
			{/if}
		{/each}
	{/each}
</Align>
