# 0004 - Using MonoRepo Structure

Date: 2022-12-08

## Context:

The project will have multiple components. The components could be stored in separate repositories or in a single repository. 

If the components are stored in separate repositories then the integration of the modules could be hard. Also the team members would have to switch between repositories to work on different components for coupled features. Increases the complexity of the dependency management.

There are several git architecture strategies that could work well for this scenario. Here are a few options:

**Monorepo:** In this architecture, all the code for the main application, libraries, and tool would be stored in a single repository. This can make it easier to manage dependencies and ensure that all the code is in sync. However, it can also make the repository quite large and complex.

**Submodules:** With this strategy, each component (main application, libraries, and tool) would have its own repository. The main application repository would then include the libraries and tool repositories as submodules. This can make it easier to manage each component separately and keep them up to date, but it can also require more effort to set up and maintain and can make it harder to manage dependencies.

## Decision:

We will use Monorepo structure for this project.

## Consequences:

- The components are stored in a single repository

- The team members can work on different components for coupled features without switching between repositories

- Easier to change the architecture and interfaces of the components