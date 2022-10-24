# Reframing IfcWall in the IFC5 proposal

Author: David de Koning (Oasys Software, Arup)

Date: October 24, 2022

To illustrate how an existing defintion might be reframed into this IFC5 proposal, let us consider the [IfcWall Instance Diagram](https://standards.buildingsmart.org/MVD/RELEASE/IFC4/ADD2_TC1/RV1_2/HTML/).

To reframe IfcWall as an IFC5 defintion, we will need three things:

- a classification defintion
- a set of components to hold the information associated with the wall
- a type definition

For this example we will retain the classification defined in IFC4.3, but rename the standard to IFC5.0-proposed. The (fake) URI for this classification is `https://identifier.buildingsmart.org/uri/buildingsmart/ifc-5.0-proposed/class/IfcWall`.

In the sections below, we will

## Special Cases

- *GlobalId*: this is replaced by the entity ID, which is a specific field on a component / property set.

**Classification**: since entities are no longer classified by the hierarchy defined in the standard, we will introduce a classification component / property set. It will contain one required property:

- ClassificationDefinition: a URI refering the to classification definition. (`https://identifier.buildingsmart.org/uri/buildingsmart/ifc-5.0-proposed/class/IfcWall` in this case)

Data from the classification definition may optionally be tagged to the component.

## Components

The data defined on *IfcWall* will be captured by components. **Names in bold** are new components, and *names in italics* are properties defined in IFC4.3. The properties are addressed below in the hierarchical order of their definition in IFC4.3, however, this does not imply any hierarchy between the components / property sets.

The following components will be defined:

- IfcCommon
- Nesting
- Composition
- Type
- Geometry
- StructureHierarchy


### IfcRoot properties

**IfcCommon**:
- *Name*
- *Description*
- *Tag* (seems like this could be a common element across all IFC5 entities)

- ~~*OwnerHistory*~~:  history, versioning and ownership have nothing to do with syntax or semantics. These concepts will be addressed in the operational / federation standard, and are not stored within an IFC5 data container.

### IfcObjectDefintion

- ~~*HasAssignements*~~: This appears to be a generic mechansim for linking property sets to objects, and is thus replaced by the component mechanism.
- ~~*HasAssociations*~~: replaced by type and classification components / property sets.

**Nesting**: (this could be a singled component, that defines parent and children, or there could be two components)
- Nests
- IsNestedBy

- *HasContext*: [TODO: not sure what to do about this one yet...]

**Compostition**: this component stores information about parent/child relationships. 

- IsDecomposedBy
- Decomposes

### IfcObject

**Type**: this component replaces the *ObjectType* and *isTypedBy* properties.

- ~~*ObjectType*~~: 
- ~~*isTypedBy*~~
- *Type*: URI pointing to a Type defined in a Semantic Standard

Note that multiple types may be assigned to one entity.

### IfcProduct

**Geometry**:

The geometry component includes all the information from the following components:

- *Representation*
- *ObjectPlacement*

### IfcElement

- Tag - moved to **IfcCommon**

**StructureHierarchy**: this component describes the hierarchy of elements in a structure. It replaces the *ContainedInStructure* property.

It contains several properties:

- Parent (required): an entity GlobalID
- Siblings (optional, non-canonical): a list of entity GlobalIDs
- Children (optional, non-canonical): a list of entity GlobalIDs

The sibling and children properties are non-canonical since other objects may be added to the hierarchy after this component is published. Since they cannot be canonical, they are also optional.


For discussion: the following properties may not be needed:

- *Fills Voids*: could the Nesting, composition or structureHierarchy components do this work? e.g. if a Void is nested in an Openning, it means it fills the openning.
- *HasOpennings*: a publisher does not necessarily know what opennings others will add to a wall, so this property cannot be canonical. This can only be stated with regards to a specific federation of data.
- *PredefinedType*: There are (at least) two ways to address this:
	- create the specific types in the Type definition of the standard, then just assign two **Type** components / property sets to an object: one for the Wall Type and another for the specific/predefined type. This would allow other requirements to be defined for some predefined types (e.g. the STANDARD wall type may apply certain limitations to the **Geometry** component)
	- create a **WallProperties** component. This doesn't smell right to me...

## Type Definition

Multiple type definitons can exist for a given classification (e.g. for different LODs / LOINs). For this example, we identify what the type definition would look like for a Wall type that corresponds to an IFC4.3 wall.

An entity conforming to the Wall Type shall contain contain:

- 1: **IfcCommon** component
- 1: **Classification** component, with the *classification* property set to `https://identifier.buildingsmart.org/uri/buildingsmart/ifc-5.0-proposed/class/IfcWall`
- 1: **Type** component, with the *type* property set to `https://identifier.buildingsmart.org/uri/buildingsmart/ifc-5.0-proposed/type/Ifc43Wall`
- no more than 1: **Geometry** component
- no more than 1: **Nesting** component (note that the nesting component contains a list of *isNestedBy* entities)
- no more than 1: **Compositions** component

We note that the Type definition is a very close match to the IFC4.3 MVD definitions. For each component listed in the Type definition, we can specify:

- cardinality: an exact number or a maximum
- specific values of specific properties

Two notes:
- properties in IFC4.3 with a cardinality of [0:?] are excluded for these type definitions. Since they are optional and have no maximum number, their presence or absense will never affect a type check.
- further discussion is required to determine if Where-Rules are required, or if specifying specific properties can acheive the required definition.