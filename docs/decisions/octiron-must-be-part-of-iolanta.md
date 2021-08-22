---
title: Octiron must be a part of Iolanta
number: 10
author: anatoly
date: 2021-08-14
status: accepted
---

## Context

### What is Octiron?

At this moment, `Octiron` is an existing Python class (plus a number of utilities coupled to it) in `octadocs` package that implements part of the core logic of the package. Its main purpose is to load Markdown, JSON-LD, and YAML-LD files from the `docs` directory (and other directories, plugin directories for example) into the RDFLib graph which will thereafter be queried for the data from those files. I will list its notable features a little later in this document.

### What is Iolanta?

`iolanta` currently also exists as a piece of Python code in `octadocs` package. Its most notable parts are:

- `iolanta.yaml` with a few terms defined, like `Facet` and `Environment`,
- and `iolanta.py` that exports `def render()` function.

The `render()` function accepts an Octiron instance *(thus, Iolanta currently depends on Octiron)*, the IRI to render, and IRI of the environment where to render it. This function will then search the graph for a pointer to an appropriate Facet. Then, it will try to execute the facet and return the result. The file also includes a few functions specific to facets implemented as Python callables.

### Why does Iolanta have its own name?

This functionality of `iolanta` is but an embryo. The tool is expected to evolve into a general purpose Linked Data browser which is capable of rendering pieces of Linked Data graphs using specific facets - specified explicitly or guessed by the system. Thus, it must make Linked Data available for manipulation by a person in a user friendly way.

`iolanta` will function in several ways:

- there will be a CLI app by that name;
- there will also be an HTTP server which you can run by calling `iolanta web`.

When you call `iolanta browse https://somewhere.net` the program does the following.

- Connect to the local RDFLib graph;
- Find the node you specified in the graph;
  - if found - try to find an appropriate facet;
  - if not found - try to load the information about that node.

How does the loading function?

- Determine the scheme of the URL provided;
- Find appropriate plugin that can fetch information from that kind of a URL;
- Call that plugin and receive from it a series of triples;
- Load those triples in the appropriate named graph inside the graph database.

After all of this is successfully executed we will go and try to find an appropriate `Facet` to visualize the data.

### Functionality Overlap

A lot of functionality in the data loading process of Iolanta is similar to what Octiron is doing.

<table>
  <thead>
    <tr>
      <th>Octiron feature</th>
      <th>Useful for Iolanta</th>
    </tr>
  </thead>

  <tbody>
    <tr>
      <td>Store a list of RDF prefixes</td>
      <td><strong>Yes</strong>: iolanta CLI must also support SPARQL queries and that will be very useful.</td>
    </tr>
    <tr>
      <td>Recognize directory-wise <code>context.yaml</code> files</td>
      <td><strong>Yes</strong>: those files can be used in GitHub repositories or IPFS directory structures with data.</td>
    </tr>
    <tr>
      <td>Determine which file has changed and which hadn't since last loading</td>
      <td><strong>Yes</strong>: since Iolanta relies heavily on local graph (which may be considered a cache), that cache must be time to time updated from the original sources. Iolanta must support that. For the sake of saving network traffic, it must intelligently recognize when each file was loaded and thus decide whether another file should be loaded again, or not yet.</td>
    </tr>
    <tr>
      <td>Load a file by request</td>
      <td><strong>Yes</strong>: that's what importing external Linked Data is all about.</td>
    </tr>
    <tr>
      <td>Support a plugin system</td>
      <td><strong>Yes</strong>: iolanta will not be useful without plugins for multiple Linked Data sources. For example, for loading data from <code>data.world</code>.</td>
    </tr>
    <tr>
      <td>Run OWL inference</td>
      <td><strong>Yes</strong>: running logical inference is definitely a required feature for Iolanta.</td>
    </tr>
    <tr>
      <td>User friendly SPARQL querying</td>
      <td><strong>Yes</strong>: that's what iolanta currently uses Octiron for. Built-in SPARQL querying in rdflib is not very user friendly, and Python facets use Octiron to do it in a less boilerplatey manner.</td>
    </tr>
  </tbody>
</table>

## Decision

Remembering that we have to do some refactoring on Octiron, we're going to do the following.

1. Create a separate `iolanta` package and make it a dependency of Octadocs;
2. Make Octiron a part of Iolanta class.

## Consequences

This will allow us to facilitate the development of `iolanta` project and avoid code duplication between `iolanta` and `octadocs`. 

We will postpone development of `ldflex` analog in Python, though. Let us keep our queries in raw SPARQL for now. The development of `pyldflex` may become a priority later and be advertised at the conference as a near-future project.
