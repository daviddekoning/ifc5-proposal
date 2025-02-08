# The Interoperability Cycle

2025-02-08
David de Koning

When discussing and evaluting decisions for IFC5, it is helpful to be clear about how data exists in the AECO world, and what areas IFC5 brings strengths to the table. This paper lays out:

1. The idea of the Interoperabilty Cycle, which includes 4 states a model can be in, 
2. Description of the 4 states of a building information model.
3. Some concrete workflow / use case examples
4. The difference between a parametric and an explicity catalogue.
5. Implications of using GUIDS and pathnames on the above
6. Recommendation for the short term to best allow experimentation.

## The Interoperability cycle

As model data flows from authoring software to a team context, it passes through these 4 states. This is the 'Interoperability cycle', with 4 **states** and 3 *transitions*:

**Parametric** model ➫ *Resolution* ➫ **Resolved** model ➫ *Export* ➫ **Explicit** Model ➫ *Composition* ➫ **Composed** Model

Data does flow in circles, but if we identify single sources of truth for each bit of project information, then each parametric model is resolved and exported into an ever growing river of data. What flows backwards are comments, suggestions, requests for revisions. The sources of truth are updated and flow back through the cycle.

#todo diagram that make the analogy to the water cycle?

## 4 states of a model

A building information model can exist in 4 states: Parametric, Resolved, Explicit and Composed.

These states generally exist in pairs:

- Within one BIM program: Parametric ➫ Resolved
- Within the project team: Explicit ➫ Composed

A **parametric** model is one that has objects defined by parameters associated with a generative function.

A **resolved** model is the result of calling all the gnerative functions on the parametric objects. This is often live-generated in an authoring tool.

An **explicit** model is one in which not generator functions are needed to get at the data. Explicit models are often snapshot exports of a resolved model.

A **composed** model is a combination of several explicit models into a single model. Model federation is a form of model composition. In general, composition allows multiple data sources to express different aspects of a single object, whereas federation does not allow sub-object information joining.

Tekla Structural, Revit, AllPlan, etc... are all parametric modellers and include logic to resolve the model geometry. IFC is mainly used as a standard for communicating explicit models. IFC 2/4 models can be federated, but cannot be composed in the general sense.

(as an aside, it seems that "Design Transfer View" refers to parametric models, whereas "Reference View: refers to explicit models. In this document, I am taking for granted that parametric models exist in specific BIM software, and explicit models are IFC5 models.)

## Model Hierarchy or Organization

### Parametric

In a parametric model, the fundamental structure is the parametric graph. As objects can have multiple parents (e.g. stairs or walls defined between multiple storeys). This graph is implicit and is rarely presented to the user.

The parametric objects can be organized into groups or into a hierarchy *independently of the parametric graph*. For example, you could place a luminaire in Level 2 for organizational purposes, but connect it's parametric inputs to Level 3, since it hangs at a fixed distance from the level above.

This organization of a model is completely optional. The use of GUIDs makes it possible to treat all the parametric objects as an unordered set: each object has a unique ID, and we can refer to it un ambiguously.

### Resolved

A resolved model has a natural aspect of organization: there is a clear parent-child relationship between the parametric object and whatever objects are generated during its resolution. There is a natural hierarchy between the parametric object and its resolved representation -- but this is a local relationship, disconnected from the organization or graph of the parametric objects.

When we discuss model organization, hierarchy and pathnames vs. GUIDs, it is helpful to distinguish between these two ideas. For example, we coudl say that all parametric objects are unstructured and identified by a GUID. We could then say that all objects generated during resolution are given a name prefixed by their parent parametric object's GUID. E.G. a stair object called `b7c2de` could generate a set of steps called `b7c2de.step1`, `b7c2de.step2` , etc...

What is critical is that the ID of parametric object (pathname or GUID), be consistent between the parametric and composed expressions of the model. #todo make link to use case.

## Workflow examples

### Coordination sketch

1. Andrew builds a parametric model in BIM software.
2. The model is resolved and geometry is shown - yay!
3. The resolved model is exported to ifcx, `model.ifcx` (v1). This is now an explicit representation of the model.
4. Barbara reviews the model and wants to tell Andrew to make some changes. To communicate what she wants unambiguously, she moves a column in her IFC5-aware editting software and exports an ifcx file that contains just the edits she has carried out, `edits.ifx`.
5. Andrew will review the result of composing Barbara's "edits" ifcx file. His editing software is able to compose the resolved data with the edits. Andrew updates his parametric model to match the geometry provided in `edits.ifcx`.
6. Once the paramters are updated, the model will be resolved. There is **no guarantee** that the resolved model will be identical to the composition of `model1.ifcx` (v1) and `edits.ifc`. The resolution rules are not know when the two ifcx files are composed, and there may be objects who's position depends on the column location in the parametric model, but were exported in global coordinates.

NB: For this workflow to be effective, ***object identies myst be stable across resolution, exporting and composition***. 

There are two ways to achieve this:
1. Place parametric objects in a hierarchy that is independent of the resolution process. E.G. even if a wall's geometry is defined relative to levels 0 and 4, it could be assigned to Level 1, or to a `Walls` collection for identification purposes. Changing the level it is defined relative to (e.g. L0+2300 mm ➫ L1-1500 mm) will not result in a renaming of the object.
2. Give all parametric objects unique names.

When we debate GUIDs vs pathnames, we are trying to solve the problem of unique and stable names across the interoperability cycle.

### Parametric models driven by an upstream explicit model

1. Sam Structural, the engineer, has a parametric model that resolved to an explict column, wall and slab geometry: `structure.ifcx`. 
2. Annie Architect references `structure.ifcx` and defines parametric finish objects that take the structural column faces as inputs.
3. Annie's parametric model is resolved and exported to `finishes.ifcx`.
4. `structure.ifcx` and `finishes.ifcx` can be composed into a full model.

NB:

1. There is no requirement that the finishes location in the composed model depend on the column location. They could both be stored in global coordinates.
2. This works best if the resolution of the structural model does not rename the faces of the columns every time the model is resolved. This can be achieved
    1. Objects generated by the resolution are given the same name every time (e.g. `face1`, `face2`, etc...) and are prefixed by the parametric objects's id (`column_id.face1`, `column_id.face2`,etc...). In this situation, the generator function needs to be written in a way that consistently gives the objects it creates the same id.
    2. Objects generated by resolution can be given their own GUIDs if the resolution algorithm remembers the GUIDs created the previous time, and re-assigns the same ids to the equivalent objects. This still requires the generator functions to be consistent in producing the objects so that the resolver can transfer the GUIDS.

The graph of relationships between parametric objects in the parametric model do not need to be exported to the explicit model. It is more important that all the objects generated during resolution have stable ids.

## Catalogues

Thinking about parametric vs explicit models also helps us think clearly about catalogues.

A parametric catalogue item is (e.g. a Revit family), in general, a set of parameters and a function that generates new objects based on those parameters.

Each parameter either:
1. affects or does not affect the resolution process
2. is a direct value or reference to another object in the model

When a parametric catalogue item is placed, a new object is created (an ID is assigned) and a reference to the catalogue item is stored. On resolution, new objects are created (by the generation function of the parametric catalogue item) and placed in the resolved model. Since we are creating new objets, it is trivial to assign new random ids.

Some catalogues used in a parametric model will have fixed geometry and properties (e.g. a chair or a desk). In this case, the generator function simply makes a copy, potentially assigning new ideas during the copy.

An explicit catalogue item is a set of parameters, without a generator function. It can be places into a model at a given location, but the object is not changed in any way.

Both parametric and explicit catalogues can be used in a parametric model, but only an explicit catalogue can be used in an explicit model.

### Exporting parametric catalogue items to the explicit model

An explicity model cannot include an object from a parametric library, so how should resolved catalogue items from a parametric model be exported to the explicit model?

Here are two options:

1. Split catalogue items into parametric and explicit parts. Create a catalogue of the explicit parts, so that the placed object / instance can inherit from it, and add explicity children or overs to store the resolved data.
2. Export the placed item as an explicit object, and store the name of the catalogue item as a classification. (e.g. `classification: my_revit_families, class: Wall_200`)

In a parametric model, the individual geometry exists on the instance, not the family, so why not just follow that logic?

Here is pseudo-ifcx for each option:

Option 1
```
class Wall_200:
    thickness: 200
    classifications: {IFC5.0: IfcWall, ACMECorpFamilies: Wall_200}

def MySolidWall inherits Wall_200:
    lower_level: L0
    lower_offset: -250
    upper_level: L7
    upper_offset: +675

    def geometry:
        mesh_data: ...
```

Option 2:

```
def MySolidWall
    thickness: 200
    classifications: {IFC5.0: IfcWall, ACMECorpFamilies: Wall_200}
    lower_level: L0
    lower_offset: -250
    upper_level: L7
    upper_offset: +675

    def geometry:
        mesh_data: ...
```

Note that both these files will be identical after composition, and anyone reading the file will look to the classification to determine the parent family.

### Explicit catalogues in resolution and composition

Explicit catalogues can be used in both resolution and composition.

In resolution, the parametric software will have a generic generation function that is used for every explicit catalogue item. When exporting to an explicit model, the explicit model can either export a copy of each item that is placed, or directly reference the explicit catalogue (provided that it is in a compatible format).

What about the IDs of objects included in the catalogue item? A resolution function can easily assign new ideas to each sub-object of the catalogue item. In composition, however, only the root object from the catalogue gets a new ID!!

Furthermore, if new IDs are assigned to sub-objects from a catalogue during resolution, the resolution function is responsible for their stability. This is feasible, but adds new complexity.

If however, sub-objects in an explicit catalogue item retain their name, and are simply pre-fixed by their parent's id, then it is trival for the resolution process and composition to give them the same name. This allows a parametric model to reference an explicit catalogue, and not have to include the catalogue data when it is exported.

If parametric modelling software does not support arbitrary ids and always assignes new GUIDS on resolution, there are a few options:

1. Export the explict model with each instance copied in place (as you would for parametrically generated objects).
2. Add a property to resolved objects (in the modelling software) with a stable id and use that to name the object during export.

## Recommendation

Thinking about the interoperability cycle use cases, including the use of catalogues, suggest that exploration is needed before settling on requiring every object in an IFC5 model to have a GUID, or making the unique ID of an object it's full path. To give us freedom to experiment and learn, I suggest the following:

1. Allow objects in an explicit model to have arbitrary IDs, including by not limited to GUIDs.
2. Allow nesting of objects within the explicit model.
3. Define the ID of an object as the list of parent object IDs.
4. Require all references to an object to us it's full ID (the full path).


## Appendix 1: Geometric context

The different types of model have a different relationship to geometric context.

**Parametric models**: the relationship between inputs of parametric objects the the objects the provide the input data form a directed (and hopefully) acyclic graph. This graph is generally rooted implicitly at the project origin. Resolution occurs relative to the project origin; it is assumed to lie at (0,0,0).

However, an object's relationship to the project origin is indirect. For any object, a subset of the parametric graph show what computations is needed to define it's geometry. In general, all the computations (which may be non-linear) must be carried out to determine where the object is.

**Resolved, Explicit, and Composed** models: objects in these models generally exist in a single cartesian space. If anything, objects may exist in a hierarchy of euclidian transforms, however, these are all linear, unlike the generator functions in a parametric model.
