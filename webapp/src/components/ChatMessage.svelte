<script lang="ts">
</script>

<main class="max-w-4xl mx-auto p-4">
	<h1 class="text-4xl">Here is your Chatbot!</h1>

	<form
		method="post"
		class="grid gap-4"
		on:submit|preventDefault={handleSubmit}
	>
		<div>
			<label for="prompt" />
			<textarea name="prompt" id="prompt">
				Ask your question!
			</textarea>
		</div>
		<div>
			<button type="submit" />
		</div>
	</form>
</main>
