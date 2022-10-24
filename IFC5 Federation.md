# Federation in IFC5

Author: David de Koning (Oasys Software, Arup)

Date: Octover 24, 2022

The entity-component model simplifies the specification of a data standard, allows participants in the standardization to agree incremntally, and allows the IFC4.3 standard to be expressed in this new architecture.

This system is almost too flexible. Anyone can publish a component that attaches to any entity! How can we prevent people from adding data that they shouldn't? How can we know that a set of data is coordinated, if everyone just gets to say whatever they want?

This is where the concept of a **federation** comes in. A **federation** (noun!) is a list of specific versions of data containers.

Let us consider an example project where three designers are contributing data containers:

- an Architect publishes a data container at https://architect.com/projectxyz/
- an Engineer publishes a data container at https://engineer.com/projectxyz/
- a quantitysurveyor publishes a data container at https://qs.com/projectxyz

Each time a data container is published, it is given a unique version ID. for the sake of this example, let us say that the version is the date and time it was published.

In addition, each party keeps two tags up to date: a `wip` tag that points to their latest work-in-progress and a `published` tag that points to the latest version that they are happy to share with the rest of the team.

A **federation** might look something like this:

```
{
"name": "Issued for Review, 2022-10-24",
"data-sources": [
	{"uri": "https://architect.com/projectxyz",
	"version": "2022-10-02 01:34:56",
	"hash": "2ldkjf0293944j2lk34jriod90s"},
	{"uri": "https://engineer.com/projectxyz/"",
	"version": "2022-10-14 21:45:32",
	"hash": "2llkjdoif02039jfal84h5"},
	{"uri": "https://qs.com/projectxyz",
	"query": "Type=Quanity",
	"version": "2022-10-20 14:13:45",
	"hash": "wdloiwjrj30942ufg9asud32h2"}
]
}
```

The **federation** is relatively simple. It contains a name that describes the data and a list of data sources. Each data source is identified by it's uri, version and optional query. A hash of the data is included so that if a publisher changes the contents of a particular version, all other parties will be able to detect the discrepancy.

The query allows a federation to only include some information from a publisher. In the example above, only **Quantity** components are included. The Quantity Surveyors may have published some other data for the team to see that did not need to be included in the data set that is issued for review.

The definition of a **federation** also includes precedence rules. This will need to be fleshed out, but one simple rule is that when components conflicts, the data lower down the list 'overwrites' the earlier components. There are two conditions when data will conflict:

1. Two publishers attach components to an entity, but the component is constrained to only 

Though it is possible to share data about any entity by simply publishing components that refer to the entity, it is not possible to add any data to a **federation**. A federation is equivalent to the transmittal the accompanies a set of contract documents. These documents are included and nothing else.

The above could be described as a **contract federation**. A **collaboration federation** would look similar except that instead of specific dated versions, it would specify a tag name, such as `wip` or `published`. All team members could point their working environment to such a federation and could (for example) receive notifications when someone pointed the `published` tag to a new data collection.