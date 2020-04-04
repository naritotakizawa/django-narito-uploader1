<template>
    <section id="composites">

        <div id="list">
            <!-- 親ディレクトリの表示 -->
            <div v-if="current.parent" class="parent composite-wrapper" :key="current.parent.pk">
                <Composite :data="current.parent" @click="moveBefore"></Composite>
            </div>
            <div v-else-if="current.pk" class="parent composite-wrapper" :key="-1">
                <Composite :data="{name: 'home', is_dir: 'true'}" @click="moveBefore"></Composite>
            </div>

            <!-- カレントディレクトリの表示 -->
            <div v-if="current.pk" class="current composite-wrapper" :key="current.pk">
                <Composite :data="current" :editableIn="true" @createDir="createDir"
                           @createFile="createFile"></Composite>
            </div>
            <div v-else class="current composite-wrapper" :key="-1">
                <Composite :data="{name: 'home', is_dir: 'true'}" :editableIn="true" @createDir="createDir"
                           @createFile="createFile"></Composite>
            </div>

            <!-- 子ファイル・ディレクトリの表示 -->
            <div class="child composite-wrapper" v-for="composite of current.composite_set" :key="composite.pk">
                <Composite :data="composite"
                           @click="move" @remove="remove"
                           @update="update" :zipUrl="zipUrl(composite)" :editable="true"></Composite>

            </div>
        </div>

        <div id="form">
            <composite-form :selected="selected" @done="reload" @close="close"
                            :key="selected.type + '-' + selected.data.pk"></composite-form>
        </div>


    </section>
</template>

<script>
    import Composite from "./Composite.vue";
    import CompositeForm from "./CompositeForm"

    export default {
        name: 'composite-list',
        components: {
            Composite, CompositeForm
        },
        props: {
            path: {type: String},
        },
        data() {
            return {
                current: {},
                selected: {
                    type: null,
                    data: {}
                },
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
                    window.open(`http://127.0.0.1:8000/uploader${nextPath}`, '_blank')
                } else {
                    this.$router.push(nextPath)
                    this.getCompositeListFromPk(composite.pk)
                }
            },
            update(composite) {
                this.selected.data = composite
                this.selected.type = 'update'
            },
            remove(composite) {
                this.selected.data = composite
                this.selected.type = 'delete'
            },
            createFile(composite) {
                this.selected.data = {
                    is_dir: false,
                    parent: composite.pk ? composite.pk : '',
                }
                this.selected.type = 'new'
            },
            createDir(composite) {
                this.selected.data = {
                    is_dir: true,
                    parent: composite.pk ? composite.pk : '',
                }
                this.selected.type = 'new'
            },
            reload() {
                this.selected.type = null
                this.selected.data = {}
                if (this.current.pk) {
                    this.getCompositeListFromPk(this.current.pk)
                } else {
                    this.getCompositeListTop()
                }
            },
            zipUrl(composite) {
                return `http://127.0.0.1:8000/uploader/zip/${composite.pk}`
            },
           close() {
                this.selected.data = {}
                this.selected.type = null
            }
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

    #form {
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        background-color: rgba(255, 255, 255, 0.9);
        padding: 10px;
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

    @media (min-width: 1366px) {
        #composites {
            padding-top: 120px;
            display: grid;
            grid-template-columns: 700px 1fr;
        }

        #list {
            grid-column: 1;
        }

        #form {
            grid-column: 2;
            justify-self: center;
            margin-top: 100px;
            position: static;
            top: 0;
            left: 0;
            transform: none;
            background-color: transparent;
            padding: 0;
            box-shadow: none;
        }
    }
</style>