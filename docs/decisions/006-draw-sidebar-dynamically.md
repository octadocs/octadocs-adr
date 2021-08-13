---
title: Draw sidebar dynamically
number: 6
author: anatoly
date: 2021-08-13
status: accepted
---

## Context

At this point, we are trying desperately to visualize the contents of the side bar for ADR pages.

## Decision

### Sidebar environment

Use `adr:sidebar` environment to choose which facet to use for sidebar. The default facet will be bound as `hasDefaultFacet` to that environment.

Users can use `iolanta:facet` to install facets of their choice, to somehow customize the overall look and feel of the sidebar.

### Properties to print

The default facet will attempt to render every property of the page where the predicate part belongs to `adr:ADRProperty` class. If available, they will be sorted by `octa:position` property.

!!! note
    I do not see any other method to choose which properties to render, honestly. There might be many of them including primitive `rdf:type` and `owl:sameAs` declarations, and I do not want to invent ad-hoc conditions to exclude those.

### Environment for properties

`adr:sidebar-property` environment is specifically designated to render properties in the default sidebar facet. There is a default facet attached to that environment, which relies upon `rdfs:label`, `schema:url`, and perhaps `octa:symbol` to draw the property.

### Environment for property values

It might happen that property can function both as property itself and a value of another property. For that sake, we introduce another environment by the name of `adr:sidebar-property-value`. That also has its attached default rendering facet, which can render a few literal data types and relies upon `rdfs:label` for all other cases.

## Consequences

After having all the above written down, I myself can much better comprehend the construct to implement. The greatest use of ADRs is focusing and clearing your thought. That's why some people had developed a habit to write diaries. 
