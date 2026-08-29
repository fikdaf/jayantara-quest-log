import { cp, mkdir, rm } from 'node:fs/promises';
import { execFileSync } from 'node:child_process';
import path from 'node:path';

const root = path.resolve(import.meta.dirname, '..', '..');
const webDist = path.join(root, 'apps', 'web', 'dist');
const dist = path.join(root, 'apps', 'desktop', 'dist');
await rm(dist, { recursive: true, force: true });
await mkdir(dist, { recursive: true });
execFileSync(process.platform === 'win32' ? 'npm.cmd' : 'npm', ['run', 'build'], { cwd: path.join(root, 'apps', 'web'), stdio: 'inherit' });
await cp(webDist, dist, { recursive: true });
console.log('Desktop web payload prepared');
