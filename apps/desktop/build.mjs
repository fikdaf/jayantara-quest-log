import { cp, mkdir, rm } from 'node:fs/promises';
import { execFileSync } from 'node:child_process';
import path from 'node:path';

const root = path.resolve(import.meta.dirname, '..', '..');
const webDir = path.join(root, 'apps', 'web');
const webDist = path.join(webDir, 'dist');
const dist = path.join(root, 'apps', 'desktop', 'dist');

await rm(dist, { recursive: true, force: true });
await mkdir(dist, { recursive: true });

const npm = process.platform === 'win32' ? process.env.ComSpec : 'npm';
const args = process.platform === 'win32'
  ? ['/d', '/s', '/c', 'npm run build']
  : ['run', 'build'];

execFileSync(npm, args, { cwd: webDir, stdio: 'inherit', windowsHide: true });
await cp(webDist, dist, { recursive: true });
console.log('Desktop web payload prepared');
