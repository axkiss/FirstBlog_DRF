<template>
    <nav class="navbar navbar-expand-lg fixed-top navbar-dark bg-dark  border-bottom border-secondary">

        <div class="container">

            <nuxt-link class="navbar-brand fs-4 text-light" to="/"><b>FIRST<span class="brand-color">BLOG</span></b>
            </nuxt-link>

            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarTogglerDemo02"
                aria-controls="navbarTogglerDemo02" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarTogglerDemo02">
                <ul class="navbar-nav mx-auto mb-2 mb-lg-0">

                    <li class="nav-item">
                        <nuxt-link class="base-link" to="/">ТЕГ</nuxt-link>
                    </li>


                    <li class="nav-item">
                        <nuxt-link class="base-link" to="/search">SEARCH</nuxt-link>
                    </li>
                    <li class="nav-item">
                        <nuxt-link class="base-link" to="/about">ABOUT US</nuxt-link>
                    </li>

                </ul>
                <ul class="nav navbar-nav">

                    <li class="nav-item">
                        <nuxt-link class="base-link" to="/login">Log in</nuxt-link>
                    </li>
                    <li class="nav-item">
                        <nuxt-link class="base-link" to="/register">
                            <button type="button" class="btn btn-outline-primary">Register
                            </button>
                        </nuxt-link>
                    </li>


                    <li class="nav-item dropdown">
                        <a class="base-link dropdown-toggle " to="#" id="navbarDropdown" role="button"
                            data-bs-toggle="dropdown" aria-expanded="false">
                        </a>
                        <ul class="dropdown-menu dropdown-menu-dark dropdown-menu-end" aria-labelledby="navbarDropdown">
                            <li><span class="dropdown-header fw-bold">Hi, user.get_short_name!</span></li>

                            <li>
                                <nuxt-link class="dropdown-item" to="/admin">Admin panel</nuxt-link>
                            </li>


                            <li>
                                <nuxt-link class="dropdown-item" to="/add_post">Add Post</nuxt-link>
                            </li>
                            <li>
                                <nuxt-link class="dropdown-item" to="/profile">Profile</nuxt-link>
                            </li>
                            <li>
                                <hr class="dropdown-divider">
                            </li>
                            <li>
                                <nuxt-link class="dropdown-item" to="/logout">Log out</nuxt-link>
                            </li>
                        </ul>
                    </li>

                </ul>
            </div>
        </div>
    </nav>
</template>