<section class="bg-gray-100">
    <div on:click={toggle} class="bg-gray-100 p-1">
        {show ? "<" : ">"}
        Log
    </div>
    {#if show}
        <ul style="height:400px; overflow:hidden; overflow-y:scroll;">
            {#each log.slice(-0) as entry}
                <li class="text-center text-sm p-1">{entry}</li>
            {/each}
        </ul>
    {/if}

</section>

<script>
    let log = []
    export let show = false

    function toggle() {
        show = !show;
    }

    function getLog() {
        if (show) {
            fetch("http://localhost:8000/log")
                .then(response => response.text())
                .then(response => log = JSON.parse(response))
        }
    }

    setInterval(() => getLog(), 5000)
    getLog()
</script>