import { render, fireEvent } from "@testing-library/svelte";
import { get, writable } from "svelte/store";
import { describe, it, expect, vi } from "vitest";
import Toolbar from "./Toolbar.svelte";
import { editorAction, drawerOpen, activeTab } from "$lib/stores";

// Mock stores
vi.mock("$lib/stores", () => {
  const { writable } = require("svelte/store");
  return {
    editorAction: writable(null),
    drawerOpen: writable(false),
    activeTab: writable({ type: "markdown", title: "test.md" }),
  };
});

describe("Toolbar", () => {
  it("should show heading dropdown and dispatch correct level", async () => {
    const { getByTitle, getByText, queryByText } = render(Toolbar);

    // Find Heading button
    const headingBtn = getByTitle("Heading");
    expect(headingBtn).toBeTruthy();

    // Dropdown should be closed initially
    expect(queryByText("H1")).toBeNull();

    // Open dropdown
    await fireEvent.click(headingBtn);

    // Check if dropdown options appear (H1 to H6)
    expect(getByText("H1")).toBeTruthy();
    expect(getByText("H6")).toBeTruthy();

    // Click H3
    // Note: getByText returns the span inside the button. We click it, event bubbles to button.
    const h3Text = getByText("H3");
    await fireEvent.click(h3Text);

    // Verify store update
    // We need to import the mocked store from the module to check its value
    // But since we mocked it, the import in this file refers to the mocked version?
    // Yes, vi.mock hoisting ensures that.

    // However, getting the value from the store requires subscribing or get()
    // Since we used 'writable' from svelte/store in the mock, it should behave like a real store.

    let currentAction;
    editorAction.subscribe((v) => (currentAction = v))();

    expect(currentAction).toEqual({ type: "toggleHeading", payload: 3 });
  });
});
