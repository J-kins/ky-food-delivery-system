import * as esbuild from 'esbuild';
import { copy } from 'esbuild-plugin-copy';
import { clean } from 'esbuild-plugin-clean';
import fs from 'fs';
import path from 'path';

// ============================================
// CONFIGURATION
// ============================================
const isDev = process.argv.includes('--dev');
const isWatch = process.argv.includes('--watch');

const DOMAIN = 'admin';
const SRC_DIR = 'src';
const DIST_DIR = 'dist';
const ENTRY_FILE = 'index.js';
const HTML_FILE = 'index.html';

// ============================================
// ESBUILD CONFIG
// ============================================
const buildConfig = {
  // Entry point
  entryPoints: {
    'bundle': ENTRY_FILE,
  },
  
  // Output
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
  
  // Platform/feature flags (injected at build time)
  define: {
    '__PLATFORM__': JSON.stringify(process.env.TARGET || 'tauri'),
    '__IS_TAURI__': JSON.stringify(process.env.TARGET === 'tauri'),
    '__IS_ANDROID__': JSON.stringify(process.env.TARGET === 'android'),
    '__IS_IOS__': JSON.stringify(process.env.TARGET === 'ios'),
    '__IS_WEB__': JSON.stringify(process.env.TARGET === 'web'),
    '__IS_MOBILE__': JSON.stringify(['android', 'ios'].includes(process.env.TARGET || '')),
    '__IS_DESKTOP__': JSON.stringify(process.env.TARGET === 'tauri'),
    '__ADMIN_MODE__': 'true',
    '__SHOW_FOOTER__': 'false',  // Admin never shows footer
    '__SHOW_NAVBAR__': 'true',
    '__SHOW_SIDEBAR__': 'true',  // Admin always has sidebar
    '__VERSION__': JSON.stringify(process.env.npm_package_version || '1.0.0'),
  },
  
  // External dependencies (if any)
  // external: ['react', 'react-dom'],  // Uncomment if using frameworks
  
  // Plugins
  plugins: [
    // Clean dist directory before build
    clean({
      patterns: [`./${DIST_DIR}/*`],
    }),
    
    // Copy HTML file to dist
    copy({
      resolveFrom: 'cwd',
      assets: {
        from: [`./${HTML_FILE}`],
        to: `./${DIST_DIR}`,
        keepStructure: true,
      },
      watch: isWatch,
    }),
    
    // Copy static assets (if any)
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
  
  // Loaders for static files
  loader: {
    '.png': 'file',
    '.jpg': 'file',
    '.svg': 'file',
    '.woff': 'file',
    '.woff2': 'file',
    '.ttf': 'file',
  },
};

// ============================================
// INJECT BUNDLE INTO HTML
// ============================================
function injectBundleIntoHtml() {
  const htmlPath = path.join(DIST_DIR, HTML_FILE);
  
  if (!fs.existsSync(htmlPath)) {
    console.warn(`${HTML_FILE} not found in ${DIST_DIR}`);
    return;
  }
  
  let html = fs.readFileSync(htmlPath, 'utf-8');
  
  // Remove any existing script tags that point to our bundle
  html = html.replace(/<script\s+src="\.\/bundle\.js"><\/script>/g, '');
  html = html.replace(/<script\s+src="\/dist\/admin\/bundle\.js"><\/script>/g, '');
  
  // Inject the new bundle script
  const injectScript = `<script type="module" src="./bundle.js"></script>`;
  html = html.replace('</body>', `${injectScript}</body>`);
  
  fs.writeFileSync(htmlPath, html);
  console.log(`Injected bundle into ${HTML_FILE}`);
}

// ============================================
// BUILD FUNCTION
// ============================================
async function build() {
  console.log(`Building ${DOMAIN} for ${process.env.TARGET || 'tauri'}...`);
  console.log(`Mode: ${isDev ? 'Development' : 'Production'}`);
  
  try {
    // Run esbuild
    await esbuild.build(buildConfig);
    
    // Inject bundle path into HTML
    injectBundleIntoHtml();
    
    console.log(`${DOMAIN} build complete!`);
    console.log(`Output: ${DIST_DIR}/`);
    
    // Print bundle size info
    const stats = fs.statSync(path.join(DIST_DIR, 'bundle.js'));
    console.log(`Bundle size: ${(stats.size / 1024).toFixed(2)} KB`);
    
    // Print chunk info if any
    const chunksDir = path.join(DIST_DIR, 'chunks');
    if (fs.existsSync(chunksDir)) {
      const chunks = fs.readdirSync(chunksDir);
      if (chunks.length > 0) {
        console.log(`Chunks: ${chunks.length} file(s)`);
      }
    }
    
  } catch (error) {
    console.error(`${DOMAIN} build failed:`, error);
    process.exit(1);
  }
}

// ============================================
// DEVELOPMENT SERVER
// ============================================
async function serve() {
  console.log(`⚡ Starting ${DOMAIN} dev server...`);
  
  try {
    // Build once before serving
    await build();
    
    // Create context for watch mode
    const ctx = await esbuild.context(buildConfig);
    
    // Enable watch
    await ctx.watch();
    
    // Start server
    const { host, port } = await ctx.serve({
      servedir: DIST_DIR,
      port: 5174,  // Different port from public (5173)
      host: 'localhost',
    });
    
    console.log(`${DOMAIN} dev server running at: http://${host}:${port}`);
    console.log(`Open: http://${host}:${port}/index.html`);
    console.log(`Watching for changes...`);
    console.log(`Domain: ${DOMAIN}`);
    console.log(`Platform: ${process.env.TARGET || 'tauri'}`);
    console.log('\nPress Ctrl+C to stop');
    
  } catch (error) {
    console.error(`${DOMAIN} dev server failed:`, error);
    process.exit(1);
  }
}

// ============================================
// WATCH MODE (without server)
// ============================================
async function watch() {
  console.log(`Watching ${DOMAIN} for changes...`);
  
  try {
    // Build once before watching
    await build();
    
    const ctx = await esbuild.context(buildConfig);
    await ctx.watch();
    
    console.log(`${DOMAIN} watch mode active. Press Ctrl+C to stop.`);
  } catch (error) {
    console.error(`${DOMAIN} watch failed:`, error);
    process.exit(1);
  }
}

// ============================================
// EXECUTION
// ============================================
if (isWatch) {
  await watch();
} else if (isDev) {
  await serve();
} else {
  await build();
}