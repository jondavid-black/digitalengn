import { json } from '@sveltejs/kit';
import { gitService } from '$lib/server/git';

export async function GET({ url }) {
  const filename = url.searchParams.get('filename');
  if (!filename) {
    return json({ error: 'Filename is required' }, { status: 400 });
  }

  try {
    const content = await gitService.readFile(filename);
    return json({ content });
  } catch (error) {
    console.error(`Failed to read file ${filename}:`, error);
    return json({ error: 'File not found or unreadable' }, { status: 404 });
  }
}

export async function POST({ request }) {
  try {
    const { filename, content, message } = await request.json();
    if (!filename || content === undefined) {
      return json({ error: 'Filename and content are required' }, { status: 400 });
    }

    await gitService.saveFile(filename, content, message);
    return json({ success: true });
  } catch (error) {
    console.error('Failed to save file:', error);
    return json({ error: 'Failed to save file' }, { status: 500 });
  }
}
