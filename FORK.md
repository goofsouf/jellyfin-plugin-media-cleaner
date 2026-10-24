# Media Cleaner local fork

This fork adds controls to the Rules page for:

- starting the existing Jellyfin cleanup task immediately;
- running that task every 5 to 10080 minutes; or
- running it once daily at a time in the Jellyfin server's local timezone.

The controls call Jellyfin's administrator-only Scheduled Tasks API. A manual run uses the saved cleanup rules. The page refuses to start a run while rule edits are unsaved or legacy rules still need review. Scheduling replaces the cleanup task's existing trigger list. For weekly or multiple triggers, use **Advanced schedule** to open Jellyfin's full Scheduled Tasks editor.

## Build and package for Jellyfin 12.1

```sh
dotnet test MediaCleaner.Tests/MediaCleaner.Tests.csproj -c Release
dotnet build MediaCleaner/MediaCleaner.csproj -c Release -p:JellyfinProfile=12.1
python3 eng/package-local.py --profile 12.1
```

The ZIP is written to `dist/`. It contains both plugin DLLs, Jellyfin's `meta.json`, and the original MIT `LICENSE` notice. The plugin uses the upstream GUID, so it replaces Media Cleaner rather than installing beside it. Preserve the plugin configuration, back up the existing plugin directory, and install this ZIP as a manual Jellyfin plugin before restarting the server. Do not leave two versions of the same plugin in Jellyfin's plugin directory. Review the dry-run report before starting a cleanup.

## License and publishing

The upstream code is [MIT licensed](LICENSE). The license permits copying, modifying, publishing, and hosting this fork, including a public GitHub fork. Keep the copyright and permission notice in source distributions and packaged copies. This local repository retains the upstream notice and includes it in the ZIP.
