---
title: Add a custom property
---

## Problem

You need to create a custom property for ADR pages, and be able to:

- fill it in in the ADR document front matter,
- and see it in the sidebar.

As an illustration, let us add a custom property named `see-also` which may link to another ADR. 

## Describe the property

Create a new YAML file with the following content.

{% macro wrapped_include(path) %}{% include path %}{% endmacro %}

{% macro code_file(path, language, highlight_lines='') %}
!!! note "{{ path }}"
    ```{{ language }} {% if highlight_lines %}hl_lines="{{ highlight_lines }}"{% endif %}
    {{ wrapped_include(path=path)|indent }}
    ```
{% endmacro %}


{{ code_file(path='decisions/meta/see-also.yaml', language='yaml') }}

### Legend

- `$id` specifies the internal name of the property. You will use it in ADR pages frontmatter sections and elsewhere in code.
- `label` presents human readable name for the property.
- `symbol` is optional. Usually we use a Unicode icon there.
- `$type: adr:ADRProperty` is required - otherwise, the property won't be displayed in the sidebar.

## Are you going to use references?

If the values of the property are going to be references (IRIs, URLs), adjust your `context.yaml` to indicate that.

{{ code_file(path='decisions/context.yaml', language='yaml', highlight_lines='2-3') }}

## Use it, finally

{{ code_file(path='decisions/008-see-also.md', language='markdown', highlight_lines='7') }}

How does it look? That's how: {{ link('decisions/008-see-also.md') }}.
