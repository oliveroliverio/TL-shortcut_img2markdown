# 250401
working

# 2025-04-04
## Added markdown formatting function for better copy-paste experience

**Files Changed:**
- `img2markdown.py`: Added new `prep_for_pasting()` function to format markdown output for better copy-paste experience
  - Converts first level headers (`# Heading`) to third level headers (`### Heading`)
  - Converts second level headers (`## Heading`) to bold text (`**Heading**`)
  - Removes triple backtick markdown designations
  - Modified `main()` function to use this new function when handling output

This change makes the clipboard output ready for direct pasting into existing markdown documents without requiring manual formatting adjustments.

# 2025-04-04
## Added unit test for prep_for_pasting function

**Files Changed:**
- `test_img2markdown.py`: Created new unit test file to verify the functionality of the `prep_for_pasting()` function
  - Test validates that the function correctly:
    - Converts first level headers to third level headers
    - Converts second level headers to bold text
    - Removes triple backtick markdown designations
  - Uses the example markdown provided as test input

The test ensures that the markdown formatting function works as expected with real-world content.