export function getInitials(name: string | null | undefined): string {
  if (typeof name !== "string" || name.length === 0) return "U";
  return name.charAt(0).toUpperCase();
}
