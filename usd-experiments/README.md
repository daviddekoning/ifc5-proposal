# USD experiments

Each of the subfolders of this directory contains a number of USD
files that demonstrate how data from different layers (USD files) is
composed into a stage (federated model).

Since the purpose is to how how the composition process works, there is no
geometry in the files. Instead, properties and types are defined so that we
can tell if a value has been added or overwritten.

## Scenario 

The alignment examples describe the following situation:

1. An alignment has been published, including some station points. These
station points allow software that cannot compute alignments to position
items along an alignment. These stations would be written out by the
alignment design software.
2. At each of three stations, a wall is placed. The walls are typical walls,
that is they are defined in a library of components. Each typical wall has two windows,
and so it is itself made up of a typical wall with no windows, and two typical windows.
3. A more detailed model of the typical window is supplied in a separate layer.
4. One specific window (the first window in the second wall) is a higher
quality window.

## Patterns

### Coordination.usd

The top-level layer is called coordination.usd, and might be maintained by
a project BIM Coordinator. It serves the following purposes:

1. Defining the core of the shared model hierarchy for the project.
2. Defining what data (layers) should be included in the composed model.

### Marshalling

It may be desirable to disconnect the organization of model content with
its placement hierarchy. By default, USD maintains one model hierarchy for
both organization and scene placement. We can break this dependency by 
introducing a marshalling yard. All objects / Prims that will be placed in
a model / stage must be defined (as `class`) with a globally unique name in
the marshalling yard or Champ de Mars.

This allows overrides to be targetted at a Prim within the Champ de Mars by
referencing the globally unique name, and then the whole, marshalled Prim
can be moved around in the final stage hierarchy without requiring all 
contributing parties to update the paths of their overs.

In the marshalled-alignment example, the marshalling yard is called Champ_de_Mars.
The glazing.usd layer, which updates the glazing of one specific window
defines an over on the window in the Champ de Mars, prior to it being
placed at Station 2.

(I don't know if this is a good idea, I'm merely demonstrating that it is possible.)