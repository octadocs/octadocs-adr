---
title: Keep octadocs-decisions docs separate from other octadocs related projects
number: 1
author: anatoly
date: 2021-08-01
status: decisions:accepted
---

## Context

At the moment of writing this document, I am working, at the same time, on several separate repositories specifically related to `octadocs`:

- [octadocs](https://github.com/octadocs/octadocs/)
- [octadocs-decisions](https://github.com/octadocs/octadocs-decisions/) *(this project)*
- [octadocs.github.io](https://github.com/octadocs/octadocs.github.io/)

At first, I wanted to document `octadocs-decisions` right along with Octadocs prime and with other blueprints at [octadocs.github.io](https://github.com/octadocs/octadocs.github.io/) but I have stumbled upon a few difficulties.

### Debugging

While working on this blueprint I have to debug it somehow, running it against real docs and interacting with the site in browser. The workflow is this:

- Make a change at `octadocs-decisions`,
- Restart a server which serves `octadocs.github.io`.

It wouldn't be a problem if I was using `octadocs-decisions` to house the docs that I use for testing the plugin.

## Decision

House `octadocs-decisions` docs right at `octadocs-decisions` repo.

## Consequences

- This will simplify my development process;
- This will make the docs more compact and readable for people who don't wish to dive deep into Octadocs prime;
- But this will also mean additional effort to integrate and interlink all of the Octadocs websites. We will worry about that later.
