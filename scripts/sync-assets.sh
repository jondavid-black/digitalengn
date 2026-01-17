#!/bin/bash

# Get the root directory of the monorepo
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SHARED_ASSETS_DIR="$ROOT_DIR/shared-assets"

# Target projects and their public/static directories
# Format: "project_path:asset_dir"
TARGETS=(
    "digitalengn:static"
    "docsengn:static"
    "docs:public"
)

for target in "${TARGETS[@]}"; do
    IFS=":" read -r project_path asset_dir <<< "$target"
    FULL_TARGET_DIR="$ROOT_DIR/$project_path/$asset_dir/shared"
    
    echo "Syncing assets to $project_path..."
    
    # Ensure the parent asset directory exists
    mkdir -p "$ROOT_DIR/$project_path/$asset_dir"
    
    # Remove existing link or directory if it exists
    if [ -L "$FULL_TARGET_DIR" ]; then
        rm "$FULL_TARGET_DIR"
    elif [ -d "$FULL_TARGET_DIR" ]; then
        rm -rf "$FULL_TARGET_DIR"
    fi
    
    # Create symlink
    # Use relative path for the symlink to be more portable
    RELATIVE_PATH=$(realpath --relative-to="$ROOT_DIR/$project_path/$asset_dir" "$SHARED_ASSETS_DIR")
    ln -s "$RELATIVE_PATH" "$FULL_TARGET_DIR"
    
    echo "Created symlink: $FULL_TARGET_DIR -> $RELATIVE_PATH"
done

echo "Asset sync complete."
