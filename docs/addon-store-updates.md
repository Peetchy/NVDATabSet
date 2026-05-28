# NVDA Add-on Store Updates

NVDA's built-in automatic add-on update checking is handled by the NVDA Add-on Store.

For NVDA TabSet to appear in NVDA's automatic add-on update checks, each release must be submitted to `nvaccess/addon-datastore` and accepted into the Add-on Store. GitHub Releases alone allow manual download, but they do not make NVDA automatically notify users about updates.

## Current Store Submission Data

- Add-on ID: `NVDATabSet`
- Version: `2026.5.1`
- Channel: `stable`
- Download URL: `https://github.com/Peetchy/NVDATabSet/releases/download/v2026.5.1/NVDATabSet-2026.5.1.nvda-addon`
- SHA256: `7A8E0E938AE90ECCE176AD806BF81D7E35BA33272870A1A0F4B71B1DB20D1633`
- Source URL: `https://github.com/Peetchy/NVDATabSet`
- License: `GPL v2`

The JSON metadata prepared for submission is in `docs/addon-store-submission/NVDATabSet-2026.5.1.json`.

## Submission Steps

1. Open `https://github.com/nvaccess/addon-datastore/issues/new/choose`.
2. Choose the add-on registration submission form.
3. Submit the add-on using the metadata from `docs/addon-store-submission/NVDATabSet-2026.5.1.json`.
4. Wait for NV Access approval and automated validation.
5. After acceptance, users can update from NVDA's Add-on Store update flow.

## User Update Flow After Store Acceptance

Users can check for add-on updates from NVDA's Add-on Store:

1. Open NVDA menu.
2. Open Tools.
3. Open Add-on Store.
4. Open the installed add-ons or update view.
5. Check for updates and install the available NVDA TabSet update.

If a user installed NVDA TabSet manually from a `.nvda-addon` file before it was accepted into the Add-on Store, NVDA may treat the installed add-on as external. In that case, the user should either reinstall NVDA TabSet from the Add-on Store or change the installed add-on's update channel to `stable` if NVDA offers that option.
