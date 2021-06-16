<section class="bg-gray-100">
    <div on:click={toggle} class="bg-gray-100 p-1">
        {show ? "<" : ">"}
        Journal
    </div>
    {#if show}
        <ul style="height:400px; overflow:hidden; overflow-y:scroll;">
            {#each journal.slice(-0) as entry}
                <li class="text-center text-sm p-1">{entry}</li>
            {/each}
        </ul>

        <form class="flex" on:submit|preventDefault={say(message)}>
            <input on:keyup|preventDefault
                   	bind:this={inputField}

                   bind:value={message} type="text" class="mt-2 mb-2 w-full px-4"
               placeholder="Send message">
            <button class="border-black border-1 bg-white mt-2 mb-2 w-20 px-4" type="submit" on:click={() => inputField.value = ''}>
                Submit
            </button>
        </form>
    {/if}

</section>

<script>
    let journal = []
    export let show = false
    let message
    let inputField

    function toggle() {
        show = !show;
    }

    function getJournal() {
        if (show) {
            fetch("http://localhost:8000/journal")
                .then(response => response.text())
                .then(response => journal = JSON.parse(response))
        }
    }

    function say(message) {
        fetch(`http://localhost:8000/say?q=${message}`)
        getJournal()
    }

    setInterval(() => getJournal(), 5000)
    getJournal()
</script>