---
title: Plan the next actions
number: 9
author: anatoly
date: 2021-08-14
status: accepted
---

## Context

At this point, I am able to create custom properties and custom values for ADR pages. I need to plan what's going to be most critical to do next, and that depends on what is the most important to demonstrate on the conference.

### Things to do before the conference, aka Epics

- Provide user-friendly documentation on octadocs.io, adr.octadocs.io, and iolanta.tech sites
  Need a place where to link to.
  - Document what Octadocs is and provide some basic hints how to use it;
  - Document `iolanta` ontology;
  - Publish octadocs-adr docs at `adr.octadocs.io`.
- Export data from `octadocs-adr`
  Build `iolanta` command-line utility that can render those in JSON and CSV formats if you provide an IRI
- Create a new ADR document from CLI
  This is a necessary part of a good user experience. Copy-pasting Markdown files is not viable. Also requires the following:
  - Get `jeeves` plugin system reliable enough;
  - Implement `jeeves add adr` command;
  - Use SQLite database to store Octadocs graph;
  - Refactor the `.query()` function so that it is usable without `Octiron` class;
  - Update Octiron graph when a file was deleted;
  - Update Octiron graph when a `context.yaml` file was modified.
- Refactor `flake8.codes` to rely upon `iolanta` logic instead of ad-hoc macros.

## Decision

Among the items above, probably `jeeves add adr` command is the most important from the user experience point of view. I believe that the out-of-the-box usage of `octadocs-adr` suffers greatly from absence of such a command.

That command, in turn, requires a fast enough read access to the graph:
- it must find the directory where ADR pages are located,
- determine the max existing `number` of an ADR to avoid the need to input it manually,
- and it potentially can also determine the proper IRI of the ADR author.

To do that, we need to store the database in some format (probably SQLite is the best) on disk.

And that, in turn, means we need to properly manage the contents of the graph database file. Most notably, we need to be able to delete named graphs which corresopnd to files which no longer exist.

## Consequences

This will require a lot of changes to the `Octiron` class in Octadocs package. We will discuss those in the next ADR.
