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

{% set sample_adr = "000-use-octadocs-adr.md" %}

Create a new document in `decisions` directory named, say, `{{ sample_adr }}`:

```markdown
{% include "decisions/" + sample_adr %}
```

Open {{ link('local:decisions/000-use-octadocs-adr.md') }} and see for yourself 😏 
