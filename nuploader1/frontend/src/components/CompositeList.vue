<template>
    <section id="composites">

        <!-- 親ディレクトリの表示 -->
        <div v-if="current.parent" class="parent composite-wrapper" :key="current.parent.pk">
            <p class="composite" @click="move(current.parent)">{{ current.parent.name }}</p>
        </div>
        <div v-else-if="current.pk" class="parent composite-wrapper" :key="-1">
            <p class="composite" @click="moveTop">home</p>
        </div>

        <!-- カレントディレクトリの表示 -->
        <div v-if="current.pk" class="current composite-wrapper" :key="current.pk">
            <p class="composite">{{ current.name }}</p>
        </div>
        <div v-else class="current composite-wrapper" :key="-1">
            <p class="composite">home</p>
        </div>

        <!-- 子ファイル・ディレクトリの表示 -->
        <div class="child composite-wrapper" v-for="composite of current.composite_set" :key="composite.pk">
            <p class="composite" @click="move(composite)">{{ composite.name }}</p>
        </div>
    </section>
</template>

<script>
    export default {
        name: 'composite-list',
        data() {
            return {
                current: {},
            }
        },
        created() {
            this.getCompositeListTop()
        },
        methods: {
            getCompositeListTop() {
                this.$http(this.$endpoint)
                    .then(response => {
                        return response.json()
                    })
                    .then(data => {
                        this.current = {
                            composite_set: data
                        }
                    })
            },
            getCompositeListFromPk(pk) {
                this.$http(this.$endpoint + pk + '/')
                    .then(response => {
                        return response.json()
                    })
                    .then(data => {
                        this.current = data
                    })
            },

            move(composite) {
                this.getCompositeListFromPk(composite.pk)
            },
            moveTop() {
                this.getCompositeListTop()
            },

        },

    }
</script>

<style scoped>
    .composite-wrapper {
        margin-bottom: 50px;
    }
    .current {
        background-color: #eee;
        padding: 6px;
    }

    @media (min-width: 1024px) {
        #composites {
            padding-top: 120px;
        }
        .current > .composite {
            margin-left: 50px;
        }
        .child {
            margin-left: 100px;
        }
    }
</style>