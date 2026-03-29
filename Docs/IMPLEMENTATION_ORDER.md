# Suggested first implementation order

1. Commit the manifest and bridge headers first.
2. Add the bridge service to the NovaForge editor-only build.
3. Add the C# project adapter into Arbiter's project adapter layer.
4. Test only read-style endpoints first:
   - `/project/info`
   - `/editor/selection`
5. Add build execution next.
6. Add tool execution only behind a whitelist and dry-run default.
