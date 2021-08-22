---
title: Loaders vs Parsers
number: 11
author: anatoly
date: 2021-08-14
status: accepted
---

## Context

### What are loaders now?

At this moment, we have a number of classes in `octiron.plugins` package, named as follows:

- `YAMLLoader`
- `TurtleLoader`
- `MarkdownLoader`

They can read data from files (one of their arguments is `path`), apply context to it (`context` is another argument), and yield a stream of triples.

### Any problems with them?

Yes. In particular, YAML-LD loader:

- can only read data from a local path;
- currently cannot return the properties of the file and indicate into which graph to load the data because it outputs triples, not quads.

There is apparently no way to create a directory loader.

### Different protocols

We might want to load files not only from local disk but, say, from HTTPS endpoints or IPFS network. This is unachievable currently.

## Decision

Let us introduce two concepts.

- **Loader** will now be an interface to a certain protocol, say - local, HTTP, FTP, SFTP, or IPFS. Loaders are installable as plugins.
- **Parser** will now mean a certain data format. It will accept a file-like object to read from, plus any meta-data relevant, and it must output a stream of RDF quads. 

Thus, the job of a loader is to fetch something and to output it as a file-like byte stream plus optional meta data. Loader will also choose an appropriate parser and run it. Parser will output the stream of quads which then will be loaded into the graph.

## Consequences

This will make our architecture much more versatile.
