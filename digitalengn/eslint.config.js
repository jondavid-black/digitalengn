import js from "@eslint/js";
import svelte from "eslint-plugin-svelte";
import prettier from "eslint-config-prettier";
import ts from "typescript-eslint";
import svelteParser from "svelte-eslint-parser";
import tsParser from "@typescript-eslint/parser";

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
    files: ["**/*.svelte"],
    languageOptions: {
      parser: svelteParser,
      parserOptions: {
        parser: tsParser,
        extraFileExtensions: [".svelte"],
      },
    },
  },
  {
    rules: {
      // Add custom rules here
    },
  },
);
