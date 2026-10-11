# v2.2 Fixes

This version addresses the two browser scenarios reported as failing:

1. **Update product — Boolean payload:** Create and Update now serialize the Available dropdown as a JSON Boolean (`true`/`false`) rather than a string. The API model intentionally validates that field as a Boolean.
2. **List all products — Clear/Search:** Clear now resets Category as well as the other form fields. Search ignores an empty/null Available selection, so a cleared form requests the full catalog instead of accidentally filtering by `available=null` or the default `UNKNOWN` category.

## Verification

- JavaScript syntax checked with Node.js.
- Python source syntax checked with `py_compile`.
- The uploaded environment's log showed 44 passing pytest tests before these changes. I could not rerun the Python/Behave suite in this build environment because the required Python packages are not installed and package installation is unavailable here. Run the commands in the README on your Windows development environment to verify end-to-end behavior.
