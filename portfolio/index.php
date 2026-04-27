<?php
/**
 * WordPress theme entry point.
 * Content lives in _body.html — edit that file, not this one.
 */
?>
<!DOCTYPE html>
<html <?php language_attributes(); ?>>
<head>
  <meta charset="<?php bloginfo('charset'); ?>" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>KD — Kshitiz Dange | Product Leader</title>
  <meta name="description" content="Kshitiz Dange (KD) — Product Leader specializing in Platform Products and HPC. Open to remote, Boston, and Bay Area opportunities." />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;500;700&family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet" />
  <?php wp_head(); ?>
</head>
<body <?php body_class(); ?>>
<?php include __DIR__ . '/_body.html'; ?>
  <?php wp_footer(); ?>
</body>
</html>
