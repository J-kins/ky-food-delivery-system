import * as esbuild from 'esbuild';
import { copy } from 'esbuild-plugin-copy';
import { clean } from 'esbuild-plugin-clean';
import fs from 'fs';
import path from 'path';

const isDev = process.argv.includes('--dev');
const isWatch = process.argv.includes('--watch');

const DOMAIN = 'delivery';
const DIST_DIR = 'dist';

// Multiple entry points and their corresponding HTML files
const ENTRIES = {
  'bundle': 'src/main.js',           // Main delivery dashboard
  'dispatcher-bundle': 'src/dispatcher.js', // Dispatcher view
  'rider-bundle': 'src/rider.js',    // Rider view
};

const HTML_FILES = {
  'index.html': 'index.html',         // Main dashboard
  'dispatcher.html': 'dispatcher.html', // Dispatcher view
  'rider.html': 'rider.html',         // Rider view
};

// Map HTML files to their corresponding bundle
const HTML_BUNDLE_MAP = {
  'index.html': 'bundle.js',
  'dispatcher.html': 'dispatcher-bundle.js',
  'rider.html': 'rider-bundle.js',
};

const buildConfig = {
  entryPoints: ENTRIES,
  
  outdir: DIST_DIR,
  bundle: true,
  minify: !isDev,
  sourcemap: isDev,
  target: ['es2020', 'chrome89', 'edge89', 'firefox89', 'safari15'],
  format: 'esm',
  splitting: true,
  chunkNames: 'chunks/[name]-[hash]',
  assetNames: 'assets/[name]-[hash]',
  legalComments: 'none',
  logLevel: 'info',
  
  define: {
    '__PLATFORM__': JSON.stringify(process.env.TARGET || 'tauri'),
    '__IS_TAURI__': JSON.stringify(process.env.TARGET === 'tauri'),
    '__IS_ANDROID__': JSON.stringify(process.env.TARGET === 'android'),
    '__IS_IOS__': JSON.stringify(process.env.TARGET === 'ios'),
    '__IS_WEB__': JSON.stringify(process.env.TARGET === 'web'),
    '__IS_MOBILE__': JSON.stringify(['android', 'ios'].includes(process.env.TARGET || '')),
    '__IS_DESKTOP__': JSON.stringify(process.env.TARGET === 'tauri'),
    '__DELIVERY_MODE__': 'true',
    '__SHOW_FOOTER__': 'false',
    '__SHOW_NAVBAR__': 'true',
    '__SHOW_SIDEBAR__': 'false',
    '__VERSION__': JSON.stringify(process.env.npm_package_version || '1.0.0'),
  },
  
  plugins: [
    clean({
      patterns: [`./${DIST_DIR}/*`],
    }),
    
    // Copy all HTML files
    copy({
      resolveFrom: 'cwd',
      assets: {
        from: Object.keys(HTML_FILES),
        to: `./${DIST_DIR}`,
        keepStructure: true,
      },
      watch: isWatch,
    }),
    
    // Copy static assets
    copy({
      resolveFrom: 'cwd',
      assets: {
        from: ['./assets/**/*'],
        to: `./${DIST_DIR}/assets`,
        keepStructure: true,
      },
      watch: isWatch,
    }),
  ],
  
  loader: {
    '.png': 'file',
    '.jpg': 'file',
    '.svg': 'file',
    '.woff': 'file',
    '.woff2': 'file',
    '.ttf': 'file',
  },
};

function injectBundlesIntoHtml() {
  console.log(`Injecting bundles into HTML files...`);
  
  Object.entries(HTML_BUNDLE_MAP).forEach(([htmlFile, bundleFile]) => {
    const htmlPath = path.join(DIST_DIR, htmlFile);
    
    if (!fs.existsSync(htmlPath)) {
      console.warn(`Warning: ${htmlFile} not found in ${DIST_DIR}`);
      return;
    }
    
    let html = fs.readFileSync(htmlPath, 'utf-8');
    
    // Remove any existing script tags that point to our bundles
    html = html.replace(/<script\s+src="\.\/.*bundle\.js"><\/script>/g, '');
    html = html.replace(/<script\s+src="\/dist\/delivery\/.*bundle\.js"><\/script>/g, '');
    
    // Inject the correct bundle for this HTML file
    const injectScript = `<script type="module" src="./${bundleFile}"></script>`;
    html = html.replace('</body>', `${injectScript}</body>`);
    
    fs.writeFileSync(htmlPath, html);
    console.log(`  Injected: ${bundleFile} -> ${htmlFile}`);
  });
  
  console.log(`Bundle injection complete`);
}

async function build() {
  console.log(`Building ${DOMAIN} for ${process.env.TARGET || 'tauri'}...`);
  console.log(`Mode: ${isDev ? 'Development' : 'Production'}`);
  console.log(`Entries: ${Object.keys(ENTRIES).join(', ')}`);
  
  try {
    await esbuild.build(buildConfig);
    injectBundlesIntoHtml();
    
    console.log(`${DOMAIN} build complete`);
    console.log(`Output: ${DIST_DIR}/`);
    
    // Print bundle sizes
    Object.keys(ENTRIES).forEach(entry => {
      const bundlePath = path.join(DIST_DIR, `${entry}.js`);
      if (fs.existsSync(bundlePath)) {
        const stats = fs.statSync(bundlePath);
        console.log(`  ${entry}.js: ${(stats.size / 1024).toFixed(2)} KB`);
      }
    });
    
  } catch (error) {
    console.error(`${DOMAIN} build failed:`, error);
    process.exit(1);
  }
}

async function serve() {
  console.log(`Starting ${DOMAIN} dev server...`);
  
  try {
    await build();
    
    const ctx = await esbuild.context(buildConfig);
    await ctx.watch();
    
    const { host, port } = await ctx.serve({
      servedir: DIST_DIR,
      port: 5177,
      host: 'localhost',
    });
    
    console.log(`${DOMAIN} dev server running at: http://${host}:${port}`);
    console.log(`Open: http://${host}:${port}/index.html (Dashboard)`);
    console.log(`Open: http://${host}:${port}/dispatcher.html (Dispatcher)`);
    console.log(`Open: http://${host}:${port}/rider.html (Rider)`);
    console.log(`Watching for changes...`);
    console.log(`Domain: ${DOMAIN}`);
    console.log(`Platform: ${process.env.TARGET || 'tauri'}`);
    console.log('Press Ctrl+C to stop');
    
  } catch (error) {
    console.error(`${DOMAIN} dev server failed:`, error);
    process.exit(1);
  }
}

async function watch() {
  console.log(`Watching ${DOMAIN} for changes...`);
  
  try {
    await build();
    
    const ctx = await esbuild.context(buildConfig);
    await ctx.watch();
    
    console.log(`${DOMAIN} watch mode active. Press Ctrl+C to stop.`);
  } catch (error) {
    console.error(`${DOMAIN} watch failed:`, error);
    process.exit(1);
  }
}

if (isWatch) {
  await watch();
} else if (isDev) {
  await serve();
} else {
  await build();
}