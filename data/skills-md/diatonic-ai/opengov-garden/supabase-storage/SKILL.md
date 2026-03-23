---
name: supabase-storage
description: Manage objects and buckets in Supabase Storage. Triggered by phrases like "upload file to storage", "list storage objects", "delete bucket", or "moving storage files".
---

# Supabase Storage Skill

## Goal
Manage files and buckets within the Supabase Storage service.

## Instructions
1.  Open the relevant rule file:
    - `supabase storage cp` -> [.agent/rules/supabase/commands/storage/cp.md](../../rules/supabase/commands/storage/cp.md)
    - `supabase storage ls` -> [.agent/rules/supabase/commands/storage/ls.md](../../rules/supabase/commands/storage/ls.md)
    - `supabase storage mv` -> [.agent/rules/supabase/commands/storage/mv.md](../../rules/supabase/commands/storage/mv.md)
    - `supabase storage rm` -> [.agent/rules/supabase/commands/storage/rm.md](../../rules/supabase/commands/storage/rm.md)
2.  Use `storage ls` to explore existing buckets and files.
3.  Check [00_global_policy.md](../../rules/supabase/00_global_policy.md) before recursive deletions using `storage rm`.

## Examples
- "List files in the 'avatars' bucket" -> Use `supabase storage ls s3://avatars`
- "Upload a local image" -> Use `supabase storage cp local.png s3://bucket/remote.png`
- "Delete a file from storage" -> Use `supabase storage rm s3://bucket/file.ext`
