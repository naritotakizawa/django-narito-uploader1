<template>
    <section id="composites">
        <p v-for="composite of compositeList" :key="composite.pk">{{ composite.name }}</p>
    </section>
</template>

<script>
    export default {
        name: 'composite-list',
        data() {
            return {
                compositeList: {},
            }
        },
        created() {
            this.$http(this.$endpoint)
                .then(response => {
                    return response.json()
                })
                .then(data => {
                    this.compositeList = data
                })
        }
    }
</script>

<style scoped>

</style>