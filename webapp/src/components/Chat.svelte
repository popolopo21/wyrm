<script lang="ts">
	import { enhance } from '$app/forms';
	import { getChatID } from '$lib/chat';
	import { ChatPromptTemplate } from 'langchain/prompts';
	export let chartData = new Map();
	export let chartDefinition: string;

	function convertDataToString(filteredData) {
		let stringRepresentation = '';

		filteredData.forEach((values, tag) => {
			stringRepresentation += `Tag: ${tag}\n`;
			values.forEach(({ date, value }) => {
				// Format date to a readable string (e.g., YYYY-MM-DD)
				let formattedDate = date.toISOString().split('T')[0];
				stringRepresentation += `  Date: ${formattedDate}, Value: ${value}\n`;
			});
			stringRepresentation += '\n'; // Add an extra line for separation between tags
		});

		return stringRepresentation;
	}
	let chatID = getChatID() || "ChatID not found in sessionStorage";
</script>

<main class="max-w-4xl mx-auto p-4">
	<h1 class="text-4xl">Here is your Chatbot!</h1>
	<form class="grid gap-4" method='post' use:enhance>
		<div>
			<label for="prompt" />
			<input name="message" type="text" />
			<input type="hidden" value={chatID} name="chatID"/>
		</div>
		<div>
			<button type="submit">Submit</button>
		</div>
	</form>
</main>
