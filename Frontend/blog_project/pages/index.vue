<template>
  <div class="row justify-content-md-center">
    <div class="col-lg-9 mb-5">
      <div class="row row-cols-1 row-cols-md-2 g-4">

        <div class="col">
          <div class="card-news">
            <!--Img of news-->
            <nuxt-link to="/"><img src="post.image.url" class="card-img-top" alt="post.title"></nuxt-link>
            <div class="mt-3">
              <!--Tags of news-->
              <p class="card-text">

                <nuxt-link to="/" class="text-decoration-none">
                  <button type="button" class="btn btn-sm btn-outline-light me-1">tag</button>
                </nuxt-link>

              </p>
              <!--Title and time of news-->
              <h2 class="card-title">
                <nuxt-link class="base-link" to="/">post.title</nuxt-link>
              </h2>
              <p class="card-text">post.created_at</p>
            </div>
          </div>
        </div>

      </div>
      <!-- {% include './include/pagination.html' with page_obj=page_obj %} -->
    </div>
    <Sidebar />
  </div>
</template>

<script>
import Sidebar from "~/components/Sidebar";

export default {}
</script>

<style>
</style>
