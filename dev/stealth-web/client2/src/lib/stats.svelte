<section class="bg-gray-100">
    <div on:click={toggle} class="bg-gray-100 p-1">
        {show ? "<" : ">"}
        Stats
    </div>

    {#if show && stats}
        <table class="text-sm mx-auto">
     <tr>
    <th>Name</th>
    <th>Amount</th>
  </tr>
        {#each Object.values(stats) as stat}
             <tr>
    <td>{stat.name}</td>
    <td>{stat.amount}</td>
  </tr>
        {/each}
            </table>



    {/if}

</section>

<script>
    let stats = {}
    export let show = true

    function toggle() {
        show = !show;
    }

    function getLog() {
        if (show) {
            fetch("http://localhost:8000/stats")
                .then(response => response.text())
                .then(response => stats = JSON.parse(response))
        }
    }

    setInterval(() => getLog(), 5000)
    getLog()
</script>

<style>
    th{
        text-align: left;
    }
    td{
        padding-right:10px;
    }
</style>