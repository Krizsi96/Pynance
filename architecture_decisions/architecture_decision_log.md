# Architecture Decision Log

This document is used to track key decisions made during the development of the project. This can be used at a later stage to understand why certain decisions were made.

## Table of Decisions

| Decision | Date | Alternative(s) | Reasoning | Decision Record | Made By |
| -------- | ---- | -------------- | --------- | --------------- | ------- |
| We will use Markdown files to track the architecture ecision made for the project | 2022-12-08 | Word document | The decision log evolves with the code and can be tracked in git | [0001 - Record architecture decisions](architecture_decision_records/0001_record_architecture_decisions.md) | [Krizsi96](https://github.com/Krizsi96) |
| The data will be stored in Googlesheets as a cloud database | 2022-12-08 | Local files | The data is stored in a cloud database, so it is accessable from all devices. The data is stored in a secure way, because the authentication is handled by Google | [0002 - Data Storage](architecture_decision_records/0002_data_storage.md) | [Krizsi96](https://github.com/Krizsi96) |
| We will use Python as the programming language for this project | 2022-12-08 | C, C++, Javascript | Python is a high level general purpose programming language. It is suitable for this project, because it is easy to implement the features mentioned above in Python | [0003 - Use Python Programming Language](architecture_decision_records/0003_use_python_programming_language.md) | [Krizsi96](https://github.com/Krizsi96) |
| We will use Monorepo structure for this project | 2022-12-08 | Submodules | The components are stored in a single repository. The team members can work on different components for coupled features without switching between repositories. Easier to change the architecture and interfaces of the components | [0004 - Using MonoRepo Structure](architecture_decision_records/0004_using_monorepo_structure.md) | [Krizsi96](https://github.com/Krizsi96) |