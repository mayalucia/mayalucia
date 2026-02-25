#!/bin/bash
# Post-process ox-hugo exported markdown to fix LaTeX escaping.
# ox-hugo escapes underscores as \_ for Goldmark compatibility,
# but with Goldmark passthrough enabled, this breaks KaTeX rendering.
#
# Run after C-c C-e H A in Emacs:
#   cd website && bash fix-math-export.sh

for f in content/papers/*.md; do
    [ -f "$f" ] || continue
    # Only process files with math: true in front matter
    if head -20 "$f" | grep -q 'math = true'; then
        echo "Fixing math escapes in $f"
        sed -i 's/\\_/_/g' "$f"
    fi
done
