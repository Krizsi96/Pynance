# 0001 - Record architecture decisions

Date: 2022-12-08

## Context:

Not all requirements can be captured in the beginning of an agile project during one or more design session. The initial architecture design can evolve or change during the project.
Tracking these changes can be done...

...in Word document. This is a common way to store the decisions, however it is not easy to see changes made in the document for review.

...using Markdown files. This is a lightweight solution that can be easily tracked in git, and changes can be reviewed. However, there is no experience with this approach in the company.

Not tracking these decisions would lead to a situation where the team members would not be aware of the reasoning behind the decisions made, and they could change the architecture without knowing the context of some choices. Or they just not change the bad architecture decisions because of the same reason.

## Decision:

We will use Markdown files to track the architecture decisions made for this project.

## Consequences:

- The decision records will be stored in the repository under the folder `architecture_decision_records` and tracked in git.

- Pull request can be used for the review process of the new decisions

- The decision are recorded for future reference