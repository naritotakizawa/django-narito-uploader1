<template>
    <div id="app">
        <header id="side">
            <router-link :to="{name:'home'}">
                <img src="@/assets/logo.svg" id="header-logo">
            </router-link>
        </header>
        <main id="main">
            <router-view/>
        </main>

    </div>
</template>

<script>
    export default {
        name: 'app',
    }
</script>

<style>
    * {
        margin: 0;
        padding: 0;
    }

    body {
        line-height: 1;
    }

    #header-logo {
        padding: 20px;
    }

    #main {
        padding: 20px;
    }

    #side {
        background-color: #eee;
    }

    #header-logo {
        width: 150px;
    }

    @media (min-width: 1024px) {
        #app {
            display: grid;
            grid-template-columns: 300px 1fr;
        }

        #side {
            grid-column: 1;
            position: fixed;
            top: 0;
            bottom: 0;
            width: 300px;
        }

        #main {
            grid-column: 2;
            padding: 20px;
        }
    }
</style>
