import { Session } from "@auth/core/types";

declare global {
  namespace App {
    interface Locals {
      auth(): Promise<Session | null>;
    }
    interface PageData {
      session: Session | null;
    }
    // interface Error {}
    // interface Platform {}
  }
}

export {};
