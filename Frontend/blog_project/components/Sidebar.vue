<template>
    <!--Sidebar block-->
    <div class="col-md-9 col-lg-3 mb-5">
        <!--Tags block -->
        <div class="card bg-secondary bg-opacity-10 border-secondary mb-4">
            <div class="card-header text-center fs-5 ">
                <b>Tags</b>
            </div>
            <div class="list-group">
                <p class="pt-2 text-center">

                    <nuxt-link to="/tag" class="text-decoration-none">
                        <button type="button" class="btn btn-sm btn-outline-light position-relative m-2">aside_tag
                            <span
                                class="position-absolute top-0 start-100 translate-middle badge rounded-pill bg-light text-dark">99</span>
                        </button>
                    </nuxt-link>

                </p>
            </div>
        </div>
        <!--Interesting news block-->
        <div class="card bg-secondary bg-opacity-10 border-secondary sticky-xl-top">
            <div class="card-header text-center fs-5">
                <b>Popular posts</b>
            </div>
            <div class="list-group">

                <nuxt-link to="/post" class="list-group-item bg-transparent base-link">
                    <div class="d-flex w-100 justify-content-between align-items-center">
                        <h6 class="mb-0 me-1">title</h6>
                        <img src="" width="64" height="64" alt="aside_post.title" class="rounded-2">
                    </div>
                </nuxt-link>

            </div>
        </div>
    </div>
</template>
<script>
export default {
    name: "Sidebar"
}
</script>

<style scoped>
</style>