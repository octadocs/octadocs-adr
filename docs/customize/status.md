---
title: Status values
---

> Suppose you need to add a new status value, to complement the built in choices detailed at [Status](/usage/status/) page. How to do that?

We will add a new status named `Archived`. In your `decisions` directory, add a new directory called `meta` and create a new file there, named `archived.yaml`. Its contents:

```yaml
{% include "decisions/meta/archived.yaml" %}
```

!!! Note
    The `symbol` part here is optional. You can skip it if you do not want to color your status tag with an emoji.

From now on, you can write:

```yaml
status: archived
```

on your ADR pages like this: {{ link('decisions/004-archived.md') }}.
