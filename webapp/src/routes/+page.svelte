<script lang="ts">
	import type { PageData } from './$types';
	export let data: PageData;
</script>

<div class="container">
	<form>
		<label for="searchInput">Keresés</label>
		<input id="searchInput" name="searchTerm" type="search" />
		<button class="anyad" type="submit">Keresés</button>
	</form>

	<ul>
		{#each data.results as result}
			<li><a href={result.url}>{result.title}</a></li>
		{/each}
	</ul>
</div>

<style>
    .container {
        max-width: 60rem;
        margin: auto;
        padding: 4rem;
    }
    .anyad {
        max-width: 15rem;
        margin: auto;
    }
</style>
