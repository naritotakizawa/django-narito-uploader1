<template>
    <section id="composites">

        <!-- 親ディレクトリの表示 -->
        <div v-if="current.parent" class="parent composite-wrapper" :key="current.parent.pk">
            <p class="composite" @click="moveBefore">{{ current.parent.name }}</p>
        </div>
        <div v-else-if="current.pk" class="parent composite-wrapper" :key="-1">
            <p class="composite" @click="moveBefore">home</p>
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
        props: {
            path: {type: String},
        },
        data() {
            return {
                current: {},
            }
        },
        created() {
            if (this.path) {
                this.getCompositeListFromPath(this.path)
            } else {
                this.getCompositeListTop()
            }
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
            getCompositeListFromPath(path) {
                this.$http(this.$endpoint + 'get_composite_from_path/' + path)
                    .then(response => {
                        return response.json()
                    })
                    .then(data => {
                        this.current = data
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
            getNextPath(composite) {
                let basePath = this.$route.path
                if (!basePath.endsWith('/')) {
                    basePath = basePath + '/'
                }

                let nextPath = basePath + composite.name
                if (composite.is_dir) {
                    nextPath = nextPath + '/'
                }
                return nextPath
            },
            getBeforePath() {
                const paths = []
                for (const path of this.$route.path.split('/')) {
                    if (path) {
                        paths.push(path)
                    }
                }
                paths.pop()
                return '/' + paths.join('/') + '/'
            },
            moveBefore() {
                const beforePath = this.getBeforePath()
                this.$router.push(beforePath)
                if (this.current.parent) {
                    this.getCompositeListFromPk(this.current.parent.pk)
                } else {
                    this.getCompositeListTop()
                }
            },
            move(composite) {
                const nextPath = this.getNextPath(composite)
                if (!composite.is_dir) {
                    window.open(nextPath, '_blank');
                } else {
                    this.$router.push(nextPath)
                    this.getCompositeListFromPk(composite.pk)
                }
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