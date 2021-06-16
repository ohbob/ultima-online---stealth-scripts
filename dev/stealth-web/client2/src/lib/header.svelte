<script>
    export let player = {'connected' : false}
     const calcPercentage = (a, b) => 100 - Math.abs((a - b) / a * 100.0)
        function getRand() {
        fetch("http://localhost:8000/player")
            .then(response => response.text())
            .then(response => player = JSON.parse(response))
    }
    getRand()
    setInterval(() => getRand(), 5000)
</script>
  <div class="bg-gray-300 p-1 flex justify-between">
 {#if player.connected}


            <span>
                <b>{player.name}</b>
                |
                {player.shardname}
<!--                |-->
                <!--{player.hp}-->
                <!--{player.stam}-->
                <!--{player.hp}-->
                <!--|-->
                <!--X:{player.X},-->
                <!--Y:{player.Y}-->

            </span>

             <div class="w-60">
                <div class="grid">
                    <div class="flex w-full h-2 bg-black">
                        <div class="h-2 bg-green-400" style="width: {calcPercentage(player.hp, player.maxhp)}%"></div>
                    </div>

                    <div class="flex w-full h-2 bg-black">
                        <div class="h-2 bg-red-400" style="width: {calcPercentage(player.stam, player.maxstam)}%"></div>
                    </div>



                    <div class="flex w-full h-2 bg-black">
                        <div class="h-2 bg-blue-400"
                             style="width: {calcPercentage(player.mana, player.maxmana)}%"></div>
                    </div>
                </div>
            </div>

      {:else}
        Connecting..

    {/if}
       </div>