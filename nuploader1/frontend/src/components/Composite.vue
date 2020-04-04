<template>
    <div class="composite">
        <img src="@/assets/dir.svg" v-if="data.is_dir" class="dir-icon">
        <img src="@/assets/file.svg" v-else class="file-icon">
        <span v-if="data.pk" class="id">{{ data.pk }}</span>
        <a class="composite-link" @click="onclick">{{ data.name }}</a>

        <template v-if="editableIn">
            <button type="button" @click="createFile" class="img-button add-dir">
                <img src="@/assets/add_file.svg" class="add-file-button-icon">
            </button>
            <button type="button" @click="createDir" class="img-button add-file">
                <img src="@/assets/add_dir.svg" class="add-dir-button-icon">
            </button>
        </template>
        <template v-if="editable">
            <button type="button" @click="update" class="img-button update">
                <img src="@/assets/update.svg" class="update-button-icon">
            </button>
            <button type="button" @click="remove" class="img-button delete">
                <img src="@/assets/delete.svg" class="delete-button-icon">
            </button>
            <a v-if="data.zip_depth" class="img-button zip" :href="zipUrl">
                <img src="@/assets/zip.svg" class="zip-button-icon">
            </a>
        </template>

    </div>
</template>

<script>
    export default {
        name: 'composite',
        props: {
            data: {type: Object},
            editable: {type: Boolean, default: false},
            editableIn: {type: Boolean, default: false},
            zipUrl: {type: String},
        },
        methods: {
            onclick() {
                this.$emit('click', this.data)
            },
            update() {
                this.$emit('update', this.data)
            },
            remove() {
                this.$emit('remove', this.data)
            },
            createFile() {
                this.$emit('createFile', this.data)
            },
            createDir() {
                this.$emit('createDir', this.data)
            }
        }

    }
</script>


<style scoped>
    .composite {
        font-size: 24px;
    }

    .composite-link {
        color: #0366d6;
    }

    .composite-link:hover {
        cursor: pointer;
        background-color: #eee;
    }

    .id {
        font-size: 16px;
        margin-right: 5px;
    }

    .dir-icon {
        width: 37px;
        margin-right: 10px;
        vertical-align: middle;
    }

    .file-icon {
        width: 24px;
        margin-right: 10px;
        vertical-align: middle;
    }

    .img-button {
        border: none;
        background: none;
        cursor: pointer;
        margin-right: 10px;
        vertical-align: middle;
        float: right;
    }

    .img-button:hover {
        opacity: 0.5;
    }

    .add-file-button-icon {
        width: 28px;
    }

    .add-dir-button-icon {
        width: 38px;
    }

    .update-button-icon {
        width: 33px;
    }

    .delete-button-icon {
        width: 28px;
    }

    .zip-button-icon {
        width: 37px;
    }
</style>
