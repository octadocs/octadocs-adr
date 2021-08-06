---
title: Installation
---

## Install Python package

=== "pip"

    ```shell
    pip install octadocs-decisions
    ```

=== "poetry"

    ```shell
    poetry add octadocs-decisions
    ```

## Configure MkDocs

Add the following two plugins into your `mkdocs.yml` file:

```yaml
plugins:
  - octadocs
  - octadocs-decisions
  # ...
```

## Create a directory for ADRs

!!! warning "TODO"
    This needs to be automated with a CLI command.

Create a new directory named `decisions` underneath `docs` and a `context.yaml` file in that directory:

```shell
mkdir docs/decisions
echo '$import: named://decisions' > docs/decisions/context.yaml
```

This `context.yaml` file marks the created directory as the location for ADR documents.

## Create your first ADR

Create a new document in `decisions` directory named, say, `001-use-octadocs-decisions.md`:

```markdown
---
title: Use octadocs-decisions
number: 1
date: 2021-08-01
status: decisions:accepted
---

## Context

I am tired of managing ADR documents manually.

## Decision

Let us use `octadocs-decisions` for that.

## Consequences

I will get rid of manual work and will be 146% happier than before.
```

Open the `Decisions` chapter on your site and enjoy 🙂 
