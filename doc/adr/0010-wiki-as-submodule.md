# 10. Wiki as submodule

Date: 2018-02-17

## Status

Accepted

## Context

The new project guidelines prescribe the usage of the Wiki for documentation. This disconnects the documentation from the repository checkout which may be undesirable. GitLab wikis are in essence git repositories of their own that hold markdown.

## Decision

We will link the project's GitLab wiki as a submodule in `doc` folder. 

## Consequences

- `+` no documentation duplication
- `-` may be complicated to sync when the code goes public
