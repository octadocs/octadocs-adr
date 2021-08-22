---
title: Add custom status value
position: 1
---

{% from "macros.html" import code_file %}

## Problem

You need to add a new status value, to complement the built in choices detailed at {{ link('local:usage/status.md') }} page. How to do that?

## Walkthrough

We will add a new status named `Archived`. In your `decisions` directory, add a new directory called `meta` and create a new file there, named `archived.yaml`. Its contents:

{{ code_file("decisions/meta/archived.yaml", language="yaml") }}

!!! Note
    The `symbol` part here is optional. You can skip it if you do not want to color your status tag with an emoji.

From now on, you can specify your ADR page is archived like this.

{{ code_file("decisions/004-archived.md", language="markdown", highlight_lines="6") }}

Preview: {{ link('decisions/004-archived.md') }}.
