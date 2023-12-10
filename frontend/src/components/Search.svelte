<script lang="ts">
	import { enhance } from "$app/forms";

    let text = ""
    let startDate = new Date()
    let endDate = new Date()
    let loading = false;
</script>

<html>
    <body>
        <h1>Submit your text here!</h1>
        <form method="post" use:enhance={()=>{
            loading=true;
            return async({update}) =>{
                await update();
                loading = false;
            }
        }}>
            <input type="text" name="text" disabled={loading}/>
            <input type="date" name="startDate" disabled={loading}/>
            <input type="date" name="endDate" disabled={loading}/>
            <button type="submit" disabled={loading}>Submit</button>
            {#if loading}
                <p>The thing is loading!</p>
            {/if}
        </form>
    </body>
</html>
