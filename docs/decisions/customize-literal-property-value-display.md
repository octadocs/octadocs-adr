---
title: Customize display of a property value if it is a literal
number: 7
author: anatoly
date: 2021-08-13
status: accepted
---

## Context

Suppose we have a `rating` property the value of which is a number from 1 to 5. How do we customize rendering it?

## Decision

We can't, not in current layout. Instead we should create an IRI for every possible value, and use it.

## Consequences

Perhaps a refactoring can help along the following lines: if property facet is customized then value facet is not rendered. But I do not see how to manage that, currently. 