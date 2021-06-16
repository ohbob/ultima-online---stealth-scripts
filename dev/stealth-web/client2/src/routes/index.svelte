<script>

    import Header from '$lib/header.svelte'
    import Journal from '$lib/journal.svelte'
    import Log from '$lib/log.svelte'
    import Stats from '$lib/stats.svelte'

</script>


<section class="container mx-auto">
    <Header />
    <article class="grid sm:grid-cols-3 grid-cols-1">
        <Stats show="{true}"/>
        <Log show="{true}"/>
        <Journal show="{true}"/>
    </article>

</section>