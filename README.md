# WorkMw Vacancy Generator - Android app

Your HTML app (`www/index.html`) wrapped as a native Android app with Capacitor.
GitHub builds the APK for you - nothing needs installing on your computer.

## Get the APK
1. Create a new repository on GitHub (private is fine) and upload everything in this folder
   (including the hidden `.github` folder).
2. Open the **Actions** tab. The "Build Android APK" workflow runs on every push (about 5-8 minutes).
   You can also start it with **Run workflow**.
3. When it is green, open the **Releases** page (right side of the repo) and download
   `WorkMw-Generator-v1.0.N.apk`, or download it from the run's **Artifacts**.
4. Send the APK to the phone, open it, and allow "Install unknown apps" when asked.

## Updating the app
Edit `www/index.html` on GitHub and commit. A new APK is built automatically.
Every build signs with the same key, so the new APK installs over the old one and keeps saved data.

## What changed in the HTML for Android
- Poster and CSV downloads open the Android share sheet (save to Files, Gallery, WhatsApp, Facebook...).
  "Download all" shares every poster in one go.
- Plus Jakarta Sans is bundled, so posters render correctly offline.
- Claude-only features (cloud sync, AI auto-fill) fall back to the app's own parser and on-device storage.

## Optional: Play Store / your own signing key
Create a keystore once (`keytool -genkeypair -v -keystore release.keystore -alias workmw -keyalg RSA -keysize 2048 -validity 10000`),
then add these repository secrets (Settings > Secrets and variables > Actions):
`KEYSTORE_BASE64` (output of `base64 -w0 release.keystore`), `KEYSTORE_PASSWORD`, `KEY_ALIAS`, `KEY_PASSWORD`.
The workflow then also produces a signed `.aab` for the Play Store.
Keep the keystore safe: Google Play requires the same key for every update.
Note: switching from the default key to your own means uninstalling the old app once.

## Details
- App id: `com.hcconsultants.workmw` (change in `capacitor.config.json` AND `android/app/build.gradle` before first publishing)
- Min Android 7.0 (API 24), target API 36, Capacitor 8, Node 22, JDK 21
- Icons and splash come from `assets/`; regenerate with `npx capacitor-assets generate --android --assetPath assets`
