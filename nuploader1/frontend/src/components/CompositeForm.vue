<template>
    <form @submit.prevent="remove" class="composite-form" v-if="selected.type==='delete'">
        <p>{{ selected.data.name }}の削除</p>
        <button type="submit">削除</button>
        <button @click="close" class="button-link">閉じる</button>
    </form>
    <form @submit.prevent="add" class="composite-form" v-else-if="selected.type==='new'">
        <p>新規作成</p>
        <input type="text" v-model="form.name" placeholder="名前">
        <div v-if="selected.data.is_dir">
            <input type="number" v-model="form.zip_depth" placeholder="ZIP階層">
        </div>
        <div v-else>
            <input type="file" ref="upfile">
        </div>
        <button type="submit">送信</button>
        <button @click="close" class="button-link">閉じる</button>
    </form>
    <form @submit.prevent="update" class="composite-form" v-else-if="selected.type==='update'">
        <p>{{ selected.data.name }}の更新</p>
        <input type="text" v-model="form.name" placeholder="名前">
        <input type="text" v-model="form.parent" placeholder="親ディレクトリID">
        <div v-if="selected.data.is_dir">
            <input type="number" v-model="form.zip_depth" placeholder="ZIP階層">
        </div>
        <div v-else>
            <input type="file" ref="upfile">
        </div>
        <button type="submit">更新</button>
        <button @click="close" class="button-link">閉じる</button>
    </form>
</template>

<script>
    export default {
        name: 'composite-form',
        props: {
            selected: {type: Object},
        },
        data() {
            return {
                form: {
                    name: '',
                    zip_depth: 0,
                    parent: '',
                }
            }
        },
        mounted() {
            if (this.selected.type === 'update') {
                this.form.name = this.selected.data.name
                this.form.zip_depth = this.selected.data.zip_depth
                this.form.parent = this.selected.data.parent ? this.selected.data.parent : ''
            }
        },
        methods: {
            add() {
                const formData = new FormData();
                formData.append('name', this.form.name);
                formData.append('is_dir', this.selected.data.is_dir);
                if (this.selected.data.is_dir) {
                    formData.append('zip_depth', this.form.zip_depth);
                } else {
                    const file = this.$refs.upfile.files[0]
                    if (file) {
                        formData.append('src', file);
                    }
                }
                if (this.selected.data.parent) {
                    formData.append('parent', this.selected.data.parent);
                }
                this.$http(this.$endpoint, {
                    credentials: "include",
                    method: 'POST',
                    body: formData,
                    headers: {
                        'X-CSRFToken': this.$csrfToken,
                    },
                }).then(response => {
                    if (response.ok) {
                        return response.json().then(() => {
                            this.$notify({
                                title: 'お知らせ',
                                message: this.$createElement('p', {style: 'color: #009'}, this.form.name + 'を追加しました'),
                                duration: 2000
                            })
                            this.$emit('done')
                        })
                    } else {
                        return response.json().then(data => {
                            this.$notify({
                                title: 'お知らせ',
                                message: this.$createElement('p', {style: 'color: #900'}, JSON.stringify(data)),
                                duration: 2000
                            })
                        })
                    }
                });
            },
            update() {
                const formData = new FormData();
                formData.append('name', this.form.name);
                formData.append('is_dir', this.selected.data.is_dir);
                if (this.selected.data.is_dir) {
                    formData.append('zip_depth', this.form.zip_depth);
                } else {
                    const file = this.$refs.upfile.files[0]
                    if (file) {
                        formData.append('src', file);
                    }
                }
                formData.append('parent', this.form.parent);
                this.$http(this.$endpoint + this.selected.data.pk + '/', {
                    credentials: "include",
                    method: 'PATCH',
                    body: formData,
                    headers: {
                        'X-CSRFToken': this.$csrfToken,
                    },
                }).then(response => {
                    if (response.ok) {
                        return response.json().then(() => {
                            this.$notify({
                                title: 'お知らせ',
                                message: this.$createElement('p', {style: 'color: #009'}, this.form.name + 'を更新しました'),
                                duration: 2000
                            })
                            this.$emit('done')
                        })
                    } else {
                        return response.json().then(data => {
                            this.$notify({
                                title: 'お知らせ',
                                message: this.$createElement('p', {style: 'color: #900'}, JSON.stringify(data)),
                                duration: 2000
                            })
                        })
                    }
                });
            },
            remove() {
                this.$http(this.$endpoint + this.selected.data.pk + '/', {
                    credentials: "include",
                    method: 'DELETE',
                    headers: {
                        'X-CSRFToken': this.$csrfToken,
                    },
                }).then(response => {
                    if (response.ok) {
                        this.$notify({
                            title: 'お知らせ',
                            message: this.$createElement('p', {style: 'color: #009'}, this.selected.data.name + 'を削除しました'),
                            duration: 2000
                        })
                        this.$emit('done')
                    } else {
                        return response.json().then(data => {
                            this.$notify({
                                title: 'お知らせ',
                                message: this.$createElement('p', {style: 'color: #900'}, JSON.stringify(data)),
                                duration: 2000
                            })
                        })
                    }
                });
            },

            close() {
                this.$emit('close')
            }
        }
    }
</script>


<style scoped>
    .composite-form {
        width: 300px;
    }

    .composite-form > * {
        margin-bottom: 1em;
    }

    .composite-form > p {
        font-size: 24px;
    }

    input[type=text], input[type=email], input[type=number],
    select, textarea {
        width: 100%;
        padding: 10px 10px;
        box-sizing: border-box;
        border-radius: 4px;
        border: solid 1px #ccc;
    }

    button, a.button {
        width: 100%;
        font-size: 14px;
        -webkit-appearance: none;
        padding: 10px 16px;
        border-radius: 4px;
        background-color: #0366d6;
        color: #fff;
        border: solid 1px #0366d6;
        vertical-align: bottom;
        box-sizing: border-box;
        display: inline-block;
        text-decoration: none;
        text-align: center;
        cursor: pointer;
    }

    button:hover, a.button:hover {
        opacity: 0.5;
    }

    .button-link {
        border: none;
        background: none;
        color: #000;
    }
</style>