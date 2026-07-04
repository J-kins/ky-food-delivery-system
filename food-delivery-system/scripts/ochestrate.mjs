import { exec, spawn } from 'child_process';
import { promisify } from 'util';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const execAsync = promisify(exec);
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const ROOT_DIR = path.resolve(__dirname, '..');

const isDev = process.argv.includes('--dev');
const isWatch = process.argv.includes('--watch');

const DOMAINS = ['public', 'admin', 'kitchen', 'manager', 'delivery'];

const COLORS = {
  reset: '\x1b[0m',
  bright: '\x1b[1m',
  dim: '\x1b[2m',
  red: '\x1b[31m',
  green: '\x1b[32m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
  magenta: '\x1b[35m',
  cyan: '\x1b[36m',
  white: '\x1b[37m',
};

const DOMAIN_COLORS = {
  public: COLORS.cyan,
  admin: COLORS.magenta,
  kitchen: COLORS.yellow,
  manager: COLORS.blue,
  delivery: COLORS.green,
};

function log(message, color = COLORS.white) {
  console.log(`${color}${message}${COLORS.reset}`);
}

function logDomain(domain, message, color = COLORS.white) {
  const domainColor = DOMAIN_COLORS[domain] || COLORS.white;
  console.log(`${domainColor}[${domain}]${COLORS.reset} ${message}`);
}

function logError(domain, message) {
  console.log(`${COLORS.red}[${domain}] ERROR:${COLORS.reset} ${message}`);
}

function logSuccess(domain, message) {
  console.log(`${COLORS.green}[${domain}]${COLORS.reset} ${message}`);
}

function logInfo(message) {
  console.log(`${COLORS.cyan}INFO:${COLORS.reset} ${message}`);
}

function logWarning(message) {
  console.log(`${COLORS.yellow}WARNING:${COLORS.reset} ${message}`);
}

function logSection(title) {
  const line = '='.repeat(60);
  console.log(`\n${COLORS.bright}${COLORS.cyan}${line}${COLORS.reset}`);
  console.log(`${COLORS.bright}${COLORS.white}  ${title}${COLORS.reset}`);
  console.log(`${COLORS.bright}${COLORS.cyan}${line}${COLORS.reset}\n`);
}

async function ensureDependencies(domain) {
  const domainPath = path.join(ROOT_DIR, 'domains', domain);
  const nodeModulesPath = path.join(domainPath, 'node_modules');
  
  if (!fs.existsSync(nodeModulesPath)) {
    logDomain(domain, 'Installing dependencies...', COLORS.yellow);
    try {
      await execAsync('npm install', { cwd: domainPath, stdio: 'inherit' });
      logSuccess(domain, 'Dependencies installed');
    } catch (error) {
      logError(domain, `Failed to install dependencies: ${error.message}`);
      throw error;
    }
  } else {
    logDomain(domain, 'Dependencies already installed', COLORS.dim);
  }
}

async function buildDomain(domain) {
  const domainPath = path.join(ROOT_DIR, 'domains', domain);
  
  logDomain(domain, 'Building...', COLORS.yellow);
  
  try {
    const command = isDev ? 'npm run dev' : 'npm run build';
    await execAsync(command, { cwd: domainPath, stdio: 'inherit' });
    logSuccess(domain, 'Build complete');
    return true;
  } catch (error) {
    logError(domain, `Build failed: ${error.message}`);
    return false;
  }
}

async function watchDomain(domain) {
  const domainPath = path.join(ROOT_DIR, 'domains', domain);
  
  logDomain(domain, 'Starting watch mode...', COLORS.yellow);
  
  return new Promise((resolve, reject) => {
    const child = spawn('npm', ['run', 'watch'], {
      cwd: domainPath,
      stdio: 'inherit',
      shell: true,
    });
    
    child.on('error', (error) => {
      logError(domain, `Watch failed: ${error.message}`);
      reject(error);
    });
    
    child.on('close', (code) => {
      if (code !== 0) {
        logError(domain, `Watch process exited with code ${code}`);
        reject(new Error(`Watch process exited with code ${code}`));
      } else {
        resolve();
      }
    });
    
    // Handle process termination
    process.on('SIGINT', () => {
      logDomain(domain, 'Stopping watch mode...', COLORS.yellow);
      child.kill('SIGINT');
    });
  });
}

async function serveDomain(domain) {
  const domainPath = path.join(ROOT_DIR, 'domains', domain);
  
  logDomain(domain, 'Starting dev server...', COLORS.yellow);
  
  return new Promise((resolve, reject) => {
    const child = spawn('npm', ['run', 'dev'], {
      cwd: domainPath,
      stdio: 'inherit',
      shell: true,
    });
    
    child.on('error', (error) => {
      logError(domain, `Dev server failed: ${error.message}`);
      reject(error);
    });
    
    child.on('close', (code) => {
      if (code !== 0) {
        logError(domain, `Dev server exited with code ${code}`);
        reject(new Error(`Dev server exited with code ${code}`));
      } else {
        resolve();
      }
    });
    
    // Handle process termination
    process.on('SIGINT', () => {
      logDomain(domain, 'Stopping dev server...', COLORS.yellow);
      child.kill('SIGINT');
    });
  });
}

async function buildAll(domains) {
  logSection(`Building all domains (${isDev ? 'Development' : 'Production'} mode)`);
  
  const results = [];
  
  for (const domain of domains) {
    logInfo(`Processing domain: ${domain}`);
    await ensureDependencies(domain);
    const success = await buildDomain(domain);
    results.push({ domain, success });
    console.log('');
  }
  
  // Summary
  logSection('Build Summary');
  const failed = results.filter(r => !r.success);
  
  results.forEach(({ domain, success }) => {
    if (success) {
      logSuccess(domain, 'Build successful');
    } else {
      logError(domain, 'Build failed');
    }
  });
  
  if (failed.length === 0) {
    log('\nAll domains built successfully!', COLORS.green);
    return true;
  } else {
    log(`\n${failed.length} domain(s) failed to build`, COLORS.red);
    return false;
  }
}

async function watchAll(domains) {
  logSection('Watching all domains for changes');
  
  logInfo('Press Ctrl+C to stop all watch processes');
  console.log('');
  
  const promises = domains.map(domain => 
    watchDomain(domain).catch(error => {
      logError(domain, `Watch failed: ${error.message}`);
    })
  );
  
  await Promise.all(promises);
}

async function serveAll(domains) {
  logSection('Starting all development servers');
  
  logInfo('Each domain will run on its own port:');
  logInfo('  public:    http://localhost:5173');
  logInfo('  admin:     http://localhost:5174');
  logInfo('  kitchen:   http://localhost:5175');
  logInfo('  manager:   http://localhost:5176');
  logInfo('  delivery:  http://localhost:5177');
  logInfo('');
  logInfo('Press Ctrl+C to stop all servers');
  console.log('');
  
  const promises = domains.map(domain => 
    serveDomain(domain).catch(error => {
      logError(domain, `Dev server failed: ${error.message}`);
    })
  );
  
  await Promise.all(promises);
}

async function serveDomainsParallel(domains) {
  logSection('Starting all development servers in parallel');
  
  logInfo('Each domain will run on its own port:');
  logInfo('  public:    http://localhost:5173');
  logInfo('  admin:     http://localhost:5174');
  logInfo('  kitchen:   http://localhost:5175');
  logInfo('  manager:   http://localhost:5176');
  logInfo('  delivery:  http://localhost:5177');
  logInfo('');
  logInfo('Press Ctrl+C to stop all servers');
  console.log('');
  
  // Install dependencies first
  for (const domain of domains) {
    await ensureDependencies(domain);
  }
  
  // Start all servers in parallel
  const processes = [];
  
  for (const domain of domains) {
    const domainPath = path.join(ROOT_DIR, 'domains', domain);
    
    const child = spawn('npm', ['run', 'dev'], {
      cwd: domainPath,
      stdio: 'inherit',
      shell: true,
      detached: false,
    });
    
    processes.push({ domain, child });
    logSuccess(domain, `Dev server started on port ${getPortForDomain(domain)}`);
  }
  
  // Handle process termination
  const cleanup = () => {
    logInfo('Stopping all dev servers...');
    processes.forEach(({ domain, child }) => {
      logDomain(domain, 'Stopping...', COLORS.yellow);
      child.kill('SIGINT');
    });
    process.exit(0);
  };
  
  process.on('SIGINT', cleanup);
  process.on('SIGTERM', cleanup);
  
  // Wait for all processes
  await Promise.all(processes.map(({ child }) => 
    new Promise((resolve) => {
      child.on('close', resolve);
    })
  ));
}

function getPortForDomain(domain) {
  const ports = {
    public: 5173,
    admin: 5174,
    kitchen: 5175,
    manager: 5176,
    delivery: 5177,
  };
  return ports[domain] || 5173;
}

function showHelp() {
  console.log(`
Usage: node scripts/orchestrate.mjs [options]

Options:
  --dev       Run in development mode (with dev servers)
  --watch     Run in watch mode (rebuild on changes, no servers)
  --help      Show this help message

Examples:
  node scripts/orchestrate.mjs           Build all domains (production)
  node scripts/orchestrate.mjs --dev     Start all dev servers
  node scripts/orchestrate.mjs --watch   Watch all domains for changes
  `);
}

// Parse arguments
const showHelpFlag = process.argv.includes('--help');

if (showHelpFlag) {
  showHelp();
  process.exit(0);
}

// Main execution
async function main() {
  try {
    if (isWatch) {
      await watchAll(DOMAINS);
    } else if (isDev) {
      await serveDomainsParallel(DOMAINS);
    } else {
      const success = await buildAll(DOMAINS);
      if (!success) {
        process.exit(1);
      }
    }
  } catch (error) {
    log(`Fatal error: ${error.message}`, COLORS.red);
    process.exit(1);
  }
}

main();