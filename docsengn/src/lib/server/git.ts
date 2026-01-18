import simpleGit, { type SimpleGit } from 'simple-git';
import fs from 'fs/promises';
import path from 'path';

const DEFAULT_CONTENT_DIR = process.env.CONTENT_DIR || path.resolve('data/content');

export class GitService {
  private git: SimpleGit;
  private contentDir: string;

  constructor(contentDir: string = DEFAULT_CONTENT_DIR) {
    this.contentDir = contentDir;
    this.git = simpleGit(this.contentDir);
  }

  async init() {
    try {
      await fs.access(this.contentDir);
    } catch {
      await fs.mkdir(this.contentDir, { recursive: true });
    }

    const isRepo = await this.git.checkIsRepo();
    if (!isRepo) {
      await this.git.init();
      await this.git.addConfig('user.name', 'DocsEngn Bot');
      await this.git.addConfig('user.email', 'bot@docsengn.local');
    }
  }

  async listFiles(subpath: string = ''): Promise<{ name: string; type: 'file' | 'folder' }[]> {
    await this.init();
    
    // Validate path
    const safeSubpath = path.resolve(this.contentDir, subpath);
    if (!safeSubpath.startsWith(this.contentDir)) {
      throw new Error('Invalid path');
    }

    try {
      const entries = await fs.readdir(safeSubpath, { withFileTypes: true });
      return entries
        .filter(entry => !entry.name.startsWith('.git'))
        .map(entry => ({
          name: entry.name,
          type: entry.isDirectory() ? 'folder' : 'file'
        }));
    } catch (e) {
      if ((e as any).code === 'ENOENT') return [];
      throw e;
    }
  }

  async createFolder(folderPath: string, message: string): Promise<void> {
    await this.init();
    const safePath = path.resolve(this.contentDir, folderPath);
    if (!safePath.startsWith(this.contentDir)) {
      throw new Error('Invalid path');
    }

    await fs.mkdir(safePath, { recursive: true });
    // Create .gitkeep to ensure folder is tracked by git
    await fs.writeFile(path.join(safePath, '.gitkeep'), '', 'utf-8');
    await this.git.add(path.join(folderPath, '.gitkeep'));
    await this.git.commit(message || `Create folder ${folderPath}`);
  }

  async readFile(filename: string): Promise<string> {
    await this.init();
    const safePath = path.resolve(this.contentDir, filename);
    if (!safePath.startsWith(this.contentDir)) {
      throw new Error('Invalid path');
    }
    return fs.readFile(safePath, 'utf-8');
  }

  async saveFile(filename: string, content: string, message: string): Promise<void> {
    await this.init();
    const safePath = path.resolve(this.contentDir, filename);
    if (!safePath.startsWith(this.contentDir)) {
      throw new Error('Invalid path');
    }

    // Ensure directory exists
    await fs.mkdir(path.dirname(safePath), { recursive: true });

    await fs.writeFile(safePath, content, 'utf-8');
    await this.git.add(filename);
    await this.git.commit(message || `Update ${filename}`);
  }
}

export const gitService = new GitService();
