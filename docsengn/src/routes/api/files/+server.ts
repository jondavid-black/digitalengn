import { json } from "@sveltejs/kit";
import { gitService } from "$lib/server/git";

export async function GET({ url }) {
  const path = url.searchParams.get("path") || "";
  try {
    const files = await gitService.listFiles(path);
    return json(files);
  } catch (error) {
    console.error("Failed to list files:", error);
    return json({ error: "Failed to list files" }, { status: 500 });
  }
}

export async function POST({ request }) {
  try {
    const { path, message } = await request.json();
    if (!path) {
      return json({ error: "Path is required" }, { status: 400 });
    }
    await gitService.createFolder(path, message);
    return json({ success: true });
  } catch (error) {
    console.error("Failed to create folder:", error);
    return json({ error: "Failed to create folder" }, { status: 500 });
  }
}
