# IFC5 Proposal

Author: David de Koning (Oasys Software, Arup)
Date: October 22, 2022

This document synthesizes the discussions in the buildingSMART Technical Room at the BSi Standards Summit in Montreal, October 17-20, 2022 into a proposal for how a new IFC standard could be structured.

## Building an addition or retrofitting new foundations?

Problems that we have with the current structure of IFC

1. Federation of data from multiple authors or publishers can only combine different objects. It is not possible for multiple authors or publishers to contribute data to a single object.
2. It is difficult for vendors, project delivery organizations or project teams to add custom data to objects and still maintain interoperability with exisitng tools.
3. Changes to the IFC standard require agreement across classifications, property names, types, prior to being used in project delivery.
4. IFC is completely incomprehensible to newcomers. (Seriously, I've tried to get my head around it for 5 years and still have no idea how to derive useful meaning from the standard as written)
5. IFC is strongly-typed and types are hierarchical.

## Layers of Standardization

We propose that a new IFC standard be broken down into three independent, layered standards.

1. Syntax Standard
	1. Property Sets / Components
	2. Data containers
2. Semantic Standard
	1. Component Definitions
	2. Classification Definitions
	3. Type Definitions
4. Operational Standard
	1. Versionning convention
	2. APIs for for real-time data provisioning

The syntax standard and the operational standard are domain-independent standards that provide a basis for transmitting information between parties. The syntax and operational standards will be driven by the technical room. The semantic standard is domain-dependent and its development will be driven across all the buildingSMART rooms.

### Syntax Standard

When we refer to syntax, we are refering to the type and organization that can be enforced by parsing. This document does not propose any specific data format or concrete syntax.

#### Components (aka Property Sets)

The fundamental unit of data in an IFC5-based openBIM system will be a property set. A property set is made up of three things:

1. The identifier of the entity or object to which the property set applies
2. A set of properties (key-value pairs)
3. An optional reference to a component or property set definition (the component type)

Components can be validated based on their syntax and based on their sematics. The syntax check confirms that it has three three items specified above. The sematantic check confirms that the properties meets the requirements of the property set definition (properties are named correctly, properties are present, values have the correct type, etc...). See below.

#### Data Containers

openBIM data will always be transfered in a data container. Data transfers include: saving data to a file, sending data in response to an REST API call, sending data in repsonse to a query, etc...

openBIM data containers are a set of components. Nothing more, nothing less. A container may contain:

1. A single component with a single property (One piece of information about one object)
2. A set of components (of the same type) that all refer to different entitities (a schedule)
3. A set of components of different types that all refer to a single entity (a 'full' description of an object)
4. A set of components of different types referring to many entities (The general case, where a full model is sent. There are many entitities, and lots of rich data about each one)

### Semantic Standard

#### Component Definitions

A component definition consists of:

1. A name (including namespaces)
2. A URI
3. A set of property definitions (name and type of value)

A component is a property set, and a component definition is a property set definition. This is the basis of semantic checks of components.

#### Classification Definitions

Fundamentally, a classification is simply an agreed name for something. When we assign a classification to an object, we are telling others "I intend for this object to represent such-and-such a thing in real life or in some system". Assigning a classification does not necessarily mean that we are promising to send any information about that thing. After all, Carl Linneaus, did not define property sets of data for each item in the biological classification we all know and love - he just assigned names.

To assign a classification to an entity, a `Classification` component will be defined that contains two properties:

1. A reference to a classification domain (or classification system)
2. A reference to a classification from the domain

Multiple classifications can be assigned to a given entity/object. Though particular software may limit the number of classifications that can be considered at one time, the federated nature of this proposal makes it impossible to limit the number of classifications assigned to a given entity.

A classification will be defined as they currently are in the bsdd, but without the classification properties (properties belong to property sets /  components, not classifications)

#### Types

A type is a definition or agreement about what data should be present on an entity. In IFC4 and before, a type definition was always directly associated with a classification. We may choose to retain this one to one relationship, but the approach outlined above does not impose this requirement. For example, we could define a set of types for different Level of Information Need / Levels of Detail / Project phases. Each set of types would define what data is needed for a given classification at a given level. LOD100.IfcWall, LOD200.IfcWall, etc...

A type definition will include:

1. A list of components that must be present for an entity to meet the type definition.

A type definition may optionally specify:

1. Specific values of certain properties in certain components. For example, a IfcWall type definition may require that there be a classification component that references both the IFC classification domain and the IfcWall classification.
2. More detailed validation rules (e.g. where-rules). It remains to be seen if these are still necessary. They may be. 🤷

Types are the basis of semantic validation of IFC entities.

### Operational Standard

The aim of this layer of the standard is to facilitate real-time data federation across software vendors. All vendors who adhere to this standard will be able to integrate with each other, and users of these platforms will be able to seamlessly work together to deliver projects.

#### Real-time Data provisioning API

This standard specifies three APIs: a data publishing API, a standard publishing API and a federated workspace API.

##### Data publishing API

The data publishing API is how an author shares their data with their collaborators. The publishing API will publish versioned data containers (see below for versioning convention). As a reminder, a data container is a set of components/property sets. To get all the available information about a particular entity/element/object, you will request all components related to that entity from all the publishers in your workspace, and collate the data together.

This will allow the following operations:

- request a particular version of a data container
- request the changes between two versions of a data container
- request a subset of a data container, via a query or filter
- request the changes between two versions of a subset data container, via a query or filter
- request the history of versions of a data container

##### Standard publishing API

The standard publishing API will make data from standards available in machine-readable format. It will publish classifications, property sets/components and types. The bSDD provides a similar API today.

##### Federated workspace API

The federated workspace API will provide a mechansim for multiple publishers to tell each other about what data containers they are publishing, and to coordinate permissions to access that data.

#### Versionning convention

Data containers will be versioned. Specific implementations may also track versions of components / property sets internally, but the API will only allow references to data container versions. This is consistent with historical practice in the AEC industry (drawings are versioned, not individual details or plan) and the software development industry (repositories of code are versioned, not individual files).

Three pieces of metadata will be associated with each version of a data container:
- the unique identifier of that version (e.g. a GUID or hash of the data in the container)
- the unique identifier of the previous version
- a list of human-readable labels that refer to this version (e.g. 'ISSUED FOR PERMIT', 'Latest Published', 'Latest WIP')

When requesting a particular version of a data container from the publishing API, the version can be specified by either a unique identifier or a label.

## Potential use cases

### Incremental standardization

The bulk of standard development will be concentrated in the Semantic Standard. By breaking down the semantic standard into three distinct pieces, we can accellerate standards development by agreement incrementally, rather than keeping all aspects open for discussion until a final agreement is reached.

Rooms may propose candidate standards of various different forms:

1. New classifications. New classifications can be added to the standard without defining any new properties or any new types. This simply serves as a means to agree on naming of things.
2. New property sets / components. A new collection of properties that would be beneficial for a given use case may be proposed independently of any classification.
3. New types. Once classifications and property sets are in place and agreed, new types can be proposed.

Obviously, candidate standards may include all three at once, but this is not necessary. If a group agrees on the naming of things, but has not yet reached concensus on what properties need to be attached, they can incorporate the classifications into the standard (which allows these to be incorporated into software tools) and then continue discussions on property sets and types.

### Live openBIM design and construction workflow

With the three APIs specified by the Operational Standard

### BIM to BAM workflows

There is a historical challenge in generating analysis models from a BIM (physical model). The heart of this challenge is that a physical model represents how a physical object occupies space, and an analysis model represents one aspect of it's behaviour (energy flow, displacement, etc...). Building an analysis model requires that decisions be made about

### The task of coordination in a federated workspace

Issues that a coordinator will need to resolve:

- data from two publishers is not in sync (e.g. cost data refers to an older version of the design)
- data from two publishers is contradictory (e.g. two publishers are publishing conflicting values of a component or parameter)
- the design doesn't work in real life (e.g. the classic task of architectural coordination)

## Ideas to continue thinking about
(note: *very draft*)
- Geometric placement hierarchy
	- components can be defined to refer to other entities to get their placement. E.G. a Hosted component/propertyset can refer to another entity that this entity is placed on
- Should data containers be allowed to define global data (e.g. a local axis or CRS that all data in the container refers to?)
	- this can be accomondated by an entity with a placementAxis or coordinate system component/propertyset, that each of the geometry components/property sets can refer to
- Geometry 
	- do we keep the current geometry language, or pick a whole new geometry language? There is probably a lot of good reasons to stay with what we have. In this structure, this discussion is limited to the definition of the Geometry component / propertyset, so the discussion might be simpler than it used to be.

## Summary

[TODO: write summary]

---
## Notes

### Transitioning IFC4.3 to this approach

One key reason that we are having this discussion today is that IFC is incredibly successful and the industry sees enormous value in it. The IFC4.3 standard contains the results of innumerable hours of discussion and negotiation. As we move forward, we must not toss the baby with the bathwater.

The content of the IFC 4.3 schema can be translated into the structure outlined in this document. The process will look something like this:

1. The classifications of IFC will be extracted into classification definitions, *without the classification properties*. This has already been done in the bsdd, you just need to ignore the `classificationProperties` data.
2. All properties defined by the IFC standard (the `classificationProperties` we ignored in step 1) will be organized into property sets / components. These will be organized by function / system / discipline, not by classification.
3. For each IFC type, a type will be defined by reference to its classification, the required components and the rules

[TODO: show a worked example]


### OO constraints that we don't care about

The power of object oriented programming paradigm is it's ability to combine the definition of both data and behaviour. The strict hierarchy and the difficulties related to multiple inheritance all relate to the behaviour, not the data. An object oriented system needs to be able to figure out which method definition to use when an object's method is called.

As IFC is a data standard and does not define any behaviour of an object, we are less constrained than an OO system and can direclty express a data hierarchy as a composition of data definitions.
