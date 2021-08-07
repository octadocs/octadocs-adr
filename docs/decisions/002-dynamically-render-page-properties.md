---
title: Dynamically render page properties
number: 2
author: anatoly
date: 2021-08-06
status: decisions:accepted
---

## Context

At the moment of this writing, the number, behavior, and appearance of the document properties at the `octadocs-decisions` sidebar are hard-coded in the template — `adr.html`. That is acceptable for now and works for this particular document, but it cannot work forever. The semantic approach permits great ability to customize, and I would like to leverage that.

User might want to add a new property, say, `supersedes`, which they obviously want to be displayed at ADR pages. In particular, they want to customize:

- Order of properties in the sidebar;
- Name and appearance of the property label ("Superseded By", "Supersedes");
- Link and title of the target page, perhaps with special formatting, like this:

> **Superseded by:** `ADR015 ✔️` Buzinga

### How to format stuff?

Formatting must be done by arbitrary code. In this particular case, that would amount to `python://module.function` IRIs, which will prompt the app to call the function provided with specific arguments.

That function may call another function, or just directly render something and return a `str`.

## Decision

I am thinking about something along the following lines.

1. The `adr.html` template will call a function named, say, `decisions.properties(page)`;
2. That function will iterate over all properties of the page which satisfy certain criteria.
   * In particular, property must have an `app` attached to it;
   * that `app` must support https://octadocs.io/sidebar environment;
3. And then, the function will scrupulously call each of the apps found, providing as arguments:
   * `page` IRI itself,
   * and `property` IRI.
4. The property-bound app will then analyse what value the property has.
   - If that is a literal, the property-bound app will likely have to render it by itself;
   - Otherwise, it will try to find an app for that value, and call it.

### Defaults

There will be a SPARQL script that will assign default values of apps for properties.

## Consequences

Hopefully, this generic mechanism will be helpful for us and our users when we want to customize how our ADRs look.
