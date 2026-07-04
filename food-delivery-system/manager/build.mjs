import * as esbuild from 'esbuild';
import { copy } from 'esbuild-plugin-copy';
import { clean } from 'esbuild-plugin-clean';
import fs from 'fs';
import path from 'path';

const isDev = process.argv.includes('--dev');
const isWatch = process.argv.includes('--watch');

const DOMAIN = 'manager';
const DIST_DIR = 'dist';
const ENTRY_FILE = 'src/main.js';
const HTML_FILE = 'index.html';

const buildConfig = {
  entryPoints: {
    'bundle': ENTRY_FILE,
  },
  
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
    '__MANAGER_MODE__': 'true',
    '__SHOW_FOOTER__': 'false',
    '__SHOW_NAVBAR__': 'true',
    '__SHOW_SIDEBAR__': 'true',
    '__VERSION__': JSON.stringify(process.env.npm_package_version || '1.0.0'),
  },
  
  plugins: [
    clean({
      patterns: [`./${DIST_DIR}/*`],
    }),
    
    copy({
      resolveFrom: 'cwd',
      assets: {
        from: [`./${HTML_FILE}`],
        to: `./${DIST_DIR}`,
        keepStructure: true,
      },
      watch: isWatch,
    }),
    
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

function injectBundleIntoHtml() {
  const htmlPath = path.join(DIST_DIR, HTML_FILE);
  
  if (!fs.existsSync(htmlPath)) {
    console.warn(`Warning: ${HTML_FILE} not found in ${DIST_DIR}`);
    return;
  }
  
  let html = fs.readFileSync(htmlPath, 'utf-8');
  
  html = html.replace(/<script\s+src="\.\/bundle\.js"><\/script>/g, '');
  html = html.replace(/<script\s+src="\/dist\/manager\/bundle\.js"><\/script>/g, '');
  
  const injectScript = `<script type="module" src="./bundle.js"></script>`;
  html = html.replace('</body>', `${injectScript}</body>`);
  
  fs.writeFileSync(htmlPath, html);
  console.log(`Injected bundle into ${HTML_FILE}`);
}

async function build() {
  console.log(`Building ${DOMAIN} for ${process.env.TARGET || 'tauri'}...`);
  console.log(`Mode: ${isDev ? 'Development' : 'Production'}`);
  
  try {
    await esbuild.build(buildConfig);
    injectBundleIntoHtml();
    console.log(`${DOMAIN} build complete`);
    console.log(`Output: ${DIST_DIR}/`);
    
    const stats = fs.statSync(path.join(DIST_DIR, 'bundle.js'));
    console.log(`Bundle size: ${(stats.size / 1024).toFixed(2)} KB`);
    
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
      port: 5176,
      host: 'localhost',
    });
    
    console.log(`${DOMAIN} dev server running at: http://${host}:${port}`);
    console.log(`Open: http://${host}:${port}/index.html`);
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