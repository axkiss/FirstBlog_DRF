<template>
  <!--Header (Navigation)-->
  <div>
    <header>
      <Navbar />
    </header>
    <main>

      <!-- {% block last-post %}{% endblock %} -->

      <section class="content">
        <div class="container">

            <Nuxt />


        </div>
      </section>

    </main>
    <Footer />
  </div>
</template>


<script>
import Navbar from "~/components/Navbar";
import Sidebar from "~/components/Sidebar";
import Footer from "~/components/Footer";


export default {
  components: {
    Navbar,
    Sidebar,
    Footer,
  }
};
</script>

<style>
</style>
