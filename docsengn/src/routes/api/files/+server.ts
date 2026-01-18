import { json } from '@sveltejs/kit';
import { gitService } from '$lib/server/git';

export async function GET() {
  try {
    const files = await gitService.listFiles();
    return json(files);
  } catch (error) {
    console.error('Failed to list files:', error);
    return json({ error: 'Failed to list files' }, { status: 500 });
  }
}
