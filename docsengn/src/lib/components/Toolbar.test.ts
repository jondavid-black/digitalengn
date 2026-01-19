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
    const headingBtn = getByTitle("Heading");
    expect(headingBtn).toBeTruthy();
    expect(queryByText("H1")).toBeNull();
    await fireEvent.click(headingBtn);
    expect(getByText("H1")).toBeTruthy();
    const h3Text = getByText("H3");
    await fireEvent.click(h3Text);
    let currentAction;
    editorAction.subscribe((v) => (currentAction = v))();
    expect(currentAction).toEqual({ type: "toggleHeading", payload: 3 });
  });

  it("should dispatch formatting actions", async () => {
    const { getByTitle } = render(Toolbar);

    const actions = [
      { title: "Bold", type: "toggleBold" },
      { title: "Italic", type: "toggleItalic" },
      { title: "Underline", type: "toggleUnderline" },
      { title: "Strike", type: "toggleStrike" },
      { title: "Code", type: "toggleCode" },
      { title: "Clear Marks", type: "unsetAllMarks" },
      { title: "Clear Nodes", type: "clearNodes" },
      { title: "Bullet List", type: "toggleBulletList" },
      { title: "Ordered List", type: "toggleOrderedList" },
      { title: "Code Block", type: "toggleCodeBlock" },
      { title: "Quote", type: "toggleBlockquote" },
      { title: "Horizontal Rule", type: "setHorizontalRule" },
      { title: "Hard Break", type: "setHardBreak" },
      { title: "Undo", type: "undo" },
      { title: "Redo", type: "redo" },
      { title: "Paragraph", type: "setParagraph" },
    ];

    for (const action of actions) {
      const btn = getByTitle(action.title);
      await fireEvent.click(btn);
      let currentAction;
      editorAction.subscribe((v) => (currentAction = v))();
      expect(currentAction).toEqual({ type: action.type, payload: undefined });
    }
  });

  it("should dispatch color action", async () => {
    const { getByTitle } = render(Toolbar);
    const btn = getByTitle("Purple");
    await fireEvent.click(btn);
    let currentAction;
    editorAction.subscribe((v) => (currentAction = v))();
    expect(currentAction).toEqual({ type: "setColor", payload: "#958DF1" });
  });
});
