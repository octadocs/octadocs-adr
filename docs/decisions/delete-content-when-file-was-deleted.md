---
title: Delete content when underlying file was deleted
number: 11
author: anatoly
date: 2021-08-14
status: accepted
---

## Context

Right now, the method of `Octiron` class called `update_from_file` is executed for every file in MkDocs directory by the means of `on_files` event. This allows to update the graph from every file that MkDocs knows about, but it does not help removing the files which are no longer there.

## Decision

- Submit path to `docs` directory to `update_from_file()`. 
- Support path to a directory as an argument to `update_from_file()`.
- Create an Octiron **plugin** (loader? extractor? importer? oracle? interface? connector?) which will be called if a directory is provided as an argument.
- That plugin should scan the directory and the tree of files represented in graph. It should check files' modification dates and existence. It will delete files which do not anymore exist and update those which still do.
- Rename `update_from_file()` to `add()`.

## Consequences

This will pave a way to finally store the graph in an SQLite db instead of in memory.
