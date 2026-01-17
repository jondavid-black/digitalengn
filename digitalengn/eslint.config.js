import js from "@eslint/js";
import svelte from "eslint-plugin-svelte";
import prettier from "eslint-config-prettier";
import ts from "typescript-eslint";

export default ts.config(
  {
    ignores: [".svelte-kit/", "node_modules/", "dist/"],
  },
  js.configs.recommended,
  ...ts.configs.recommended,
  ...svelte.configs["flat/recommended"],
  prettier,
  ...svelte.configs["flat/prettier"],
  {
    rules: {
      // Add custom rules here
    },
  },
);
