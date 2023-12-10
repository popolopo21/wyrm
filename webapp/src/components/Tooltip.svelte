<script src="ts">
	export let data;
	export let xScale;
	export let yScale;
</script>

<div
	class="tooltip"
	style="position:absolute;
    top: {yScale(data.value) + 3}px;
    left: {xScale(data.date) + 3}px"
>
	<p>{data.tag}:{data.value}</p>
</div>

<style>
	.tooltip {
		padding: 6px;
		background: transparent;
		pointer-events: none;
		transition: cubic-bezier(0.075, 0.82, 0.165, 1);
	}
</style>
