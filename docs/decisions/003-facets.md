---
title: Use the word "facet" the piece of code that builds a representation of a semantic network
number: 3
author: anatoly
date: 2021-08-07
status: accepted
---

## Context

As Zuckerberg says in his [interview about Metaverse](https://www.theverge.com/22588022/mark-zuckerberg-facebook-ceo-metaverse-interview), 

> People aren’t meant to navigate things in terms of a grid of apps.

That is true. In Octadocs and Iolanta, the content, expressed as a semantic graph, is primary. Every node of the graph may be represented somehow using a piece of code that will query the graph, retrieve all the information it needs about the node in question, and output something:

- A piece of static HTML, as in Octadocs;
- A live JavaScript visualization, or a WebGL 3D landscape, or a piece of text in CLI — if we're talking about iolanta.

## Decision

The word `app` which I originally used is too broad, and too overloaded. I believe we need a special word, and I couldn't come up with anything better than a `facet`.
