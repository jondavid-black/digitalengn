import { describe, it, expect } from "vitest";
import { getInitials } from "./utils";

describe("getInitials", () => {
  it("should return the first letter of the name", () => {
    expect(getInitials("Digital User")).toBe("D");
  });

  it("should return U if name is null", () => {
    expect(getInitials(null)).toBe("U");
  });

  it("should return U if name is undefined", () => {
    expect(getInitials(undefined)).toBe("U");
  });

  it("should return U if name is empty", () => {
    expect(getInitials("")).toBe("U");
  });
});
