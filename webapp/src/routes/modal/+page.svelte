<script lang="ts">
  import * as d3 from "d3";
  import type {PageData} from "./$types"
  
  export let width = 640;
  export let height = 400;
  export let marginTop = 20;
  export let marginRight = 20;
  export let marginBottom = 20;
  export let marginLeft = 20;
  
  export let data: PageData;

  let dates = data.d3Data.map(d => d.time)

  let timeDomain: d3.ScaleTime<number,number,never>;
  $: timeDomain = d3
      .scaleTime()
      .domain(d3.extent(dates) as [Date, Date])
      .range([marginLeft, width - marginRight])
      .nice();

  let y: number;
  $: y= d3.scaleLinear()
      .domain([0, 99])
      .range([height - marginBottom, marginTop])


  let gx: any;
  let gy: any;
  $: d3.select(gx).call(d3.axisBottom(timeDomain))
  $: d3.select(gy).call(d3.axisLeft(y))

  let allTags= new Set();
  data.d3Data.forEach(element => {
    Object.keys(element.tags).forEach(tag => {
      allTags.add(tag);
    })
  });

  let processedData = new Map();
  data.d3Data.forEach(d => {
    const date = new Date(d.time); // Convert time to Date object
    Object.entries(d.tags).forEach(([tag, value]) => {
      if (!processedData.has(tag)) {
        processedData.set(tag, []);
      }
      processedData.get(tag).push({ date, value });
    });
  });
  console.debug(processedData);

  let lineGenerator = d3.line()
    .x(d => timeDomain(d.date))
    .y(d => y(d.value))
    .curve(d3.curveBasis); // You can choose the type of curve

  let colors = d3.scaleOrdinal(d3.schemeCategory10); // For different colors
</script>

<svg width={width} height={height}>
  <g bind:this={gx} transform="translate(0,{height - marginBottom})" color="black" />
  <!-- Add y-axis -->
  <g bind:this={gy} transform="translate({marginLeft},0)" color="black" />
  {#each Array.from(processedData.keys()) as tag (tag)}
    <path d={lineGenerator(processedData.get(tag))}
          stroke={colors(tag)}
          fill="none"></path>
  {/each}
</svg>

