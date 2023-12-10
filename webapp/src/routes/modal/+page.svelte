<script lang="ts">
	import * as d3 from 'd3';
	import type { PageData } from './$types';
	import Tooltip from '../../components/Tooltip.svelte';
	import Chat from '../../components/Chat.svelte';
	import type { ProcessedDataType, DataValue } from '$lib/types';
	import { getChatID, newChat } from '$lib/chat';

	export let width = 640;
	export let height = 400;
	export let marginTop = 20;
	export let marginRight = 20;
	export let marginBottom = 20;
	export let marginLeft = 20;

	let showChat = false;
	export let data: PageData;
	let dates = data.d3Data.map((d) => d.time);
	const chartDefinition =
		'This is a linechart which shows each topic keyword count on a specific timeframe';
	let timeDomain: d3.ScaleTime<number, number, never>;
	$: timeDomain = d3
		.scaleTime()
		.domain(d3.extent(dates) as [Date, Date])
		.range([marginLeft, width - marginRight])
		.nice();

	let y: number;
	$: y = d3
		.scaleLinear()
		.domain([0, 99])
		.range([height - marginBottom, marginTop]);

	let gx: any;
	let gy: any;
	$: d3.select(gx).call(d3.axisBottom(timeDomain));
	$: d3.select(gy).call(d3.axisLeft(y));

	let allTags = new Set();
	data.d3Data.forEach((element) => {
		Object.keys(element.tags).forEach((tag) => {
			allTags.add(tag);
		});
	});

	let processedData = new Map();

	data.d3Data.forEach((d) => {
		const date = new Date(d.time); // Convert time to Date object
		Object.entries(d.tags).forEach(([tag, value]) => {
			if (!processedData.has(tag)) {
				processedData.set(tag, []);
			}
			processedData.get(tag).push({ date, value });
		});
	});

	let filteredData = new Map();

	processedData.forEach((values, tag) => {
		if (values.length > 0 && values[values.length - 1].value > 5) {
			filteredData.set(tag, values);
		}
	});

	let lineGenerator = d3
		.line()
		.x((d) => timeDomain(d.date))
		.y((d) => y(d.value))
		.curve(d3.curveBasis); // You can choose the type of curve
	let colors = d3.scaleOrdinal(d3.schemeCategory10); // For different colors

	let hoveredData = {};
</script>

<div class="chart-container">
	<svg {width} {height} on:click={() => {
		showChat = true;
		newChat()
	}}>
		<g
			bind:this={gx}
			transform="translate(0,{height - marginBottom})"
			color="black"
		/>
		<g
			bind:this={gy}
			transform="translate({marginLeft},0)"
			color="black"
		/>
		{#each Array.from(filteredData.keys()) as tag (tag)}
			<path
				role="figure"
				d={lineGenerator(filteredData.get(tag))}
				stroke={colors(tag)}
				fill="none"
			/>
			{#each filteredData.get(tag) as point}
				<circle
					role="figure"
					cx={timeDomain(point.date)}
					cy={y(point.value)}
					r={hoveredData?.date == point.date &&
					hoveredData?.value == point.value &&
					hoveredData?.tag == tag
						? '10'
						: '5'}
					fill={colors(tag)}
					on:mouseover={() => {
						hoveredData = {
							tag: tag,
							date: point.date,
							value: point.value
						};
					}}
					on:mouseleave={() => {
						hoveredData = null;
					}}
				/>
			{/each}
		{/each}
	</svg>
	{#if hoveredData}
		<Tooltip data={hoveredData} xScale={timeDomain} yScale={y} />
	{/if}

	{#if showChat}
		<Chat chartData={filteredData} {chartDefinition} />
	{/if}
</div>
