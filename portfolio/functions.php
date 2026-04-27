<?php
/**
 * Theme functions — only relevant when deployed to WordPress.com Business plan.
 * For GitHub Pages / Netlify deployments, this file is ignored.
 */

function kd_portfolio_enqueue_assets() {
    wp_enqueue_style(
        'kd-portfolio-style',
        get_stylesheet_uri(),
        [],
        '1.0.0'
    );
    wp_enqueue_script(
        'kd-portfolio-script',
        get_template_directory_uri() . '/script.js',
        [],
        '1.0.0',
        true  // load in footer
    );
}
add_action('wp_enqueue_scripts', 'kd_portfolio_enqueue_assets');

// Hide WP admin bar so it doesn't overlap the fixed nav
add_filter('show_admin_bar', '__return_false');
