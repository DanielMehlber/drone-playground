---
type: module
module: playground
tags:
  - module
---

# Adding a technique

The set is meant to grow the way an encyclopedia grows. A new page exists because some module now depends on an idea that has no article.

1. Name the file exactly as you want the link to read. `[[Foo]]` looks for a note titled Foo.
2. Put shared background in `docs/concepts/`. Put a note that only one module cares about in that module's `docs/` folder.
3. Insert the template [[Technique]]. Keep the four sections: the problem, the background and the year, what it is for, and where this repo meets it.
4. Link the new page from the module that needed it, and add a line under the right heading in [[Concept index]].

A page that only says "see the module note" is too thin. A page that re-derives a textbook is too long. Aim for the length of a Wikipedia lead plus a short history.
