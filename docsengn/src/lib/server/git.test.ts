import { describe, it, expect, beforeEach, afterEach } from 'vitest';
import { GitService } from './git';
import fs from 'fs/promises';
import path from 'path';
import os from 'os';

describe('GitService', () => {
  let tempDir: string;
  let service: GitService;

  beforeEach(async () => {
    tempDir = await fs.mkdtemp(path.join(os.tmpdir(), 'docsengn-test-'));
    service = new GitService(tempDir);
  });

  afterEach(async () => {
    await fs.rm(tempDir, { recursive: true, force: true });
  });

  it('should initialize a git repo', async () => {
    await service.init();
    const gitDir = path.join(tempDir, '.git');
    const stats = await fs.stat(gitDir);
    expect(stats.isDirectory()).toBe(true);
  });

  it('should save and list files', async () => {
    await service.saveFile('test.md', '# Hello', 'Initial commit');
    const files = await service.listFiles();
    expect(files).toHaveLength(1);
    expect(files[0].name).toBe('test.md');
    
    const content = await service.readFile('test.md');
    expect(content).toBe('# Hello');
  });

  it('should create folders and save nested files', async () => {
    await service.createFolder('folder1', 'Create folder');
    const files = await service.listFiles();
    expect(files.find(f => f.name === 'folder1')?.type).toBe('folder');

    await service.saveFile('folder1/nested.md', '# Nested', 'Nested commit');
    const nestedFiles = await service.listFiles('folder1');
    expect(nestedFiles.find(f => f.name === 'nested.md')).toBeDefined();
    
    const content = await service.readFile('folder1/nested.md');
    expect(content).toBe('# Nested');
  });
});
